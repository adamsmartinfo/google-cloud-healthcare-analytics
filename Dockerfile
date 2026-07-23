FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "streamlit run app/app.py --server.address=0.0.0.0 --server.port=${PORT:-8080} --server.headless=true"]
