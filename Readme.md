# Iris ML API — Лабораторна робота №2 (CI/CD та ML API)

[![CI](https://github.com/YOUR_USERNAME/ml-api-lab2/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/ml-api-lab2/actions/workflows/ci.yml)

> ⚠️ Замініть `YOUR_USERNAME` у бейджі вище на ваш GitHub-нікнейм після створення репозиторію.

## Опис проєкту

Навчальний MLOps-проєкт, що демонструє повний наскрізний конвеєр:
від тренування ML-моделі до публічного REST API, розгорнутого у хмарі.
Модель класифікації квіток **Iris** (LogisticRegression з scikit-learn) обгорнута
у FastAPI-сервіс, контейнеризована за допомогою Docker, покрита тестами,
автоматизована через GitHub Actions та розгорнута на платформі Render.

**Ключові ендпоінти:**
- `GET /` — статус сервісу
- `GET /health` — liveness probe
- `POST /predict` — інференс моделі (приймає 4 ознаки, повертає клас та ймовірність)
- `GET /docs` — автоматично згенерована Swagger UI документація

## Стек технологій

| Категорія | Інструмент |
|-----------|------------|
| Мова | Python 3.11 |
| ML-фреймворк | scikit-learn 1.5.2 |
| Серіалізація моделі | joblib |
| Web-фреймворк | FastAPI 0.115 |
| ASGI-сервер | Uvicorn |
| Валідація даних | Pydantic v2 |
| Тестування | pytest, httpx (TestClient) |
| Контейнеризація | Docker |
| CI/CD | GitHub Actions |
| Хостинг | Render (PaaS) |

## Структура репозиторію

```
ml-api-lab2/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions workflow
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI застосунок (ендпоінти)
│   └── schemas.py              # Pydantic-моделі вхід/вихід
├── ml/
│   ├── __init__.py
│   └── train.py                # Скрипт тренування Iris
├── tests/
│   ├── __init__.py
│   ├── test_api.py             # Інтеграційні тести API
│   └── test_model.py           # Unit-тести моделі
├── .dockerignore
├── .gitignore
├── Dockerfile                  # Збірка Docker-образу
├── README.md                   # Цей файл
└── requirements.txt            # Залежності Python
```

---

## Послідовний запуск проєкту

### Етап 1. Ініціалізація репозиторію

```bash
# 1. Створіть публічний репозиторій на github.com (наприклад, "ml-api-lab2")
# 2. Склонуйте його локально
git clone https://github.com/kirgo0/ml-ops-lab2.git
cd ml-api-lab2

# 3. Скопіюйте у цей каталог усі файли проєкту
```

### Етап 2. Локальне середовище

```bash
# Створення віртуального оточення
python -3.11 -m venv .venv

# Активація: Linux/macOS
source .venv/bin/activate

# Активація: Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Встановлення залежностей
pip install --upgrade pip
pip install -r requirements.txt
```

### Етап 3. Тренування моделі

```bash
python -m ml.train
```

**Очікуваний вивід:**
```
Model trained. Test accuracy: 0.9667
Saved to: /path/to/ml-api-lab2/model.joblib
```

Файл `model.joblib` з'явиться у корені проєкту — це артефакт, який буде використовувати API.

### Етап 4. Запуск API локально

```bash
uvicorn app.main:app --reload
```

Сервіс буде доступний за адресою:
- API: <http://localhost:8000>
- **Swagger UI**: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

**Тестовий запит через curl:**
```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

**Очікувана відповідь:**
```json
{"class_id":0,"class_name":"setosa","probability":0.9784}
```

**Перевірка стану сервісу:**
```bash
curl http://localhost:8000/health
# {"status":"healthy","model_loaded":true}
```

### Етап 5. Запуск тестів

```bash
pytest -q
```

**Очікуваний вивід:**
```
.........                              [100%]
9 passed in 1.85s
```

Тести покривають:
- **test_model.py** (3 тести): створення файлу моделі, передбачення коректних класів, сума ймовірностей = 1.
- **test_api.py** (6 тестів): ендпоінти `/`, `/health`, `/predict` (setosa, virginica), валідація типу та діапазонів.

### Етап 6. Запуск через Docker

```bash
# Збірка образу (модель тренується автоматично під час білду)
docker build -t ml-api:lab2 .

# Запуск контейнера
docker run --rm -p 8000:8000 ml-api:lab2

# В іншому терміналі — перевірка
curl http://localhost:8000/health
```

Зупинити контейнер: `Ctrl+C`.

### Етап 7. Налаштування CI (GitHub Actions)

1. Переконайтеся, що файл `.github/workflows/ci.yml` присутній у репозиторії.
2. Закомітьте та запуште зміни:
   ```bash
   git add .
   git commit -m "Initial ML API project with CI"
   git push origin main
   ```
3. Перейдіть у вкладку **Actions** репозиторію на GitHub.
4. Дочекайтеся завершення workflow (~2–3 хвилини при першому запуску).
5. При зеленому статусі — workflow готовий, бейдж у README автоматично почне відображати статус.

**Що робить CI:**
- **Job `test`**: піднімає Python 3.11 → встановлює залежності → тренує модель → запускає `pytest`.
- **Job `docker-build`**: після успіху тестів збирає Docker-образ для перевірки коректності Dockerfile.

### Етап 8. Деплой на Render

1. Зареєструйтеся на <https://render.com> через ваш GitHub-акаунт.
2. На дашборді натисніть **New** → **Web Service**.
3. Виберіть ваш репозиторій `ml-api-lab2` (можливо, доведеться надати Render доступ).
4. Налаштування:
   - **Name**: `ml-api-<your-name>` (наприклад, `ml-api-ivan`)
   - **Region**: найближчий до вас (наприклад, Frankfurt)
   - **Branch**: `main`
   - **Runtime / Environment**: `Docker` (Render автоматично знайде `Dockerfile`)
   - **Instance Type**: `Free`
5. Натисніть **Create Web Service**. Білд триватиме ~5–7 хвилин при першому запуску.
6. Після завершення Render видасть публічний URL вигляду:
   ```
   https://ml-api-<your-name>.onrender.com
   ```

**Перевірка розгорнутого сервісу:**
```bash
# Liveness probe
curl https://ml-api-<your-name>.onrender.com/health

# Передбачення
curl -X POST https://ml-api-<your-name>.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":6.7,"sepal_width":3.0,"petal_length":5.2,"petal_width":2.3}'
```

Або через браузер — `https://ml-api-<your-name>.onrender.com/docs` (інтерактивний Swagger UI).

> 💡 **Примітка:** На безкоштовному тарифі Render сервіс «засинає» після ~15 хвилин відсутності трафіку.
> Перший запит після сну може займати 30–60 секунд (cold start) — це нормально.

---

## Як працює API

### Pydantic-схема запиту (`IrisFeatures`)

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Усі чотири поля — `float` у діапазоні `[0, 10]` см. Pydantic автоматично:
- відхиляє запити з невірним типом (повертає `422 Unprocessable Entity`),
- відхиляє значення поза межами `[0, 10]`,
- генерує OpenAPI-схему для Swagger UI.

### Pydantic-схема відповіді (`PredictionResponse`)

```json
{
  "class_id": 0,
  "class_name": "setosa",
  "probability": 0.9784
}
```

| Поле | Тип | Опис |
|------|-----|------|
| `class_id` | `int` | 0, 1 або 2 |
| `class_name` | `str` | `setosa`, `versicolor` або `virginica` |
| `probability` | `float` | Ймовірність класу (округлена до 4 знаків) |

### Коди відповідей

| Код | Випадок |
|-----|---------|
| `200` | Успішне передбачення |
| `422` | Помилка валідації (неправильний тип / діапазон) |
| `503` | Модель не завантажена (внутрішня помилка сервера) |

---

## Посилання

- **Репозиторій GitHub**: `https://github.com/YOUR_USERNAME/ml-api-lab2`
- **Розгорнутий сервіс на Render**: `https://ml-api-<your-name>.onrender.com`
- **Swagger UI (інтерактивна документація)**: `https://ml-api-<your-name>.onrender.com/docs`
- **GitHub Actions (статус CI)**: `https://github.com/YOUR_USERNAME/ml-api-lab2/actions`

---

## Часті помилки та як їх виправити

| Проблема | Причина | Рішення |
|----------|---------|---------|
| `FileNotFoundError: model.joblib` при старті API | Модель не натренована | Виконати `python -m ml.train` |
| `ImportError: attempted relative import...` | Запуск файлу `main.py` напряму | Запускати через `uvicorn app.main:app` |
| `ModuleNotFoundError: No module named 'app'` у тестах | Запуск з невірного каталогу | Запускати `pytest` з кореня проєкту |
| CI падає на кроці `pytest` | Локально працює, але CI ні — забуто `python -m ml.train` у workflow | Перевірити, що крок `Train model` присутній перед `Run pytest` |
| Render показує `Failed to build` | Помилка у Dockerfile | Перевірити локально: `docker build -t test .` |
| Перший запит до Render займає 30+ секунд | Cold start на безкоштовному тарифі | Це нормально для free-плану |

---

## Автор

Лабораторну роботу виконано у рамках курсу **MLOps**.
