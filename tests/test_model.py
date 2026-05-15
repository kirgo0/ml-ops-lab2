"""Unit-тести для скрипта тренування моделі."""
from pathlib import Path

import joblib

from ml.train import train_and_save


def test_train_creates_model_file(tmp_path: Path):
    """Перевіряє, що файл моделі створюється після тренування."""
    model_file = tmp_path / "model.joblib"
    accuracy = train_and_save(model_path=model_file)

    assert model_file.exists(), "Файл моделі має бути створений"
    assert 0.0 <= accuracy <= 1.0, "Accuracy має бути коректним числом у [0, 1]"
    assert accuracy > 0.8, f"Очікувано accuracy > 0.8, отримано {accuracy}"


def test_model_predicts_three_classes(tmp_path: Path):
    """Перевіряє, що модель повертає один із трьох допустимих класів."""
    model_file = tmp_path / "model.joblib"
    train_and_save(model_path=model_file)

    model = joblib.load(model_file)
    sample = [[5.1, 3.5, 1.4, 0.2]]  # типова setosa
    pred = model.predict(sample)

    assert pred[0] in (0, 1, 2), "Клас має бути одним із 0/1/2"


def test_model_predict_proba_sums_to_one(tmp_path: Path):
    """Перевіряє, що ймовірності класів у сумі дають 1."""
    model_file = tmp_path / "model.joblib"
    train_and_save(model_path=model_file)

    model = joblib.load(model_file)
    sample = [[6.3, 3.3, 4.7, 1.6]]  # типова versicolor
    proba = model.predict_proba(sample)[0]

    assert abs(sum(proba) - 1.0) < 1e-6, "Сума ймовірностей має дорівнювати 1"
    assert len(proba) == 3, "Модель має повертати ймовірності для 3 класів"
