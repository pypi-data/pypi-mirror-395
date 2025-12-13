FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files and metadata files (required by pyproject.toml)
COPY pyproject.toml uv.lock LICENSE README.md ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY medical_mcps/ ./medical_mcps/

# Expose port
EXPOSE 8000

# Set environment variables
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000
ENV PYTHONUNBUFFERED=1

# Run the server
CMD ["uv", "run", "medical-mcps"]

