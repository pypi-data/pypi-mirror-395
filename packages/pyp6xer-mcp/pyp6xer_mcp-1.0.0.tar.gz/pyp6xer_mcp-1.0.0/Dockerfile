FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package
COPY pyp6xer_mcp/ pyp6xer_mcp/

# Expose port
EXPOSE 5000

# Run server with streamable-http transport
CMD ["python", "-m", "pyp6xer_mcp.cli", "streamable-http"]
