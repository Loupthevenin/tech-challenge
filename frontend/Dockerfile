FROM node:20-bookworm

RUN apt update -y && apt upgrade -y && apt install -y \
    tini \
    && apt clean

COPY ./script.sh /tmp

WORKDIR /app

EXPOSE 3000

ENTRYPOINT ["tini", "--"]
CMD ["bash", "/tmp/script.sh"]
