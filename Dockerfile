# Use an official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first, for efficient docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Ensure the media directory exists
RUN mkdir -p /app/media

# Expose API port (not strictly required for compose)
EXPOSE 8000

# Default command: just show help (compose sets actual command!)
CMD ["bash"]
