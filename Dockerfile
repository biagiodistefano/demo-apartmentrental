# ------ base stage ------

FROM python:3.12.1-slim-bullseye as base-image

# emvironment variables shared by both the compile and final image
ENV WORKDIR=/apartmentrentals \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # Inspired by https://pythonspeed.com/articles/multi-stage-docker-python/
    # and https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
    VIRTUAL_ENV=/opt/venv

ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV ACCEPT_EULA=Y

RUN apt-get update

# ------ Compile stage ------
# This stage has installed additional dependencies not are required in the final image

FROM base-image as compile-image

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1

# DB deps: maybe??
# RUN apt-get install python3-dev default-libmysqlclient-dev build-essential

# System deps:
RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

# Create a virtual env.
# Inspired by https://pythonspeed.com/articles/multi-stage-docker-python/
# and https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
RUN python -m venv $VIRTUAL_ENV

# Copy only requirements to cache them in docker layer
WORKDIR ${WORKDIR}
COPY poetry.lock pyproject.toml README.md ${WORKDIR}/

# Copy source code of the project:
COPY src ${WORKDIR}/src

# install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi --no-root \
    && python -m compileall $(python -c 'import site; print(site.getsitepackages()[0])')

# ------ Final stage ------
FROM base-image as final-image

# Install system deps:
RUN apt-get update \
    && apt-get install -y dumb-init --no-install-recommends \
    && apt-get install -y make --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get -y install curl

WORKDIR ${WORKDIR}

# copy virtual env from the compile stage
COPY --from=compile-image $VIRTUAL_ENV $VIRTUAL_ENV

# Copy source code of the project:
COPY --from=compile-image $WORKDIR $WORKDIR

WORKDIR ${WORKDIR}/src

VOLUME ${WORKDIR}/media

RUN mkdir -p /apartmentrentals/src/media && chown -R nobody:nogroup /apartmentrentals/src/media

EXPOSE 8000
USER nobody

# https://github.com/Yelp/dumb-init
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
