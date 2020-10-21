FROM python:3.7-alpine


LABEL name="black-isort-suggestions"
LABEL version="1.0.0"

RUN apk add --no-cache --virtual .build-deps gcc musl-dev  \
    && apk add jq git \
    && pip install --no-cache-dir black==19.10b0 isort==4.3.20 GitPython unidiff requests\
    && apk del .build-deps

COPY "entrypoint.sh" "/entrypoint.sh"
ENTRYPOINT ["/entrypoint.sh"]
