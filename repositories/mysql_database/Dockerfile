FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD pass
ENV MYSQL_DATABASE my_database

# COPY ./generate.sql /docker-entrypoint-initdb.d/generate.sql
#The MySQL Docker entrypoint runs any .sql files in the /docker-entrypoint-initdb.d/ directory in alphabetical order
COPY ./sakila/sakila-schema.sql /docker-entrypoint-initdb.d/1_sakila-schema.sql
COPY ./sakila/sakila-data.sql /docker-entrypoint-initdb.d/2_sakila-data.sql
COPY ./generate.sql /docker-entrypoint-initdb.d/generate.sql