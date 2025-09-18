# Use Python 3.11 base image
FROM --platform=linux/amd64 python:3.11

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your processing script
COPY . .

# Run the script
CMD ["python", "app.py"]
