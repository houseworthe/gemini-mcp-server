# Multi-stage build for smaller final image
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Create non-root user
RUN useradd -m -u 1000 mcp && \
    mkdir -p /app && \
    chown -R mcp:mcp /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/mcp/.local

# Set working directory
WORKDIR /app

# Copy application files
COPY --chown=mcp:mcp server.py .
COPY --chown=mcp:mcp requirements.txt .

# Switch to non-root user
USER mcp

# Update PATH
ENV PATH=/home/mcp/.local/bin:$PATH

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Expose the MCP server port (if applicable)
# EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import server; print('healthy')" || exit 1

# Run the server
CMD ["python", "server.py"]