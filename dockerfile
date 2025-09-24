# Dockerfile
FROM python:3.13-slim

# Install system dependencies for WeasyPrint
COPY apt.txt .
RUN xargs -a apt.txt apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set port and start gunicorn
ENV PORT=8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
