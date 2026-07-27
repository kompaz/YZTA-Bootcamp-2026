"""EcoShield AI ortak veri hazırlama ve preprocessing yardımcıları.

Bu modül model eğitmez. IEEE-CIS train dosyalarını birleştirir, ortak
train/validation/test splitini üretir ve model ailelerine göre hazırlanmış
cache dosyalarını kaydeder.
"""

from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import joblib
import numpy as np
import pandas as pd
import psutil
from scipy import sparse
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from tqdm.auto import tqdm


TARGET_COL = "isFraud"
ID_COL = "TransactionID"
RANDOM_STATE = 42
TRAIN_SIZE = 0.70
VALIDATION_SIZE = 0.15
TEST_SIZE = 0.15
HIGH_MISSING_THRESHOLD = 0.98
ONEHOT_MIN_FREQUENCY = 20
CSV_CHUNK_SIZE = 100_000


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    raw: Path
    processed: Path
    common: Path
    linear: Path
    sklearn_tree: Path
    lightgbm: Path
    catboost: Path
    outputs: Path
    splits: Path
    metrics: Path
    metadata: Path


@dataclass
class CommonData:
    merged: pd.DataFrame
    train_idx: np.ndarray
    val_idx: np.ndarray
    test_idx: np.ndarray
    feature_columns: list[str]
    numeric_columns: list[str]
    categorical_columns: list[str]
    high_missing_columns: list[str]
    constant_columns: list[str]
    missing_report: pd.DataFrame
    cardinality_report: pd.DataFrame
    dtype_report: pd.DataFrame
    quality_summary: pd.DataFrame
    split_summary: pd.DataFrame


def find_project_root(start_path: Path | None = None) -> Path:
    """IEEE-CIS ham dosyalarını içeren repository kökünü bulur."""
    start = (start_path or Path.cwd()).resolve()
    for candidate in [start, *start.parents]:
        raw = candidate / "data" / "raw"
        if (
            (raw / "train_transaction.csv").exists()
            and (raw / "train_identity.csv").exists()
        ):
            return candidate
    raise FileNotFoundError(
        "Repository kökü bulunamadı. train_transaction.csv ve "
        "train_identity.csv dosyalarını data/raw/ altına yerleştirin."
    )


def build_project_paths(root: Path) -> ProjectPaths:
    """Ortak giriş ve çıktı yollarını oluşturur."""
    root = root.resolve()
    processed = root / "data" / "processed"
    outputs = root / "outputs"
    paths = ProjectPaths(
        root=root,
        raw=root / "data" / "raw",
        processed=processed,
        common=processed / "common",
        linear=processed / "linear",
        sklearn_tree=processed / "sklearn_tree",
        lightgbm=processed / "lightgbm",
        catboost=processed / "catboost",
        outputs=outputs,
        splits=outputs / "splits",
        metrics=outputs / "metrics",
        metadata=outputs / "metadata",
    )
    for directory in [
        paths.common,
        paths.linear,
        paths.sklearn_tree,
        paths.lightgbm,
        paths.catboost,
        paths.splits,
        paths.metrics,
        paths.metadata,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    return paths


def memory_usage_gb() -> float:
    """Aktif Python sürecinin RAM kullanımını GB olarak döndürür."""
    return psutil.Process(os.getpid()).memory_info().rss / (1024**3)


@contextmanager
def step_timer(name: str) -> Iterator[None]:
    """Aşama adı, geçen süre ve RAM kullanımını raporlar."""
    started = time.perf_counter()
    print("\n" + "=" * 78)
    print("BAŞLADI:", name)
    print("=" * 78)
    try:
        yield
    finally:
        elapsed = time.perf_counter() - started
        print(
            f"TAMAMLANDI: {name} | geçen süre: {elapsed:.1f} sn "
            f"| RAM: {memory_usage_gb():.2f} GB"
        )


def count_csv_rows(path: Path) -> int:
    """Başlık hariç yaklaşık olmayan gerçek CSV satır sayısını sayar."""
    file_size = path.stat().st_size
    newline_count = 0
    last_byte = b""
    with path.open("rb") as file:
        with tqdm(
            total=file_size,
            desc=f"{path.name} satır sayımı",
            unit="B",
            unit_scale=True,
        ) as progress:
            while True:
                block = file.read(8 * 1024 * 1024)
                if not block:
                    break
                newline_count += block.count(b"\n")
                last_byte = block[-1:]
                progress.update(len(block))
    physical_lines = newline_count + int(file_size > 0 and last_byte != b"\n")
    return max(physical_lines - 1, 0)


def read_csv_with_progress(
    path: Path,
    *,
    chunk_size: int = CSV_CHUNK_SIZE,
    max_rows: int | None = None,
) -> pd.DataFrame:
    """CSV'yi chunk halinde, satır ilerlemesi ve RAM bilgisiyle okur."""
    total_rows = count_csv_rows(path)
    rows_to_read = min(total_rows, max_rows) if max_rows else total_rows
    chunks: list[pd.DataFrame] = []
    processed_rows = 0
    reader = pd.read_csv(path, chunksize=chunk_size, low_memory=False)

    with tqdm(
        total=rows_to_read,
        desc=f"{path.name} okunuyor",
        unit=" satır",
    ) as progress:
        for chunk in reader:
            if max_rows is not None:
                remaining = max_rows - processed_rows
                if remaining <= 0:
                    break
                chunk = chunk.iloc[:remaining]
            chunks.append(chunk)
            processed_rows += len(chunk)
            progress.update(len(chunk))
            progress.set_postfix(ram_gb=f"{memory_usage_gb():.2f}")
            if max_rows is not None and processed_rows >= max_rows:
                break

    if not chunks:
        raise ValueError(f"{path} dosyasından veri okunamadı.")
    frame = pd.concat(chunks, ignore_index=True)
    print(f"{path.name}: {len(frame):,} satır, {frame.shape[1]:,} kolon")
    return frame


def load_and_merge_train(
    paths: ProjectPaths,
    *,
    quick_rows: int | None = None,
) -> pd.DataFrame:
    """Train transaction ve identity dosyalarını doğrulayıp left join yapar."""
    transaction_path = paths.raw / "train_transaction.csv"
    identity_path = paths.raw / "train_identity.csv"
    with step_timer("IEEE-CIS train dosyalarını okuma"):
        transaction = read_csv_with_progress(
            transaction_path,
            max_rows=quick_rows,
        )
        identity = read_csv_with_progress(identity_path)

    missing_transaction = {ID_COL, TARGET_COL} - set(transaction.columns)
    if missing_transaction:
        raise KeyError(
            "train_transaction.csv içinde eksik zorunlu kolonlar: "
            + ", ".join(sorted(missing_transaction))
        )
    if ID_COL not in identity.columns:
        raise KeyError(f"train_identity.csv içinde {ID_COL} bulunamadı.")
    if transaction[ID_COL].isna().any():
        raise ValueError(f"train_transaction.csv içinde eksik {ID_COL} var.")
    if transaction[ID_COL].duplicated().any():
        raise ValueError(f"train_transaction.csv içinde tekrar eden {ID_COL} var.")
    if identity[ID_COL].duplicated().any():
        raise ValueError(f"train_identity.csv içinde tekrar eden {ID_COL} var.")
    if transaction[TARGET_COL].isna().any():
        raise ValueError(f"Target kolonu {TARGET_COL} eksik değer içeriyor.")

    unexpected_targets = sorted(set(transaction[TARGET_COL].unique()) - {0, 1})
    if unexpected_targets:
        raise ValueError(f"Beklenmeyen target değerleri: {unexpected_targets}")

    with step_timer("Transaction ve identity left join"):
        merged = transaction.merge(
            identity,
            on=ID_COL,
            how="left",
            validate="one_to_one",
            suffixes=("", "_identity"),
        )
    if len(merged) != len(transaction):
        raise RuntimeError("Left join sonrasında transaction satır sayısı değişti.")
    return merged


def create_common_split(target: pd.Series) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """%70/%15/%15 stratified indeks splitini üretir."""
    all_indices = np.arange(len(target), dtype=np.int64)
    temporary_size = VALIDATION_SIZE + TEST_SIZE
    test_share = TEST_SIZE / temporary_size
    train_idx, temporary_idx = train_test_split(
        all_indices,
        test_size=temporary_size,
        random_state=RANDOM_STATE,
        stratify=target,
    )
    val_idx, test_idx = train_test_split(
        temporary_idx,
        test_size=test_share,
        random_state=RANDOM_STATE,
        stratify=target.iloc[temporary_idx],
    )
    train_idx = np.sort(train_idx)
    val_idx = np.sort(val_idx)
    test_idx = np.sort(test_idx)
    combined = np.concatenate([train_idx, val_idx, test_idx])
    if len(combined) != len(target) or len(np.unique(combined)) != len(target):
        raise RuntimeError("Split indeksleri çakışıyor veya bazı satırlar eksik.")
    return train_idx, val_idx, test_idx


def _semantic_categorical_columns(feature_columns: list[str]) -> list[str]:
    """IEEE-CIS'te kod olarak saklanan gerçek kategorik kolonları seçer."""
    candidates = {
        "ProductCD",
        "card1",
        "card2",
        "card3",
        "card4",
        "card5",
        "card6",
        "addr1",
        "addr2",
        "P_emaildomain",
        "R_emaildomain",
        "M1",
        "M2",
        "M3",
        "M4",
        "M5",
        "M6",
        "M7",
        "M8",
        "M9",
        "DeviceType",
        "DeviceInfo",
        *{f"id_{number:02d}" for number in range(12, 39)},
    }
    return sorted(candidates.intersection(feature_columns))


def analyze_common_data(merged: pd.DataFrame) -> CommonData:
    """Kalite raporlarını, ortak spliti ve train-temelli feature şemasını üretir."""
    target = merged[TARGET_COL].astype(np.int8)
    with step_timer("%70/%15/%15 stratified split oluşturma"):
        train_idx, val_idx, test_idx = create_common_split(target)

    raw_features = [
        column for column in merged.columns if column not in {TARGET_COL, ID_COL}
    ]
    train_raw = merged.iloc[train_idx][raw_features]
    with step_timer("Train splitinde feature kalite kontrolleri"):
        train_missing_ratio = train_raw.isna().mean()
        high_missing = sorted(
            train_missing_ratio[
                train_missing_ratio > HIGH_MISSING_THRESHOLD
            ].index.tolist()
        )
        unique_counts = train_raw.nunique(dropna=False)
        constant = sorted(unique_counts[unique_counts <= 1].index.tolist())

    dropped = set(high_missing) | set(constant)
    feature_columns = [column for column in raw_features if column not in dropped]
    train_features = merged.iloc[train_idx][feature_columns]
    dtype_categorical = train_features.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()
    semantic_categorical = _semantic_categorical_columns(feature_columns)
    categorical = sorted(set(dtype_categorical) | set(semantic_categorical))
    numeric = [column for column in feature_columns if column not in categorical]

    with step_timer("Veri kalitesi raporlarını hazırlama"):
        missing_report = pd.DataFrame(
            {
                "column": merged.columns,
                "dtype": merged.dtypes.astype(str).values,
                "missing_count": merged.isna().sum().values,
                "missing_ratio": merged.isna().mean().values,
            }
        ).sort_values(
            ["missing_ratio", "column"],
            ascending=[False, True],
        ).reset_index(drop=True)

        cardinality_rows: list[dict[str, Any]] = []
        for column in tqdm(
            merged.columns,
            desc="Kardinalite hesaplanıyor",
            unit=" kolon",
        ):
            unique_count = int(merged[column].nunique(dropna=True))
            cardinality_rows.append(
                {
                    "column": column,
                    "dtype": str(merged[column].dtype),
                    "unique_count": unique_count,
                    "unique_ratio": float(unique_count / len(merged)),
                }
            )
        cardinality_report = pd.DataFrame(cardinality_rows).sort_values(
            ["unique_count", "column"],
            ascending=[False, True],
        ).reset_index(drop=True)
        dtype_report = (
            merged.dtypes.astype(str)
            .value_counts()
            .rename_axis("dtype")
            .reset_index(name="column_count")
        )

    quality_summary = pd.DataFrame(
        [
            {"metric": "row_count", "value": len(merged)},
            {"metric": "column_count", "value": merged.shape[1]},
            {"metric": "duplicate_row_count", "value": int(merged.duplicated().sum())},
            {"metric": "fraud_count", "value": int(target.sum())},
            {"metric": "normal_count", "value": int((target == 0).sum())},
            {"metric": "fraud_ratio", "value": float(target.mean())},
        ]
    )
    split_summary = pd.DataFrame(
        [
            _split_row("train", train_idx, target),
            _split_row("validation", val_idx, target),
            _split_row("test", test_idx, target),
        ]
    )
    return CommonData(
        merged=merged,
        train_idx=train_idx,
        val_idx=val_idx,
        test_idx=test_idx,
        feature_columns=feature_columns,
        numeric_columns=numeric,
        categorical_columns=categorical,
        high_missing_columns=high_missing,
        constant_columns=constant,
        missing_report=missing_report,
        cardinality_report=cardinality_report,
        dtype_report=dtype_report,
        quality_summary=quality_summary,
        split_summary=split_summary,
    )


def _split_row(name: str, indices: np.ndarray, target: pd.Series) -> dict[str, Any]:
    split_target = target.iloc[indices]
    return {
        "split": name,
        "row_count": len(indices),
        "row_ratio": len(indices) / len(target),
        "fraud_count": int(split_target.sum()),
        "fraud_ratio": float(split_target.mean()),
    }


def make_one_hot_encoder() -> OneHotEncoder:
    """Scikit-learn sürümüne uygun sparse encoder üretir."""
    arguments = {
        "handle_unknown": "ignore",
        "min_frequency": ONEHOT_MIN_FREQUENCY,
    }
    try:
        return OneHotEncoder(sparse_output=True, **arguments)
    except TypeError:
        return OneHotEncoder(sparse=True, **arguments)


def build_sklearn_preprocessor(
    profile: str,
    numeric_columns: list[str],
    categorical_columns: list[str],
) -> ColumnTransformer:
    """Linear veya tree/boosting sparse preprocessing pipeline'ı üretir."""
    if profile not in {"linear", "sklearn_tree"}:
        raise ValueError("profile linear veya sklearn_tree olmalıdır.")
    numeric_steps: list[tuple[str, Any]] = [
        ("imputer", SimpleImputer(strategy="median"))
    ]
    if profile == "linear":
        numeric_steps.append(("scaler", StandardScaler()))
    return ColumnTransformer(
        transformers=[
            ("numeric", Pipeline(numeric_steps), numeric_columns),
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", make_one_hot_encoder()),
                    ]
                ),
                categorical_columns,
            ),
        ],
        remainder="drop",
        sparse_threshold=1.0,
    )


def _split_indices(data: CommonData) -> dict[str, np.ndarray]:
    return {
        "train": data.train_idx,
        "validation": data.val_idx,
        "test": data.test_idx,
    }


def _select_feature_frame(data: CommonData, indices: np.ndarray) -> pd.DataFrame:
    """Yalnızca işlenecek split için feature DataFrame'ini belleğe alır."""
    return data.merged.iloc[indices][data.feature_columns].copy()


def save_common_artifacts(
    data: CommonData,
    paths: ProjectPaths,
    *,
    quick_mode: bool,
) -> dict[str, Path]:
    """Ortak taban veriyi, indeksleri, target/ID'leri ve raporları kaydeder."""
    prefix = "quick" if quick_mode else "common"
    base_path = paths.common / f"{prefix}_feature_base.parquet"
    split_path = paths.splits / f"{prefix}_split_indices.npz"
    labels_path = paths.splits / f"{prefix}_split_targets_ids.npz"
    schema_path = paths.metadata / f"{prefix}_feature_schema.json"

    base_columns = [ID_COL, TARGET_COL, *data.feature_columns]
    with step_timer("Ortak Parquet tabanını kaydetme"):
        data.merged[base_columns].to_parquet(
            base_path,
            index=False,
            compression="zstd",
        )
    target = data.merged[TARGET_COL].astype(np.int8)
    identifiers = data.merged[ID_COL].to_numpy()
    np.savez_compressed(
        split_path,
        train_idx=data.train_idx,
        val_idx=data.val_idx,
        test_idx=data.test_idx,
        random_state=np.array([RANDOM_STATE], dtype=np.int64),
    )
    np.savez_compressed(
        labels_path,
        y_train=target.iloc[data.train_idx].to_numpy(),
        y_validation=target.iloc[data.val_idx].to_numpy(),
        y_test=target.iloc[data.test_idx].to_numpy(),
        id_train=identifiers[data.train_idx],
        id_validation=identifiers[data.val_idx],
        id_test=identifiers[data.test_idx],
    )

    data.split_summary.to_csv(
        paths.metrics / f"{prefix}_split_summary.csv",
        index=False,
    )
    data.quality_summary.to_csv(
        paths.metrics / f"{prefix}_data_quality_report.csv",
        index=False,
    )
    data.missing_report.to_csv(
        paths.metrics / f"{prefix}_missing_value_report.csv",
        index=False,
    )
    data.cardinality_report.to_csv(
        paths.metrics / f"{prefix}_cardinality_report.csv",
        index=False,
    )
    data.dtype_report.to_csv(
        paths.metrics / f"{prefix}_dtype_report.csv",
        index=False,
    )

    schema = {
        "schema_version": "common_v2",
        "quick_mode": quick_mode,
        "target_column": TARGET_COL,
        "id_column": ID_COL,
        "random_state": RANDOM_STATE,
        "split_ratios": {
            "train": TRAIN_SIZE,
            "validation": VALIDATION_SIZE,
            "test": TEST_SIZE,
        },
        "high_missing_threshold": HIGH_MISSING_THRESHOLD,
        "feature_columns": data.feature_columns,
        "numeric_columns": data.numeric_columns,
        "categorical_columns": data.categorical_columns,
        "dropped_high_missing_columns": data.high_missing_columns,
        "dropped_constant_columns": data.constant_columns,
    }
    with schema_path.open("w", encoding="utf-8") as file:
        json.dump(schema, file, ensure_ascii=False, indent=2)
    return {
        "base": base_path,
        "split": split_path,
        "labels": labels_path,
        "schema": schema_path,
    }


def save_sparse_profile(
    data: CommonData,
    paths: ProjectPaths,
    *,
    profile: str,
    quick_mode: bool,
) -> dict[str, Path]:
    """Linear veya tree/XGBoost sparse cache'ini train-fitted olarak kaydeder."""
    if profile not in {"linear", "sklearn_tree"}:
        raise ValueError("profile linear veya sklearn_tree olmalıdır.")
    output_dir = paths.linear if profile == "linear" else paths.sklearn_tree
    prefix = "quick_" if quick_mode else ""
    preprocessor = build_sklearn_preprocessor(
        profile,
        data.numeric_columns,
        data.categorical_columns,
    )
    with step_timer(f"{profile} preprocessing — train fit_transform"):
        train_frame = _select_feature_frame(data, data.train_idx)
        train_matrix = preprocessor.fit_transform(train_frame)
        del train_frame

    saved: dict[str, Path] = {}
    train_path = output_dir / f"{prefix}X_train.npz"
    train_matrix = sparse.csr_matrix(train_matrix)
    sparse.save_npz(train_path, train_matrix, compressed=True)
    saved["train"] = train_path
    print(f"{profile}/train: {train_matrix.shape}, nnz={train_matrix.nnz:,}")
    del train_matrix

    for split_name, indices in [
        ("validation", data.val_idx),
        ("test", data.test_idx),
    ]:
        with step_timer(f"{profile} preprocessing — {split_name} transform"):
            frame = _select_feature_frame(data, indices)
            matrix = sparse.csr_matrix(preprocessor.transform(frame))
            del frame
        matrix_path = output_dir / f"{prefix}X_{split_name}.npz"
        sparse.save_npz(matrix_path, matrix, compressed=True)
        saved[split_name] = matrix_path
        print(f"{profile}/{split_name}: {matrix.shape}, nnz={matrix.nnz:,}")
        del matrix
    preprocessor_path = output_dir / f"{prefix}preprocessor.joblib"
    joblib.dump(preprocessor, preprocessor_path, compress=3)
    saved["preprocessor"] = preprocessor_path
    return saved


def _lightgbm_categories(data: CommonData) -> dict[str, pd.Index]:
    train_frame = _select_feature_frame(data, data.train_idx)
    categories: dict[str, pd.Index] = {}
    for column in tqdm(
        data.categorical_columns,
        desc="LightGBM train kategorileri öğreniliyor",
        unit=" kolon",
    ):
        train_values = train_frame[column].astype("string").fillna("__MISSING__")
        categories[column] = pd.Index(train_values.unique())
    del train_frame
    return categories


def _prepare_native_frame(
    frame: pd.DataFrame,
    categorical_columns: list[str],
    *,
    profile: str,
    lightgbm_categories: dict[str, pd.Index] | None = None,
) -> pd.DataFrame:
    for column in categorical_columns:
        values = frame[column].astype("string").fillna("__MISSING__")
        if profile == "lightgbm":
            if lightgbm_categories is None:
                raise ValueError("LightGBM train kategorileri sağlanmalıdır.")
            frame[column] = pd.Categorical(
                values,
                categories=lightgbm_categories[column],
            )
        else:
            frame[column] = values
    return frame


def save_native_profile(
    data: CommonData,
    paths: ProjectPaths,
    *,
    profile: str,
    quick_mode: bool,
) -> dict[str, Path]:
    """LightGBM veya CatBoost için hazırlanmış Parquet splitlerini kaydeder."""
    if profile == "lightgbm":
        output_dir = paths.lightgbm
        category_map = _lightgbm_categories(data)
    elif profile == "catboost":
        output_dir = paths.catboost
        category_map = None
    else:
        raise ValueError("profile lightgbm veya catboost olmalıdır.")
    prefix = "quick_" if quick_mode else ""
    saved: dict[str, Path] = {}
    for split_name, indices in _split_indices(data).items():
        frame = _select_feature_frame(data, indices)
        frame = _prepare_native_frame(
            frame,
            data.categorical_columns,
            profile=profile,
            lightgbm_categories=category_map,
        )
        path = output_dir / f"{prefix}{split_name}.parquet"
        with step_timer(f"{profile}/{split_name} Parquet kaydı"):
            frame.to_parquet(path, index=False, compression="zstd")
        saved[split_name] = path
        del frame
    return saved


def save_cache_manifest(
    paths: ProjectPaths,
    artifacts: dict[str, dict[str, Path]],
    *,
    quick_mode: bool,
) -> Path:
    """Üretilen cache dosyalarının yollarını ve rollerini JSON'a kaydeder."""
    prefix = "quick" if quick_mode else "common"
    manifest_path = paths.metadata / f"{prefix}_cache_manifest.json"
    manifest = {
        "cache_version": "cache_v1",
        "quick_mode": quick_mode,
        "profiles": {
            profile: {
                key: str(path.relative_to(paths.root))
                for key, path in profile_paths.items()
            }
            for profile, profile_paths in artifacts.items()
        },
        "profile_aliases": {
            "xgboost": "sklearn_tree",
            "decision_tree": "sklearn_tree",
            "random_forest": "sklearn_tree",
            "logistic_regression": "linear",
        },
    }
    with manifest_path.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)
    return manifest_path


def _load_common_data_from_cache(
    paths: ProjectPaths,
    manifest: dict[str, Any],
) -> CommonData:
    """Modele özel cache üretmek için ortak Parquet ve şemayı yeniden yükler."""
    common_entries = manifest["profiles"].get("common")
    if not common_entries:
        raise KeyError("Manifest içinde ortak veri girdileri bulunamadı.")

    base_path = paths.root / common_entries["base"]
    split_path = paths.root / common_entries["split"]
    schema_path = paths.root / common_entries["schema"]
    for path in [base_path, split_path, schema_path]:
        if not path.exists():
            raise FileNotFoundError(
                f"{path} bulunamadı. Önce 03_common_preprocessing.ipynb "
                "notebookunu çalıştırın."
            )

    with step_timer("Ortak Parquet cache'ini yükleme"):
        merged = pd.read_parquet(base_path)
    split = np.load(split_path)
    with schema_path.open(encoding="utf-8") as file:
        schema = json.load(file)

    return CommonData(
        merged=merged,
        train_idx=split["train_idx"],
        val_idx=split["val_idx"],
        test_idx=split["test_idx"],
        feature_columns=schema["feature_columns"],
        numeric_columns=schema["numeric_columns"],
        categorical_columns=schema["categorical_columns"],
        high_missing_columns=schema["dropped_high_missing_columns"],
        constant_columns=schema["dropped_constant_columns"],
        missing_report=pd.DataFrame(),
        cardinality_report=pd.DataFrame(),
        dtype_report=pd.DataFrame(),
        quality_summary=pd.DataFrame(),
        split_summary=pd.DataFrame(),
    )


def _manifest_profile_files_exist(
    paths: ProjectPaths,
    entries: dict[str, str],
) -> bool:
    return bool(entries) and all((paths.root / path).exists() for path in entries.values())


def _write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)


def get_or_create_profile_cache(
    profile: str,
    project_root: Path | None = None,
    *,
    quick_mode: bool = False,
    force_rebuild: bool = False,
    include_test: bool = True,
) -> dict[str, Any]:
    """İstenen profil cache'ini yükler; yoksa ortak tabandan bir kez üretir.

    Desteklenen kullanıcı adları:
    logistic_regression, linear, decision_tree, random_forest, xgboost,
    sklearn_tree, lightgbm ve catboost.
    """
    paths, manifest = load_cache_manifest(project_root, quick_mode=quick_mode)
    canonical_profile = manifest["profile_aliases"].get(profile, profile)
    if canonical_profile not in {
        "linear",
        "sklearn_tree",
        "lightgbm",
        "catboost",
    }:
        raise ValueError(f"Desteklenmeyen preprocessing profili: {profile}")

    existing = manifest["profiles"].get(canonical_profile, {})
    cache_ready = _manifest_profile_files_exist(paths, existing)
    if cache_ready and not force_rebuild:
        print(f"{canonical_profile} cache hazır; yeniden preprocessing yapılmayacak.")
    else:
        print(f"{canonical_profile} cache bulunamadı; ortak Parquet'ten oluşturuluyor.")
        common_data = _load_common_data_from_cache(paths, manifest)
        if canonical_profile in {"linear", "sklearn_tree"}:
            created = save_sparse_profile(
                common_data,
                paths,
                profile=canonical_profile,
                quick_mode=quick_mode,
            )
        else:
            created = save_native_profile(
                common_data,
                paths,
                profile=canonical_profile,
                quick_mode=quick_mode,
            )
        manifest["profiles"][canonical_profile] = {
            key: str(path.relative_to(paths.root))
            for key, path in created.items()
        }
        prefix = "quick" if quick_mode else "common"
        _write_manifest(
            paths.metadata / f"{prefix}_cache_manifest.json",
            manifest,
        )
        del common_data

    if canonical_profile in {"linear", "sklearn_tree"}:
        return load_sparse_profile(
            canonical_profile,
            paths.root,
            quick_mode=quick_mode,
            include_test=include_test,
        )
    return load_native_profile(
        canonical_profile,
        paths.root,
        quick_mode=quick_mode,
        include_test=include_test,
    )


def load_cache_manifest(
    project_root: Path | None = None,
    *,
    quick_mode: bool = False,
) -> tuple[ProjectPaths, dict[str, Any]]:
    """Sonraki notebookların kullanacağı cache manifestini yükler."""
    root = find_project_root(project_root)
    paths = build_project_paths(root)
    prefix = "quick" if quick_mode else "common"
    manifest_path = paths.metadata / f"{prefix}_cache_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"{manifest_path} bulunamadı. Önce 03_common_preprocessing.ipynb "
            "notebookunu çalıştırın."
        )
    with manifest_path.open(encoding="utf-8") as file:
        return paths, json.load(file)


def load_sparse_profile(
    profile: str,
    project_root: Path | None = None,
    *,
    quick_mode: bool = False,
    include_test: bool = True,
) -> dict[str, Any]:
    """Linear/tree/XGBoost cache'ini model notebookuna yükler."""
    paths, manifest = load_cache_manifest(project_root, quick_mode=quick_mode)
    alias = manifest["profile_aliases"].get(profile, profile)
    if alias not in {"linear", "sklearn_tree"}:
        raise ValueError("İstenen profil sparse cache kullanmıyor.")
    entries = manifest["profiles"][alias]
    labels_entry = manifest["profiles"]["common"]["labels"]
    labels = np.load(paths.root / labels_entry)
    loaded = {
        "X_train": sparse.load_npz(paths.root / entries["train"]),
        "X_validation": sparse.load_npz(paths.root / entries["validation"]),
        "y_train": labels["y_train"],
        "y_validation": labels["y_validation"],
        "id_train": labels["id_train"],
        "id_validation": labels["id_validation"],
        "preprocessor": joblib.load(paths.root / entries["preprocessor"]),
    }
    if include_test:
        loaded.update(
            {
                "X_test": sparse.load_npz(paths.root / entries["test"]),
                "y_test": labels["y_test"],
                "id_test": labels["id_test"],
            }
        )
    return loaded


def load_native_profile(
    profile: str,
    project_root: Path | None = None,
    *,
    quick_mode: bool = False,
    include_test: bool = True,
) -> dict[str, Any]:
    """LightGBM/CatBoost Parquet cache'ini model notebookuna yükler."""
    if profile not in {"lightgbm", "catboost"}:
        raise ValueError("profile lightgbm veya catboost olmalıdır.")
    paths, manifest = load_cache_manifest(project_root, quick_mode=quick_mode)
    entries = manifest["profiles"][profile]
    labels_entry = manifest["profiles"]["common"]["labels"]
    labels = np.load(paths.root / labels_entry)
    loaded = {
        "X_train": pd.read_parquet(paths.root / entries["train"]),
        "X_validation": pd.read_parquet(paths.root / entries["validation"]),
        "y_train": labels["y_train"],
        "y_validation": labels["y_validation"],
        "id_train": labels["id_train"],
        "id_validation": labels["id_validation"],
    }
    if include_test:
        loaded.update(
            {
                "X_test": pd.read_parquet(paths.root / entries["test"]),
                "y_test": labels["y_test"],
                "id_test": labels["id_test"],
            }
        )
    return loaded
