"""Веб-сервіс для інференсу моделі Iris."""
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException

from .schemas import IrisFeatures, PredictionResponse

MODEL_PATH = Path(__file__).resolve().parent.parent / "model.joblib"
CLASS_NAMES = ["setosa", "versicolor", "virginica"]

# Глобальна змінна для моделі — завантажується один раз при старті
model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan-хук: завантажує модель при старті сервера."""
    global model
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model file not found: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    yield
    # Cleanup при зупинці сервера (за потреби)
    model = None


app = FastAPI(
    title="Iris ML API",
    description="REST API для класифікації квіток Iris на основі моделі LogisticRegression",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict:
    """Кореневий ендпоінт для перевірки доступності сервісу."""
    return {"status": "ok", "service": "Iris ML API"}


@app.get("/health")
def health() -> dict:
    """Liveness probe — перевірка стану сервісу та моделі."""
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: IrisFeatures) -> PredictionResponse:
    """Виконує інференс моделі для одного прикладу."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    x = np.array([[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]])

    class_id = int(model.predict(x)[0])
    proba = float(model.predict_proba(x)[0, class_id])

    return PredictionResponse(
        class_id=class_id,
        class_name=CLASS_NAMES[class_id],
        probability=round(proba, 4),
    )
