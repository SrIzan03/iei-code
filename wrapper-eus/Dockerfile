FROM python:3.13-slim

# # Set working directory
WORKDIR /wrapper-eus

# Install dependencies for PowerShell
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    apt-transport-https \
    software-properties-common \
    gnupg \
    && wget -q https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && dpkg --add-architecture amd64 \
    && apt-get update \
    && apt-get install -y --no-install-recommends powershell \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# # Install Poetry
RUN pip install poetry

# # Copy poetry files
COPY pyproject.toml poetry.lock ./

# # Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# # Install dependencies
RUN poetry install --only main

# # Copy application code
COPY . .

# # Expose port
EXPOSE 8003

# # Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]