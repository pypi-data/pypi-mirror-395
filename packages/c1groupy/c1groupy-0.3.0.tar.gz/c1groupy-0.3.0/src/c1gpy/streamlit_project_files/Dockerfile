FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy only dependency files first
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv pip install --system -e .

# use multi stage for smaller image size
FROM python:3.12-slim

LABEL author="{author_email}"

WORKDIR /app

# Copy uv and installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/
COPY tests/ ./tests/

# Change ownership of src and tests to appuser
RUN chown -R appuser:appuser /app/src /app/tests

# Make entrypoint executable
RUN chmod +x /app/src/entrypoint.sh

# Switch to non-root user
USER appuser

# Set default environment variables
ENV LOCALRUN=FALSE
ENV PYTEST=FALSE

#needs $PORT $LOCALRUN $PYTEST
ENTRYPOINT ["/app/src/entrypoint.sh"]
