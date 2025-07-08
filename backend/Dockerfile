FROM python:3.11-slim

RUN apt update -y && apt upgrade -y && apt install -y \
    tini \
    && apt clean

COPY ./script.sh /tmp

WORKDIR /app

ENTRYPOINT ["tini", "--"]
CMD ["bash", "/tmp/script.sh"]
