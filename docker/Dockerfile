FROM python:3.9-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN useradd -m myuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
RUN useradd -m myuser
COPY --chown=myuser:myuser --from=builder /usr/local /usr/local
COPY --chown=myuser:myuser . .
USER myuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--reload"]