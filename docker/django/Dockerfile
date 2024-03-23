FROM python:3.12.2

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy only the dependencies file to optimize caching
COPY pyproject.toml poetry.lock /code/

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the application code
COPY ./core/ /code/

#Make script executable
RUN chmod +x start.dev.sh
## Make database migrations
#CMD poetry run python manage.py makemigrations
