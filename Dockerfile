FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

WORKDIR /app

# Copy the uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Optimize uv for Docker environment
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install runtime dependencies
COPY pyproject.toml uv.lock* /app/
    
RUN uv sync --frozen --no-dev

# Copy application code
COPY main.py /app/main.py
COPY src /app/src
RUN mkdir /output

# Default output path inside the container
ENV OUTPUT_PATH=/output

CMD ["uv", "run", "python", "main.py"]

