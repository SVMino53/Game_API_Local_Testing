# Base image with Python 3.12
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy rest of code
COPY . .

# Port used by the application
EXPOSE 5000

# Start application
CMD ["python", "main.py"]