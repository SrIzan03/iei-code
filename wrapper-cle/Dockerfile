FROM python:3.13-slim

# # Set working directory
WORKDIR /wrapper-cle

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
EXPOSE 8001

# # Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]