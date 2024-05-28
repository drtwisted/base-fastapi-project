########################
# BASE IMAGE
########################
FROM bitnami/python:3.11.9-debian-12-r9 as base

ARG UID
ARG GID
ARG USER_NAME


ENV UID=${UID} \
    GID=${GID} \
    USER_HOME=/home/${USER_NAME}/app \
    USER_NAME=${USER_NAME} \
    VIRTUAL_ENV=/opt/venv

ENV PATH="${VIRTUAL_ENV}/bin:${PATH}}"

RUN apt update \ 
    && apt install -y sudo \
    && addgroup --gid ${GID} ${USER_NAME} \
    && adduser --uid ${UID} --gid ${GID} --disabled-password --gecos "" ${USER_NAME} \
    && echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER ${USER_NAME}
WORKDIR ${USER_HOME}


########################
# BUILDER IMAGE
########################
FROM base as builder

ARG POETRY_VERSION
ARG BUILD_TARGET
ENV POETRY_VERSION=${POETRY_VERSION} \
    BUILD_TARGET=${BUILD_TARGET}

RUN sudo mkdir ${VIRTUAL_ENV}
RUN sudo chown ${UID}:${GID} ${VIRTUAL_ENV}

RUN python -m venv ${VIRTUAL_ENV}

RUN pip install poetry==${POETRY_VERSION}
COPY pyproject.toml poetry.lock ./

RUN if [[ "$BUILD_TARGET" == "dev" ]]; then \
    poetry --no-cache install --with=dev --no-root; \
else \
    poetry --no-cache install --without=dev --no-root; \
fi

########################
# BACKEND IMAGE
########################
FROM builder as backend

ARG APP_PORT
ENV APP_PORT=${APP_PORT}

COPY ./src .

CMD [ "sh", "-c", "python -m uvicorn app:app --host 0.0.0.0 --port ${APP_PORT} --reload" ]
