"""EcoShield AI — D8 Balanced fraud detection Streamlit prototype."""

from __future__ import annotations

import io
import html
import json
import os
import time
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
MODEL_PATH = PROJECT_ROOT / "models" / "heavy" / "optimized_single_heavy_model.joblib"
SELECTION_PATH = PROJECT_ROOT / "outputs" / "metrics" / "selected_single_heavy_model.csv"
MANIFEST_PATH = PROJECT_ROOT / "outputs" / "metadata" / "common_cache_manifest.json"
FINAL_METRICS_PATH = PROJECT_ROOT / "outputs" / "metrics" / "final_test_comparison.csv"
CONFUSION_FIGURE_PATH = PROJECT_ROOT / "outputs" / "figures" / "final_test_confusion_matrices.png"
CURVES_FIGURE_PATH = PROJECT_ROOT / "outputs" / "figures" / "final_test_pr_roc_curves.png"
FINAL_PREDICTIONS_PATH = (
    PROJECT_ROOT / "outputs" / "predictions" / "final_test_predictions.parquet"
)
TARGET_COLUMN = "isFraud"
ID_COLUMN = "TransactionID"
API_CHUNK_SIZE = int(os.getenv("ECOSHIELD_API_CHUNK_SIZE", "1000"))
API_BASE_URL = os.getenv("ECOSHIELD_API_URL", "http://127.0.0.1:8000").rstrip("/")
API_TIMEOUT_SECONDS = float(os.getenv("ECOSHIELD_API_TIMEOUT", "120"))


def project_path(entry: str) -> Path:
    """Resolve manifest paths written on either Windows or POSIX."""
    return PROJECT_ROOT / Path(entry.replace("\\", "/"))


st.set_page_config(
    page_title="EcoShield AI",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --eco-bg: #0b1018;
        --eco-panel: #151c2b;
        --eco-panel-2: #1c2538;
        --eco-border: #2b3650;
        --eco-text: #f6f8fc;
        --eco-muted: #9facbf;
        --eco-blue: #36a3ff;
        --eco-red: #ff4b55;
        --eco-green: #26c281;
        --eco-orange: #f5a623;
    }
    .stApp { background: var(--eco-bg); }
    [data-testid="stSidebar"] { background: #131a29; }
    [data-testid="stSidebar"] > div { border-right: 1px solid var(--eco-border); }
    .block-container { max-width: 1450px; padding-top: 2.2rem; }
    h1, h2, h3 { letter-spacing: -0.02em; }
    .eco-hero {
        padding: 0.4rem 0 1.25rem 0;
        border-bottom: 1px solid var(--eco-border);
        margin-bottom: 1rem;
    }
    .eco-hero h1 { font-size: 3rem; margin: 0; color: var(--eco-text); }
    .eco-hero p { color: var(--eco-muted); font-size: 1.05rem; margin: 0.45rem 0 0; }
    .eco-card {
        background: linear-gradient(145deg, var(--eco-panel-2), var(--eco-panel));
        border: 1px solid var(--eco-border);
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        min-height: 132px;
        box-shadow: 0 10px 28px rgba(0,0,0,.16);
    }
    .eco-card-label { color: var(--eco-muted); font-size: .92rem; }
    .eco-card-value { color: var(--eco-text); font-size: 2rem; font-weight: 750; margin-top: .35rem; }
    .eco-card-note { color: var(--eco-muted); font-size: .86rem; margin-top: .25rem; }
    .eco-action {
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin: 1rem 0;
        border-left: 6px solid;
    }
    .eco-action h3 { margin: 0 0 .5rem; }
    .eco-gauge {
        position: relative;
        height: 72px;
        border-radius: 12px;
        background: linear-gradient(90deg, #178554 0 35%, #bd7a13 35% 65%, #a62f35 65% 100%);
        margin: .8rem 0 1.4rem;
        border: 10px solid #080c12;
    }
    .eco-gauge-marker {
        position: absolute;
        top: -17px;
        width: 4px;
        height: 76px;
        background: white;
        box-shadow: 0 0 0 5px #ff4b77, 0 0 18px rgba(255,75,119,.8);
    }
    .eco-gauge-label {
        position: absolute;
        top: -42px;
        transform: translateX(-50%);
        color: white;
        font-weight: 800;
        font-size: 1.15rem;
    }
    .eco-threshold {
        position: absolute;
        bottom: -30px;
        transform: translateX(-50%);
        color: var(--eco-muted);
        font-size: .78rem;
        white-space: nowrap;
    }
    .eco-section {
        background: var(--eco-panel);
        border: 1px solid var(--eco-border);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: .75rem 0;
    }
    .eco-feature-up { color: #ff635f; font-weight: 700; }
    .eco-feature-down { color: #48a8ff; font-weight: 700; }
    div[data-baseweb="tab-list"] { gap: .55rem; border-bottom: 1px solid var(--eco-border); }
    button[data-baseweb="tab"] {
        background: var(--eco-panel);
        border-radius: 10px 10px 0 0;
        padding: .65rem 1.05rem;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: #ff496b;
        color: white;
    }
    div.stButton > button { border-radius: 10px; min-height: 44px; }
    div[data-testid="stMetric"] {
        background: var(--eco-panel);
        border: 1px solid var(--eco-border);
        border-radius: 12px;
        padding: .8rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _require_file(path: Path, explanation: str) -> None:
    if not path.exists():
        st.error(f"{explanation}\n\nEksik dosya: `{path.relative_to(PROJECT_ROOT)}`")
        st.stop()


def api_request(method: str, endpoint: str, **kwargs: Any) -> dict[str, Any]:
    """Call the model API and expose a readable error to the UI."""
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{endpoint}",
            timeout=API_TIMEOUT_SECONDS,
            **kwargs,
        )
    except requests.RequestException as error:
        raise ConnectionError(
            f"EcoShield API'ye ulaşılamadı: {API_BASE_URL}. "
            "Önce FastAPI servisini başlatın."
        ) from error
    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"API hatası ({response.status_code}): {detail}")
    return response.json()


@st.cache_resource(show_spinner="EcoShield API ve feature şeması kontrol ediliyor...")
def load_runtime_artifacts() -> dict[str, Any]:
    _require_file(
        SELECTION_PATH,
        "Seçilmiş model metadata dosyası bulunamadı.",
    )
    _require_file(
        MANIFEST_PATH,
        "Ortak cache manifesti bulunamadı. Önce Görev 1'i çalıştırın.",
    )

    with MANIFEST_PATH.open(encoding="utf-8") as file:
        manifest = json.load(file)
    common_entries = manifest.get("profiles", {}).get("common", {})
    schema_entry = common_entries.get("schema")
    if not schema_entry:
        raise KeyError("Manifest içinde common/schema kaydı bulunamadı.")
    schema_path = project_path(schema_entry)
    if not schema_path.exists():
        raise FileNotFoundError(f"Feature şeması bulunamadı: {schema_path}")
    with schema_path.open(encoding="utf-8") as file:
        schema = json.load(file)

    selection = pd.read_csv(SELECTION_PATH).iloc[0]
    if selection["trial_name"] != "cat_d8_balanced":
        raise ValueError(
            "Streamlit prototipi cat_d8_balanced bekliyor; "
            f"{selection['trial_name']} bulundu."
        )

    feature_columns = list(schema["feature_columns"])
    numeric_columns = list(schema["numeric_columns"])
    categorical_columns = list(schema["categorical_columns"])
    test_entry = manifest.get("profiles", {}).get("catboost", {}).get("test")
    test_cache_path = (
        project_path(test_entry)
        if test_entry
        else PROJECT_ROOT / "data" / "processed" / "catboost" / "test.parquet"
    )

    api_info = api_request("GET", "/model-info")
    if api_info.get("model") != "cat_d8_balanced":
        raise ValueError("API beklenen cat_d8_balanced modelini sunmuyor.")
    if int(api_info.get("feature_count", -1)) != len(feature_columns):
        raise ValueError("API feature sayısı ile ortak feature şeması uyuşmuyor.")
    if not np.isclose(float(api_info["threshold"]), float(selection["threshold"])):
        raise ValueError("API threshold değeri ile seçilmiş threshold uyuşmuyor.")

    return {
        "threshold": float(api_info["threshold"]),
        "selection": selection.to_dict(),
        "feature_columns": feature_columns,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "schema_path": schema_path,
        "test_cache_path": test_cache_path,
        "manifest": manifest,
        "api_info": api_info,
        "api_url": API_BASE_URL,
    }


def _json_safe(value: Any) -> Any:
    if pd.isna(value):
        return None
    if isinstance(value, np.generic):
        return value.item()
    return value


@st.cache_data(show_spinner="Gerçek demo işlemleri hazırlanıyor...")
def load_demo_profiles(
    test_cache_path: str,
    predictions_path: str,
    threshold: float,
) -> dict[str, dict[str, Any]]:
    test_path = Path(test_cache_path)
    prediction_path = Path(predictions_path)
    if not test_path.exists() or not prediction_path.exists():
        return {}

    predictions = pd.read_parquet(
        prediction_path,
        columns=[ID_COLUMN, "single_d8_probability"],
    )
    probabilities = predictions["single_d8_probability"].to_numpy()
    positions = {
        "🔥 Yüksek riskli işlem": int(np.argmax(probabilities)),
        "✅ Düşük riskli işlem": int(np.argmin(probabilities)),
        "⚠️ Sınırda işlem": int(np.argmin(np.abs(probabilities - threshold))),
    }
    test_frame = pd.read_parquet(test_path)
    profiles: dict[str, dict[str, Any]] = {}
    for label, position in positions.items():
        row = test_frame.iloc[position].to_dict()
        row[ID_COLUMN] = _json_safe(predictions.iloc[position][ID_COLUMN])
        profiles[label] = {
            "payload": {
                key: _json_safe(value) for key, value in row.items()
            },
            "reference_probability": float(probabilities[position]),
        }
    return profiles


def merge_transaction_identity(
    transaction_frame: pd.DataFrame,
    identity_frame: pd.DataFrame | None,
) -> pd.DataFrame:
    transaction_frame = transaction_frame.copy()
    if identity_frame is None:
        return transaction_frame
    if ID_COLUMN not in transaction_frame.columns or ID_COLUMN not in identity_frame.columns:
        raise KeyError(
            "Transaction ve identity dosyalarının ikisinde de TransactionID bulunmalıdır."
        )
    if identity_frame[ID_COLUMN].duplicated().any():
        raise ValueError("Identity dosyasında tekrar eden TransactionID var.")
    overlap = (
        set(transaction_frame.columns)
        & set(identity_frame.columns)
    ) - {ID_COLUMN}
    if overlap:
        raise ValueError(
            "Transaction ve identity dosyalarında çakışan kolonlar var: "
            + ", ".join(sorted(overlap)[:20])
        )
    return transaction_frame.merge(
        identity_frame,
        on=ID_COLUMN,
        how="left",
        validate="many_to_one",
    )


def frame_to_api_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert pandas and NumPy scalar values to JSON-safe Python values."""
    records: list[dict[str, Any]] = []
    for record in frame.to_dict(orient="records"):
        records.append({key: _json_safe(value) for key, value in record.items()})
    return records


def predict_with_api(
    raw_frame: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, Any], float]:
    if raw_frame.empty:
        raise ValueError("Tahmin girdisi boş.")
    if raw_frame.columns.duplicated().any():
        duplicates = raw_frame.columns[raw_frame.columns.duplicated()].tolist()
        raise ValueError(f"Tekrar eden kolon adları: {duplicates[:20]}")
    raw_frame = raw_frame.copy()
    if ID_COLUMN in raw_frame and raw_frame[ID_COLUMN].dropna().duplicated().any():
        raise ValueError("Girdi içinde tekrar eden TransactionID var.")
    if ID_COLUMN not in raw_frame:
        raw_frame.insert(0, ID_COLUMN, np.arange(1, len(raw_frame) + 1))

    row_count = len(raw_frame)
    progress = st.progress(0.0, text="API tahmini hazırlanıyor...")
    status = st.empty()
    results: list[dict[str, Any]] = []
    report: dict[str, Any] | None = None
    api_inference_seconds = 0.0
    started = time.perf_counter()

    for start in range(0, row_count, API_CHUNK_SIZE):
        end = min(start + API_CHUNK_SIZE, row_count)
        response = api_request(
            "POST",
            "/predict",
            json={"records": frame_to_api_records(raw_frame.iloc[start:end])},
        )
        results.extend(response["results"])
        api_inference_seconds += float(response["inference_seconds"])
        if report is None:
            report = response["input_report"]
            report["row_count"] = row_count
        processed = end
        elapsed = time.perf_counter() - started
        rate = processed / elapsed if elapsed > 0 else 0.0
        remaining = row_count - processed
        eta = remaining / rate if rate > 0 else 0.0
        progress.progress(
            processed / row_count,
            text=(
                f"API ilerleme: {processed:,}/{row_count:,} "
                f"(%{100 * processed / row_count:.1f})"
            ),
        )
        status.caption(
            f"Geçen süre: {elapsed:.1f} sn · Hız: {rate:,.0f} satır/sn · ETA: {eta:.1f} sn"
        )

    total_elapsed = time.perf_counter() - started
    progress.empty()
    status.empty()
    if report is None:
        raise RuntimeError("API geçerli bir input raporu döndürmedi.")
    report["api_inference_seconds"] = api_inference_seconds
    return pd.DataFrame(results), report, total_elapsed


def show_input_report(report: dict[str, Any]) -> None:
    columns = st.columns(4)
    columns[0].metric("Satır", f"{report['row_count']:,}")
    columns[1].metric("Gerekli özellik", report["required_feature_count"])
    columns[2].metric("Sağlanan özellik", report["provided_feature_count"])
    columns[3].metric("Eksik özellik", report["missing_feature_count"])

    if report["target_was_removed"]:
        st.warning("`isFraud` girdiden çıkarıldı; tahmin sırasında hedef kullanılmadı.")
    if report["missing_features"]:
        with st.expander("Eksik özellikler"):
            st.write(report["missing_features"])
    if report["ignored_extra_columns"]:
        with st.expander("Model tarafından kullanılmayan ek kolonlar"):
            st.write(report["ignored_extra_columns"])


def risk_label(probability: float, threshold: float) -> tuple[str, str, str]:
    if probability >= threshold:
        return "Yüksek", "🔥", "#ff4b55"
    if probability >= threshold * 0.75:
        return "Sınırda", "⚠️", "#f5a623"
    return "Düşük", "✅", "#26c281"


def render_single_result(
    output: pd.DataFrame,
    elapsed: float,
    threshold: float,
) -> None:
    row = output.iloc[0]
    probability = float(row["fraud_probability"])
    label, icon, color = risk_label(probability, threshold)
    decision = "İncelemeye gönder" if row["fraud_prediction"] else "Normal akış"
    cards = st.columns(4)
    values = [
        ("Karar", decision, "Sabit validation eşiğiyle"),
        ("Fraud olasılığı", f"%{probability * 100:.2f}", "Model skoru"),
        ("Risk seviyesi", f"{icon} {label}", "Arayüz segmentasyonu"),
        ("Toplam yanıt", f"{elapsed * 1000:.1f} ms", "FastAPI + model"),
    ]
    for column, (title, value, note) in zip(cards, values):
        column.markdown(
            f"""<div class="eco-card">
            <div class="eco-card-label">{title}</div>
            <div class="eco-card-value">{value}</div>
            <div class="eco-card-note">{note}</div></div>""",
            unsafe_allow_html=True,
        )

    probability_position = min(max(probability * 100, 1), 99)
    threshold_position = min(max(threshold * 100, 1), 99)
    st.markdown(
        f"""<div style="margin-top:3.4rem">
        <div class="eco-gauge">
          <div class="eco-gauge-label" style="left:{probability_position}%">
            %{probability * 100:.1f}
          </div>
          <div class="eco-gauge-marker" style="left:{probability_position}%"></div>
          <div class="eco-threshold" style="left:{threshold_position}%">
            ↑ Karar eşiği %{threshold * 100:.1f}
          </div>
        </div></div>""",
        unsafe_allow_html=True,
    )

    if probability >= threshold:
        background = "#391b20"
        title = "🔥 Manuel inceleme öneriliyor"
        text = (
            "İşlem model tarafından yüksek riskli işaretlendi. Otomatik ret yerine "
            "kimlik doğrulama, işlem bağlamı ve hesap geçmişi birlikte incelenmelidir."
        )
    else:
        background = "#123128"
        title = "✅ Normal akışta izlenebilir"
        text = (
            "İşlem sabit karar eşiğinin altında. Bu sonuç garanti değildir; rutin "
            "fraud izleme kuralları ve sonradan oluşan sinyaller uygulanmaya devam etmelidir."
        )
    st.markdown(
        f"""<div class="eco-action" style="background:{background};border-color:{color}">
        <h3>{title}</h3><p>{text}</p></div>""",
        unsafe_allow_html=True,
    )


def render_output_table(output: pd.DataFrame) -> None:
    st.dataframe(
        output.sort_values("fraud_probability", ascending=False),
        hide_index=True,
        use_container_width=True,
    )
    st.download_button(
        "Tahminleri CSV olarak indir",
        data=output.to_csv(index=False).encode("utf-8-sig"),
        file_name="ecoshield_predictions.csv",
        mime="text/csv",
        use_container_width=True,
    )


def run_prediction(raw_frame: pd.DataFrame, artifacts: dict[str, Any]) -> None:
    try:
        output, report, elapsed = predict_with_api(raw_frame)
        show_input_report(report)
        if report["missing_feature_count"] > 0:
            st.warning(
                "Eksik özellikler NaN/__MISSING__ olarak işlendi. "
                "Çok sayıda eksik özellik tahmin güvenilirliğini azaltabilir."
            )
    except Exception as error:
        st.exception(error)
        return

    st.session_state.last_output = output
    st.session_state.last_elapsed = elapsed
    st.session_state.last_record = (
        frame_to_api_records(raw_frame.iloc[[0]])[0]
        if len(raw_frame) == 1 else None
    )
    st.session_state.last_shap = None

    if len(output) == 1:
        render_single_result(output, elapsed, artifacts["threshold"])
    else:
        fraud_count = int(output["fraud_prediction"].sum())
        metrics = st.columns(4)
        metrics[0].metric("İşlenen", f"{len(output):,}")
        metrics[1].metric("Fraud tahmini", f"{fraud_count:,}")
        metrics[2].metric("Fraud oranı", f"%{100 * fraud_count / len(output):.2f}")
        metrics[3].metric("Tahmin süresi", f"{elapsed:.2f} sn")
    render_output_table(output)


def compute_shap_explanation(
    record: dict[str, Any],
    top_n: int,
) -> tuple[pd.DataFrame, float]:
    response = api_request(
        "POST",
        "/explain",
        json={"record": record, "top_n": top_n},
    )
    return pd.DataFrame(response["features"]), float(response["base_value"])


def render_explainability(artifacts: dict[str, Any]) -> None:
    st.subheader("🔎 Tahmin açıklanabilirliği")
    st.caption(
        "CatBoost SHAP katkıları son tek işlem tahmininde model skorunu hangi "
        "özelliklerin artırıp azalttığını gösterir. Değerler log-odds katkısıdır."
    )
    record = st.session_state.get("last_record")
    if record is None:
        st.info("Açıklama görmek için önce Tahmin sekmesinde tek işlem tahmini yapın.")
        return
    if st.session_state.get("last_shap") is None:
        with st.spinner("SHAP katkıları hesaplanıyor..."):
            st.session_state.last_shap = compute_shap_explanation(
                record,
                len(artifacts["feature_columns"]),
            )
    table, base_value = st.session_state.last_shap
    top = table.head(12).sort_values("shap_value")

    probability = float(
        st.session_state.last_output.iloc[0]["fraud_probability"]
    )
    summary = st.columns(3)
    summary[0].metric("Karar", st.session_state.last_output.iloc[0]["decision"])
    summary[1].metric("Fraud olasılığı", f"%{probability * 100:.2f}")
    summary[2].metric("SHAP base value", f"{base_value:.3f}")

    figure, axis = plt.subplots(figsize=(10, 5.5))
    figure.patch.set_facecolor("#0b1018")
    axis.set_facecolor("#151c2b")
    colors = np.where(top["shap_value"] >= 0, "#ff5349", "#36a3ff")
    axis.barh(top["feature"], top["shap_value"], color=colors)
    axis.axvline(0, color="#9facbf", linewidth=1)
    axis.tick_params(colors="#dce4f0")
    axis.set_xlabel("SHAP katkısı (log-odds)", color="#dce4f0")
    axis.set_title("En etkili 12 özellik", color="white", fontsize=15)
    for spine in axis.spines.values():
        spine.set_color("#2b3650")
    figure.tight_layout()
    st.pyplot(figure, use_container_width=True)
    plt.close(figure)

    st.subheader("🏆 En etkili 3 özellik")
    feature_cards = st.columns(3)
    for rank, (_, feature) in enumerate(table.head(3).iterrows(), start=1):
        direction_class = (
            "eco-feature-up" if feature["shap_value"] >= 0
            else "eco-feature-down"
        )
        feature_cards[rank - 1].markdown(
            f"""<div class="eco-card"><div class="eco-card-label">#{rank}</div>
            <div style="font-size:1.15rem;font-weight:750;margin:.35rem 0">
            {html.escape(str(feature['feature']))}</div>
            <div class="eco-card-note">Değer: {html.escape(str(feature['value']))}</div>
            <div class="{direction_class}">{feature['direction']} ·
            {feature['shap_value']:+.4f}</div></div>""",
            unsafe_allow_html=True,
        )
    with st.expander("Tüm feature katkıları"):
        st.dataframe(
            table[["feature", "value", "shap_value", "direction"]],
            hide_index=True,
            use_container_width=True,
        )


def render_performance_tab(artifacts: dict[str, Any]) -> None:
    if FINAL_METRICS_PATH.exists():
        metrics = pd.read_csv(FINAL_METRICS_PATH)
        selected = metrics.loc[
            metrics["approach"] == "PreselectedSingleHeavy"
        ]
        if not selected.empty:
            selected = selected.iloc[0]
            columns = st.columns(5)
            columns[0].metric("Precision", f"{selected['precision']:.4f}")
            columns[1].metric("Recall", f"{selected['recall']:.4f}")
            columns[2].metric("F1", f"{selected['f1']:.4f}")
            columns[3].metric("PR-AUC", f"{selected['pr_auc']:.4f}")
            columns[4].metric("ROC-AUC", f"{selected['roc_auc']:.4f}")
        st.dataframe(metrics, hide_index=True)
    else:
        st.info("Final test karşılaştırma dosyası bulunamadı.")

    figure_columns = st.columns(2)
    if CONFUSION_FIGURE_PATH.exists():
        figure_columns[0].image(
            str(CONFUSION_FIGURE_PATH),
            caption="Final test confusion matrisleri",
        )
    if CURVES_FIGURE_PATH.exists():
        figure_columns[1].image(
            str(CURVES_FIGURE_PATH),
            caption="Final test PR ve ROC eğrileri",
        )

    st.subheader("Model bilgisi")
    st.json({
        "model": "cat_d8_balanced",
        "threshold": artifacts["threshold"],
        "split_version": artifacts["selection"].get("split_version"),
        "preprocessing_profile": artifacts["selection"].get(
            "preprocessing_profile"
        ),
        "feature_count": len(artifacts["feature_columns"]),
        "model_path": str(MODEL_PATH.relative_to(PROJECT_ROOT)),
        "inference_api": artifacts["api_url"],
    })


try:
    runtime = load_runtime_artifacts()
except Exception as error:
    st.exception(error)
    st.stop()

example: dict[str, Any] = {}
if runtime["numeric_columns"]:
    example[runtime["numeric_columns"][0]] = 0.0
if runtime["categorical_columns"]:
    example[runtime["categorical_columns"][0]] = "__MISSING__"
default_single_payload = json.dumps(example, ensure_ascii=False, indent=2)
if "single_payload" not in st.session_state:
    st.session_state.single_payload = default_single_payload

demo_profiles: dict[str, dict[str, Any]] = {}
if runtime["test_cache_path"] is not None:
    demo_profiles = load_demo_profiles(
        str(runtime["test_cache_path"]),
        str(FINAL_PREDICTIONS_PATH),
        runtime["threshold"],
    )


def load_demo_payload(label: str) -> None:
    profile = demo_profiles[label]
    st.session_state.single_payload = json.dumps(
        profile["payload"],
        ensure_ascii=False,
        indent=2,
    )
    for key in ("last_output", "last_elapsed", "last_record", "last_shap"):
        st.session_state.pop(key, None)


def clear_session() -> None:
    st.session_state.single_payload = default_single_payload
    for key in ("last_output", "last_elapsed", "last_record", "last_shap"):
        st.session_state.pop(key, None)


with st.sidebar:
    st.header("🛡️ EcoShield AI")
    st.caption("IEEE-CIS Fraud Detection · Karar destek prototipi")
    st.divider()
    st.subheader("🟢 Sistem durumu")
    st.success("FastAPI bağlı · model hazır")
    st.caption(runtime["api_url"])
    st.write("**CatBoost D8 Balanced**")
    st.metric("Sabit threshold", f"{runtime['threshold']:.6f}")
    st.caption(
        "Threshold validation splitinde seçildi. "
        "Uygulama içinde yeniden ayarlanmaz."
    )
    st.divider()
    st.subheader("🎯 Örnek işlemler")
    if demo_profiles:
        st.caption("Final test cache'inden yalnızca arayüz demosu için seçildi.")
        for demo_label in demo_profiles:
            st.button(
                demo_label,
                key=f"demo_{demo_label}",
                on_click=load_demo_payload,
                args=(demo_label,),
                use_container_width=True,
            )
    else:
        st.caption("Demo cache dosyaları bulunamadı; JSON/CSV girişi kullanılabilir.")
    st.button(
        "🧹 Oturumu temizle",
        on_click=clear_session,
        use_container_width=True,
    )
    st.divider()
    st.caption(
        "Bu uygulama karar destek prototipidir. "
        "Tahminler otomatik finansal karar yerine inceleme sinyali olarak kullanılmalıdır."
    )
    st.caption("Arayüz sürümü: 3.0 · FastAPI serving")

st.markdown(
    """<div class="eco-hero">
    <h1>🛡️ EcoShield AI</h1>
    <p>İşlem verisini analiz et, fraud riskini ölç, kararı açıklanabilir sinyallerle incele.</p>
    </div>""",
    unsafe_allow_html=True,
)

single_tab, batch_tab, explain_tab, performance_tab = st.tabs([
    "🎯 Tahmin",
    "📂 Toplu CSV",
    "🔎 Açıklanabilirlik",
    "📊 Model & Mimari",
])

with single_tab:
    st.subheader("🧾 Tek işlem risk analizi")
    st.write(
        "Sol menüden gerçek bir demo işlemi seçebilir veya ortak şemaya uygun "
        "özellikleri JSON olarak girebilirsiniz."
    )
    payload = st.text_area(
        "İşlem özellikleri",
        key="single_payload",
        height=260,
    )
    with st.expander("423 özellikli ortak feature şeması"):
        st.write(runtime["feature_columns"])

    predict_clicked = st.button(
        "🤖 Fraud riskini tahmin et",
        type="primary",
        use_container_width=True,
    )

    if predict_clicked:
        try:
            parsed = json.loads(payload)
            if not isinstance(parsed, dict):
                raise TypeError("JSON girdisi tek bir nesne olmalıdır.")
            run_prediction(pd.DataFrame([parsed]), runtime)
        except Exception as error:
            st.exception(error)

with batch_tab:
    st.subheader("📂 CSV ile toplu fraud taraması")
    st.write(
        "Birleştirilmiş feature CSV'si yükleyebilir veya transaction ve identity "
        "dosyalarını ayrı vererek `TransactionID` üzerinden left join yaptırabilirsiniz."
    )
    transaction_file = st.file_uploader(
        "Transaction veya birleştirilmiş CSV",
        type=["csv"],
        key="transaction_csv",
    )
    identity_file = st.file_uploader(
        "Identity CSV — isteğe bağlı",
        type=["csv"],
        key="identity_csv",
    )
    if transaction_file is not None:
        try:
            transaction_frame = pd.read_csv(
                io.BytesIO(transaction_file.getvalue()),
                low_memory=False,
            )
            identity_frame = (
                pd.read_csv(
                    io.BytesIO(identity_file.getvalue()),
                    low_memory=False,
                )
                if identity_file is not None
                else None
            )
            merged_frame = merge_transaction_identity(
                transaction_frame,
                identity_frame,
            )
            st.write("Girdi önizlemesi")
            st.dataframe(merged_frame.head(20), hide_index=True)
            if st.button("Toplu tahmini başlat", type="primary"):
                run_prediction(merged_frame, runtime)
        except Exception as error:
            st.exception(error)

with explain_tab:
    render_explainability(runtime)

with performance_tab:
    st.subheader("📈 Final model performansı")
    st.caption(
        "Aşağıdaki sonuçlar daha önce kilitlenmiş test splitinde bir kez ölçülmüştür; "
        "uygulama threshold veya model seçimini yeniden yapmaz."
    )
    render_performance_tab(runtime)
    st.subheader("🏗️ Gerçek sistem mimarisi")
    st.code(
        """
Transaction CSV + Identity CSV
            │  TransactionID left join
            ▼
Streamlit kullanıcı arayüzü
            │  HTTP / JSON
            ▼
FastAPI inference servisi
            │  Feature şeması ve tip dönüşümleri
            ▼
CatBoost D8 Balanced + sabit threshold
            │
            ├── Fraud inceleme sinyali
            ├── Toplu CSV raporu
            └── CatBoost SHAP açıklaması
        """.strip(),
        language="text",
    )
    technology, rationale = st.columns(2)
    with technology:
        st.markdown("### 🔧 Teknolojiler")
        st.write(
            "Python · pandas · NumPy · scikit-learn · CatBoost · "
            "FastAPI · Streamlit · Docker · Matplotlib · Parquet"
        )
    with rationale:
        st.markdown("### 💡 Neden D8 Balanced?")
        st.write(
            "Validation'da seçilen tekil ağır model, final testte cascade yaklaşımdan "
            "daha yüksek PR-AUC ve ROC-AUC üretirken daha az false positive verdi."
        )
