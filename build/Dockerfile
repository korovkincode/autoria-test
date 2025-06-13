# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright & dependencies
RUN apt-get update && apt-get install -y curl && \
    apt-get install -y libglib2.0-0 libnss3 libatk-bridge2.0-0 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libxshmfence1 libxss1 libgtk-3-0 && \
    pip install playwright && playwright install --with-deps

# Copy project files
COPY . .

# Default command
CMD ["python", "scheduler.py"]