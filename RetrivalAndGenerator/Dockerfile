FROM --platform=linux/amd64 python:3.10

# Set working directory
WORKDIR /app

# Install base dependencies first (rarely changes = cache hit)
COPY requirements-base.txt .
RUN pip install -r requirements-base.txt

# Install changing dependencies (invalidates cache only if this changes)
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# Make model directory
RUN mkdir -p /app/models

# Download model at build time and save locally
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
SentenceTransformer('all-MiniLM-L12-v2').save('./models/all-MiniLM-L12-v2')"

# Download LLaMA 1.1B GGUF model
RUN apt-get update && apt-get install -y wget \
 && wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q6_K.gguf \
 -O /app/models/tinyllama-1.1b-chat-v1.0.Q6_K.gguf


# Copy all remaining code
COPY . .

# Run the application
CMD ["python", "app.py"]