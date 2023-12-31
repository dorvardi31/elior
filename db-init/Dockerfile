FROM ubuntu:latest

# Install necessary packages for Oracle Instant Client and SQL*Plus
RUN apt-get update && apt-get install -y wget libaio1 unzip

# Download and install Oracle Instant Client Basic Lite
RUN wget https://download.oracle.com/otn_software/linux/instantclient/2112000/instantclient-basiclite-linux.x64-21.12.0.0.0dbru.zip -O instantclient-basiclite.zip && \
    unzip instantclient-basiclite.zip -d /opt/oracle && \
    rm instantclient-basiclite.zip

# Download and install SQL*Plus
RUN wget https://download.oracle.com/otn_software/linux/instantclient/2112000/instantclient-sqlplus-linux.x64-21.12.0.0.0dbru.zip -O sqlplus.zip && \
    unzip sqlplus.zip -d /opt/oracle && \
    rm sqlplus.zip

# Configure environment variables
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_12:$LD_LIBRARY_PATH
ENV PATH=/opt/oracle/instantclient_21_12:$PATH


COPY initialize-oracle-db.sh /initialize-oracle-db.sh
COPY create_tables.sql /create_tables.sql

RUN chmod +x /initialize-oracle-db.sh

CMD ["/initialize-oracle-db.sh"]