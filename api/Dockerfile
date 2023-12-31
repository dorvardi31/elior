# Use an appropriate base image (e.g., python:3.8-slim)
FROM python:3.8-slim

# Set the working directory inside the container to /api
WORKDIR /api

# Install necessary packages for Oracle Instant Client and SQL*Plus
RUN apt-get update && \
    apt-get install -y wget libaio1 unzip && \
    wget https://download.oracle.com/otn_software/linux/instantclient/2112000/instantclient-basiclite-linux.x64-21.12.0.0.0dbru.zip -O instantclient.zip && \
    unzip instantclient.zip -d /opt/oracle && \
    rm instantclient.zip && \
    sh -c "echo /opt/oracle/instantclient_21_12 > /etc/ld.so.conf.d/oracle-instantclient.conf" && \
    ldconfig

# Set environment variables (adjust as needed)
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_1
ENV ORACLE_HOME=/opt/oracle/instantclient_21_1

# Copy your requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code into the container
COPY src/ ./

# Define the command to run when the container starts
CMD ["python", "./fileupload.py"]