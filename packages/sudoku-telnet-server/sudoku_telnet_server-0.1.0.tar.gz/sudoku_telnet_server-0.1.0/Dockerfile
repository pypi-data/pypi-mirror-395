# Dockerfile for Sudoku Telnet Server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml /app/
COPY src/ /app/src/
COPY config.yaml /app/

# Install the package with dependencies
RUN pip install --no-cache-dir -e .

# Expose ports for all transports
# 8023: Telnet
# 8024: TCP
# 8025: WebSocket
# 8026: WebSocket-Telnet
EXPOSE 8023 8024 8025 8026

# Set Python path to include current directory
ENV PYTHONPATH=/app

# Health check on telnet port
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import socket; s = socket.socket(); s.connect(('localhost', 8023)); s.close()" || exit 1

# Run the server using chuk-protocol-server launcher
CMD ["chuk-protocol-server", "server-launcher", "-c", "config.yaml"]
