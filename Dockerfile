FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Expose port (use Railway's PORT variable)
EXPOSE ${PORT:-8000}

# Run - use PORT env var from Railway
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
