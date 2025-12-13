FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (including README.md required by pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Copy package directories needed for installation
COPY wistx_mcp/ ./wistx_mcp/
COPY data_pipelines/ ./data_pipelines/

# Install dependencies (this will install the project including wistx_mcp)
RUN uv sync --frozen

# Copy application code
COPY api/ ./api/

# Make startup script executable
RUN chmod +x api/start.sh

# Expose port
# Note: EXPOSE is documentation only. The actual port is controlled by PORT env var.
# Cloud Run sets PORT=8080 (matches container_port in Terraform).
# For local dev, PORT defaults to 8000 in start.sh if not set.
EXPOSE 8080

# Run application using startup script
CMD ["./api/start.sh"]
