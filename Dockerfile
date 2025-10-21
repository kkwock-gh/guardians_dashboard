# Use a lightweight official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for pyarrow and others
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the Streamlit default port
EXPOSE 8502

# Streamlit configuration (disables telemetry and headless errors)
ENV STREAMLIT_HOME=/app
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]

