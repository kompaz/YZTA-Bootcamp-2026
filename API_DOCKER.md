# EcoShield AI — FastAPI ve Docker Kullanımı

## Gerekli yerel dosyalar

Servisleri başlatmadan önce aşağıdaki dosyaların mevcut olması gerekir:

```text
models/heavy/optimized_single_heavy_model.joblib
outputs/metrics/selected_single_heavy_model.csv
outputs/metadata/common_cache_manifest.json
outputs/metadata/common_feature_schema.json
```

Model dosyası 100 MB sınırını aştığı için GitHub'a eklenmez. Görev 6 notebook'u
çalıştırılarak yerel olarak oluşturulur.

## Docker Compose ile çalıştırma

Repository kökünde:

```bash
docker compose up --build
```

Servisler:

- Streamlit: <http://localhost:8501>
- FastAPI dokümantasyonu: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health>

Durdurmak için:

```bash
docker compose down
```

## Docker kullanmadan yerel çalıştırma

Birinci terminal:

```bash
conda activate torchcuda
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

İkinci terminal:

```bash
conda activate torchcuda
python -m streamlit run notebooks/streamlit_app.py
```

## API sözleşmesi

```text
GET  /health
GET  /model-info
POST /predict
POST /explain
```

Örnek tahmin isteği:

```json
{
  "records": [
    {
      "TransactionID": 100001,
      "TransactionAmt": 249.90,
      "ProductCD": "W"
    }
  ]
}
```

API, eksik feature'ları eğitimde kullanılan şemaya göre `NaN` veya
`__MISSING__` olarak tamamlar. Threshold sunucu tarafında sabittir ve test
sonucuna göre değiştirilmez.
