FROM python:3.11-slim

WORKDIR /app

COPY . .
COPY requirements-google.txt .
RUN pip install -r requirements-google.txt

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
