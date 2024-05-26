FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD pass

COPY ./generate.sql /docker-entrypoint-initdb.d/generate.sql
