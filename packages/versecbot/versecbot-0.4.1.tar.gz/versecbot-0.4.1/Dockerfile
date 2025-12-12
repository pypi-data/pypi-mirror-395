FROM python:3.13-slim

# Use Bash as shell
SHELL ["/bin/bash", "-c"]

# silence Dialog TERM not set errors in apt-get install
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git

# Set Containerized environment variable for conditional behavior in application
ENV IS_CONTAINER=true

# Set context for entrypoint
WORKDIR /app

# Copy application files
COPY ./pyproject.toml /app/pyproject.toml
COPY ./README.md /app/README.md
COPY ./LICENSE.md /app/LICENSE.md
COPY ./src/versecbot /app/versecbot
COPY ./src/start.sh /app/start.sh

# Install all Python requirements
RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --ignore-installed .

# Set metadata as specified by https://github.com/opencontainers/image-spec/blob/main/annotations.md
ARG BUILD_TIMESTAMP="unknown"
ARG BUILD_VERSION="unknown"

LABEL org.opencontainers.image.created="${BUILD_TIMESTAMP}"
LABEL org.opencontainers.image.authors="Museus <versecbot@museus.dev>"
LABEL org.opencontainers.image.url=""
LABEL org.opencontainers.image.documentation=""
LABEL org.opencontainers.image.source="https://github.com/Museus/VerSecBot"
LABEL org.opencontainers.image.version="${BUILD_VERSION}"
LABEL org.opencontainers.image.vendor="Museus"
LABEL org.opencontainers.image.title="VerSecBot"
LABEL org.opencontainers.image.description="An extendable Discord Bot to manage common moderation tasks."

ENTRYPOINT ["bash", "-c", "./start.sh"]