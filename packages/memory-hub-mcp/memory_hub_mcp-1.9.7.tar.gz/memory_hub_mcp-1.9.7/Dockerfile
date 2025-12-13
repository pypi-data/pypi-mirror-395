# Multi-stage build for smaller production image
FROM python:3.11-slim as builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files first (for Docker layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies in virtual environment (include dev deps for uvicorn)
RUN uv sync --frozen

# Production stage
FROM python:3.11-slim as production

# Install uv in production stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install security updates, curl for health checks, and clean up
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user for security with home directory
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code and project files
COPY . .

# Create cache directory and set ownership
RUN mkdir -p /home/appuser/.cache/uv && \
    chown -R appuser:appuser /app /home/appuser

# Switch to non-root user
USER appuser

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application using uv run (proper virtual environment activation)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 