FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --force-reinstall -r requirements.txt
RUN pip install --no-cache-dir --upgrade --force-reinstall \
    setuptools==80.9.0 wheel==0.46.2 msgpack==1.2.2 jaraco.context==6.1.2

FROM python:3.11-slim
WORKDIR /app
RUN useradd -m myuser
RUN rm -rf /usr/local/lib/python3.11/site-packages/setuptools/_vendor/* \
    && rm -rf /usr/local/lib/python3.11/site-packages/*.dist-info
COPY --chown=myuser:myuser --from=builder /usr/local /usr/local
COPY --chown=myuser:myuser . .
USER myuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--reload"]

