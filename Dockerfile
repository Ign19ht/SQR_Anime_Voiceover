FROM python:3.11-alpine

# Install curl and other dependencies
RUN apk update && \
    apk add --no-cache curl py-pip

# # Install Poetry
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .

RUN poetry install

COPY secrets/ secrets/
COPY scripts/ scripts/

# Set a default command
CMD ["poetry", "run", "python", "scripts/main.py"]