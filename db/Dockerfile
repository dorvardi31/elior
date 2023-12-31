
FROM oracle/database:21.3.0-xe


RUN mkdir -p /docker-entrypoint-initdb.d/


COPY ./init_scripts/ /docker-entrypoint-initdb.d/

EXPOSE 1521
