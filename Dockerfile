#Arguement Declaration
ARG docker_registry

#Stage 1
FROM python:3.10-slim as requirements-stage
WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN apt-get update && \
    apt-get install -y git && \
    pip install poetry && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

# Final stage
FROM ${docker_registry}/spark:latest
ARG spark_uid=185
ARG private_repo_username
ARG private_repo_token
ARG github_username
ARG github_token
USER ${spark_uid}
WORKDIR /copyscenario
COPY --from=requirements-stage /tmp/requirements.txt .
RUN git config --global credential.helper store && \
    echo "https://$github_username:$github_token@github.com" >> $HOME/.git-credentials && \
    echo "https://$private_repo_username:$private_repo_token@gitlab.com" >> $HOME/.git-credentials && \
    pip install --no-cache-dir --upgrade -r /copyscenario/requirements.txt && \
    rm -rf ${HOME}/.git-credentials

COPY . .
CMD ["python3", "main.py"]
