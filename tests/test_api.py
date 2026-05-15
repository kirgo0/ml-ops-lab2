"""Інтеграційні тести для FastAPI ендпоінтів."""
import pytest
from fastapi.testclient import TestClient

from ml.train import train_and_save
from app.main import app, MODEL_PATH

# Гарантуємо існування файлу моделі перед запуском API-тестів
if not MODEL_PATH.exists():
    train_and_save(MODEL_PATH)


@pytest.fixture(scope="module")
def client():
    """TestClient як context manager — викликає lifespan-події (startup/shutdown)."""
    with TestClient(app) as c:
        yield c


def test_root_endpoint(client):
    """GET / повертає 200 та коректний статус."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_endpoint(client):
    """GET /health повертає 200 та підтверджує завантаження моделі."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["model_loaded"] is True


def test_predict_setosa(client):
    """POST /predict з типовими ознаками setosa повертає клас setosa."""
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["class_name"] == "setosa"
    assert body["class_id"] == 0
    assert 0.0 <= body["probability"] <= 1.0


def test_predict_virginica(client):
    """POST /predict з типовими ознаками virginica повертає правильний клас."""
    payload = {
        "sepal_length": 6.7,
        "sepal_width": 3.0,
        "petal_length": 5.2,
        "petal_width": 2.3,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["class_name"] == "virginica"
    assert body["class_id"] == 2


def test_predict_invalid_input(client):
    """POST /predict з некоректним типом повертає 422."""
    payload = {"sepal_length": "not-a-number"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Pydantic validation error


def test_predict_out_of_range(client):
    """POST /predict зі значеннями поза допустимим діапазоном повертає 422."""
    payload = {
        "sepal_length": 999,  # > 10, недопустимо
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
