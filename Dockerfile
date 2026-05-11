# Lightweight Python runtime
FROM python:3.10-slim

# Environment triggers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies for handling PDF processing libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency configurations
COPY requirements.txt .

# Install python tools
RUN pip install --no-cache-dir -r requirements.txt

# Copy standard distribution layers
COPY . .

# Expose internal streamlit comms
EXPOSE 8501

# Global runtime healthchecks
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Boot command
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
