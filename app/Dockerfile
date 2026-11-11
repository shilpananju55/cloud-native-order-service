FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app

# Create a non-privileged system user
RUN useradd -m -u 10001 appuser

# Copy installed python dependencies from builder
COPY --from=builder /install /usr/local
COPY main.py .

# Update system packages to patch known high/critical CVEs in the base image
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]