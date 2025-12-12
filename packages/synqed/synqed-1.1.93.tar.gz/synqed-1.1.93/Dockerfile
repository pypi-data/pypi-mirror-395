FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy synqed source (make it importable via PYTHONPATH)
COPY src /app/src

# Copy application and MCP module
COPY main.py .
COPY synqed_mcp /app/synqed_mcp/

# Add src to PYTHONPATH so synqed can be imported
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# Copy .env if it exists (optional)
COPY .env* ./

# Create non-root user
RUN useradd -m -u 1000 synqed && \
    chown -R synqed:synqed /app

USER synqed

# Health check - use PORT env var
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, httpx; httpx.get(f'http://localhost:{os.getenv(\"PORT\", \"8080\")}/health', timeout=5)"

EXPOSE 8080

# Run unified server (email + MCP)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
