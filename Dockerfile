FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    ECOSHIELD_PROJECT_ROOT=/app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system ecoshield \
    && useradd --system --gid ecoshield --create-home ecoshield

COPY requirements-runtime.txt ./requirements-runtime.txt
RUN pip install --upgrade pip \
    && pip install -r requirements-runtime.txt

COPY api ./api
COPY notebooks/streamlit_app.py ./notebooks/streamlit_app.py

RUN chown -R ecoshield:ecoshield /app
USER ecoshield

EXPOSE 8000 8501

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
