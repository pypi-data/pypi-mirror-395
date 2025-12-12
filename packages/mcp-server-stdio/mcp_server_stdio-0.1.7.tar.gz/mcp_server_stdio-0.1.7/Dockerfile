# -----------------------------
# 1. Builder Stage
# -----------------------------
    FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder

    WORKDIR /app
    
    # Copy project files
    COPY . .
    
    # Install dependencies into a folder
    RUN uv pip install --no-cache --target=/install fastmcp
    RUN uv pip install --no-cache --target=/install -r requirements.txt || true
    
    
    # -----------------------------
    # 2. Runtime Stage
    # -----------------------------
    FROM python:3.12-slim
    
    WORKDIR /app
    
    # Copy installed Python dependencies
    COPY --from=builder /install /usr/local/lib/python3.12/site-packages/
    
    # Copy project code
    COPY . .
    
    # Environment variables
    ENV PYTHONUNBUFFERED=1
    
    # Expose FastMCP port
    EXPOSE 8000
    
    # CMD using uv inside runtime
    CMD ["uv", "run", "python", "app/main.py"]
    