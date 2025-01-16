FROM python:3.13-slim

# # Install Chrome and required dependencies
RUN apt-get update && apt-get install -y

# # Set working directory
WORKDIR /app

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

# # Set environment variables
ENV DB_NAME=postgres
ENV DB_USER=root
ENV DB_PASSWORD=root
ENV DB_HOST=db
ENV DB_PORT=5432

# # Expose port
EXPOSE 8080

# # Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]