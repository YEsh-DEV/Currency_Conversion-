# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . /app

# Expose port 8000 internally (docker-compose will map it to 8001 on host)
EXPOSE 8000

# Run the FastAPI app
# Using 0.0.0.0 to accept connections from outside container
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]