FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
