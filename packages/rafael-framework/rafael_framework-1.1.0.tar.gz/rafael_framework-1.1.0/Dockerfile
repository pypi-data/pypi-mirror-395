# RAFAEL Framework Docker Image
# Multi-stage build for optimal size

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY setup.py .
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .

# Copy source code
COPY core/ ./core/
COPY chaos_forge/ ./chaos_forge/
COPY vault/ ./vault/
COPY guardian/ ./guardian/
COPY devkit/ ./devkit/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/rafael /usr/local/bin/rafael

# Copy application code
COPY core/ ./core/
COPY chaos_forge/ ./chaos_forge/
COPY vault/ ./vault/
COPY guardian/ ./guardian/
COPY devkit/ ./devkit/
COPY examples/ ./examples/
COPY docs/ ./docs/
COPY README.md LICENSE ./

# Create non-root user
RUN useradd -m -u 1000 rafael && \
    chown -R rafael:rafael /app

USER rafael

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import core; print('healthy')" || exit 1

# Expose dashboard port
EXPOSE 8080

# Default command: start dashboard
CMD ["rafael", "dashboard", "--port", "8080"]
