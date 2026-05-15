"""Pydantic-моделі для валідації вхідних та вихідних даних API."""
from pydantic import BaseModel, Field


class IrisFeatures(BaseModel):
    """Вхідні ознаки квітки Iris (4 виміри у сантиметрах)."""

    sepal_length: float = Field(..., ge=0, le=10, description="Довжина чашолистка, см")
    sepal_width: float = Field(..., ge=0, le=10, description="Ширина чашолистка, см")
    petal_length: float = Field(..., ge=0, le=10, description="Довжина пелюстки, см")
    petal_width: float = Field(..., ge=0, le=10, description="Ширина пелюстки, см")

    model_config = {
        "json_schema_extra": {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            }
        }
    }


class PredictionResponse(BaseModel):
    """Відповідь API з результатом передбачення."""

    class_id: int = Field(..., description="ID класу (0, 1 або 2)")
    class_name: str = Field(..., description="Назва класу (setosa/versicolor/virginica)")
    probability: float = Field(..., ge=0, le=1, description="Ймовірність належності до класу")
