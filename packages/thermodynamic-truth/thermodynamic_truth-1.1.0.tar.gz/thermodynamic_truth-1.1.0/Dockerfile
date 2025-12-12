# ThermoTruth Protocol - Production Docker Image
FROM python:3.11-slim

LABEL maintainer="ThermoTruth Initiative <info@thermodynamic-truth.org>"
LABEL description="Thermodynamic Consensus Protocol - Byzantine Fault Tolerant consensus"
LABEL version="0.1.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app user
RUN useradd -m -u 1000 thermo && \
    mkdir -p /app && \
    chown -R thermo:thermo /app

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
        && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY --chown=thermo:thermo requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY --chown=thermo:thermo src/ ./src/
COPY --chown=thermo:thermo setup.py pyproject.toml README.md LICENSE ./

# Install the package
RUN pip install --no-cache-dir -e .

# Switch to non-root user
USER thermo

# Expose default gRPC port
EXPOSE 50051

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import grpc; channel = grpc.insecure_channel('localhost:50051'); channel.close()" || exit 1

# Default command: run node
ENTRYPOINT ["python", "-m", "thermodynamic_truth.cli.node"]
CMD ["--help"]
