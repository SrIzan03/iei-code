FROM python:3.13-slim

RUN apt-get update && apt-get install -y chromium && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Chrome Driver
# COPY chromedriver-linux64 /chromedriver-linux64
# Set working directory
WORKDIR /iei-bot

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
