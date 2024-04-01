# uvicorn main:app --reload
# uvicorn main:app --proxy-headers --host 0.0.0.0

pip install poetry

poetry install --no-root

poetry run uvicorn main:app --host 0.0.0.0