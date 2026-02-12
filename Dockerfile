FROM ghcr.io/astral-sh/uv:python3.12-trixie

# Required for i8n
RUN apt-get update && apt-get install -y gettext

# Set working directory to main app
WORKDIR /app/

# Copy application code into image
# (Excludes any files/dirs matched by patterns in .dockerignore)
COPY . /app/

# Install dependencies
RUN uv sync

# Collect and compress static files
RUN uv run manage.py collectstatic --no-input