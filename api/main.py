"""FastAPI inference service for the EcoShield AI final model."""

from __future__ import annotations

import json
import os
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from catboost import Pool
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(
    os.getenv("ECOSHIELD_PROJECT_ROOT", Path(__file__).resolve().parents[1])
).resolve()
MODEL_PATH = Path(
    os.getenv(
        "ECOSHIELD_MODEL_PATH",
        PROJECT_ROOT / "models" / "heavy" / "optimized_single_heavy_model.joblib",
    )
)
SELECTION_PATH = Path(
    os.getenv(
        "ECOSHIELD_SELECTION_PATH",
        PROJECT_ROOT / "outputs" / "metrics" / "selected_single_heavy_model.csv",
    )
)
MANIFEST_PATH = Path(
    os.getenv(
        "ECOSHIELD_MANIFEST_PATH",
        PROJECT_ROOT / "outputs" / "metadata" / "common_cache_manifest.json",
    )
)
ID_COLUMN = "TransactionID"
TARGET_COLUMN = "isFraud"
MODEL_NAME = "cat_d8_balanced"
MAX_REQUEST_ROWS = int(os.getenv("ECOSHIELD_MAX_REQUEST_ROWS", "5000"))


def _project_path(entry: str) -> Path:
    """Resolve manifest paths written on either Windows or POSIX."""
    return PROJECT_ROOT / Path(entry.replace("\\", "/"))


class PredictionRequest(BaseModel):
    """One or more raw IEEE-CIS records."""

    records: list[dict[str, Any]] = Field(min_length=1)


class ExplanationRequest(BaseModel):
    """A single raw IEEE-CIS record for SHAP explanation."""

    record: dict[str, Any]
    top_n: int = Field(default=12, ge=1, le=500)


@dataclass
class RuntimeArtifacts:
    model: Any
    threshold: float
    feature_columns: list[str]
    numeric_columns: list[str]
    categorical_columns: list[str]
    categorical_indices: list[int]
    split_version: str | None
    preprocessing_profile: str | None


def _require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Gerekli dosya bulunamadı: {path}")


def load_runtime_artifacts() -> RuntimeArtifacts:
    """Load the model, fixed threshold and shared feature schema once."""
    for path in (MODEL_PATH, SELECTION_PATH, MANIFEST_PATH):
        _require_file(path)

    with MANIFEST_PATH.open(encoding="utf-8") as file:
        manifest = json.load(file)
    schema_entry = manifest.get("profiles", {}).get("common", {}).get("schema")
    if not schema_entry:
        raise KeyError("Manifest içinde profiles/common/schema kaydı bulunamadı.")
    schema_path = _project_path(schema_entry)
    _require_file(schema_path)
    with schema_path.open(encoding="utf-8") as file:
        schema = json.load(file)

    selection = pd.read_csv(SELECTION_PATH).iloc[0]
    if selection["trial_name"] != MODEL_NAME:
        raise ValueError(
            f"API {MODEL_NAME} bekliyor; {selection['trial_name']} bulundu."
        )

    model = joblib.load(MODEL_PATH)
    feature_columns = list(schema["feature_columns"])
    numeric_columns = list(schema["numeric_columns"])
    categorical_columns = list(schema["categorical_columns"])
    model_features = list(getattr(model, "feature_names_", []) or [])
    if model_features and model_features != feature_columns:
        raise ValueError("Model feature sırası ile ortak feature şeması uyuşmuyor.")

    return RuntimeArtifacts(
        model=model,
        threshold=float(selection["threshold"]),
        feature_columns=feature_columns,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        categorical_indices=[
            feature_columns.index(column) for column in categorical_columns
        ],
        split_version=(
            None
            if pd.isna(selection.get("split_version"))
            else str(selection.get("split_version"))
        ),
        preprocessing_profile=(
            None
            if pd.isna(selection.get("preprocessing_profile"))
            else str(selection.get("preprocessing_profile"))
        ),
    )


def prepare_model_frame(
    records: list[dict[str, Any]],
    runtime: RuntimeArtifacts,
) -> tuple[pd.DataFrame, list[Any], dict[str, Any]]:
    """Align raw records to the training schema without fitting anything."""
    if not records:
        raise ValueError("Tahmin girdisi boş.")
    if len(records) > MAX_REQUEST_ROWS:
        raise ValueError(
            f"Tek istekte en fazla {MAX_REQUEST_ROWS:,} satır gönderilebilir."
        )

    frame = pd.DataFrame(records)
    if frame.columns.duplicated().any():
        raise ValueError("Girdide tekrar eden kolon adları var.")
    target_was_removed = TARGET_COLUMN in frame.columns
    if target_was_removed:
        frame = frame.drop(columns=TARGET_COLUMN)

    if ID_COLUMN in frame.columns:
        transaction_ids = []
        for value in frame[ID_COLUMN].tolist():
            if pd.isna(value):
                transaction_ids.append(None)
            elif isinstance(value, np.generic):
                transaction_ids.append(value.item())
            else:
                transaction_ids.append(value)
        non_missing_ids = pd.Series(transaction_ids).dropna()
        if non_missing_ids.duplicated().any():
            raise ValueError("Girdi içinde tekrar eden TransactionID var.")
    else:
        transaction_ids = list(range(1, len(frame) + 1))

    missing_columns = [
        column for column in runtime.feature_columns if column not in frame
    ]
    extra_columns = [
        column
        for column in frame.columns
        if column not in runtime.feature_columns and column != ID_COLUMN
    ]
    frame = frame.reindex(columns=runtime.feature_columns).copy()

    for column in runtime.numeric_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    for column in runtime.categorical_columns:
        frame[column] = frame[column].astype("string").fillna("__MISSING__")

    report = {
        "row_count": len(frame),
        "required_feature_count": len(runtime.feature_columns),
        "provided_feature_count": len(runtime.feature_columns) - len(missing_columns),
        "missing_feature_count": len(missing_columns),
        "missing_features": missing_columns,
        "ignored_extra_columns": extra_columns,
        "target_was_removed": target_was_removed,
    }
    return frame, transaction_ids, report


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runtime = load_runtime_artifacts()
    yield
    app.state.runtime = None


app = FastAPI(
    title="EcoShield AI Inference API",
    version="1.0.0",
    description="CatBoost D8 Balanced fraud risk inference service.",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, Any]:
    runtime: RuntimeArtifacts = app.state.runtime
    return {
        "status": "ok",
        "model_loaded": runtime is not None,
        "model": MODEL_NAME,
    }


@app.get("/model-info")
def model_info() -> dict[str, Any]:
    runtime: RuntimeArtifacts = app.state.runtime
    return {
        "model": MODEL_NAME,
        "threshold": runtime.threshold,
        "feature_count": len(runtime.feature_columns),
        "split_version": runtime.split_version,
        "preprocessing_profile": runtime.preprocessing_profile,
    }


@app.post("/predict")
def predict(request: PredictionRequest) -> dict[str, Any]:
    runtime: RuntimeArtifacts = app.state.runtime
    try:
        prepared, transaction_ids, report = prepare_model_frame(
            request.records, runtime
        )
        if report["provided_feature_count"] == 0:
            raise ValueError("Model şemasındaki hiçbir özellik sağlanmadı.")
        started = time.perf_counter()
        probabilities = runtime.model.predict_proba(prepared)[:, 1]
        inference_seconds = time.perf_counter() - started
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="Tahmin işlemi başarısız.") from error

    predictions = (probabilities >= runtime.threshold).astype(np.int8)
    results = [
        {
            ID_COLUMN: transaction_id,
            "fraud_probability": float(probability),
            "decision_threshold": runtime.threshold,
            "fraud_prediction": int(prediction),
            "decision": "Fraud" if prediction else "Normal",
        }
        for transaction_id, probability, prediction in zip(
            transaction_ids, probabilities, predictions
        )
    ]
    return {
        "model": MODEL_NAME,
        "results": results,
        "input_report": report,
        "inference_seconds": inference_seconds,
    }


@app.post("/explain")
def explain(request: ExplanationRequest) -> dict[str, Any]:
    runtime: RuntimeArtifacts = app.state.runtime
    try:
        prepared, transaction_ids, report = prepare_model_frame(
            [request.record], runtime
        )
        if report["provided_feature_count"] == 0:
            raise ValueError("Model şemasındaki hiçbir özellik sağlanmadı.")
        pool = Pool(prepared, cat_features=runtime.categorical_indices)
        shap_values = runtime.model.get_feature_importance(pool, type="ShapValues")
        contributions = shap_values[0, :-1]
        order = np.argsort(np.abs(contributions))[::-1][: request.top_n]
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="SHAP açıklaması üretilemedi.") from error

    features = []
    for index in order:
        value = prepared.iloc[0, index]
        if pd.isna(value):
            value = None
        elif isinstance(value, np.generic):
            value = value.item()
        contribution = float(contributions[index])
        features.append({
            "feature": runtime.feature_columns[index],
            "value": value,
            "shap_value": contribution,
            "absolute_contribution": abs(contribution),
            "direction": (
                "Riski artırıyor" if contribution >= 0 else "Riski azaltıyor"
            ),
        })
    return {
        ID_COLUMN: transaction_ids[0],
        "base_value": float(shap_values[0, -1]),
        "features": features,
    }
