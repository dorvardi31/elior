#!/bin/bash

echo "Starting Oracle DB initialization script..."


check_oracle_ready() {
  echo "Checking if Oracle DB is ready..."
  echo "exit" | sqlplus SYSTEM/Sep2023N@db:1521/XEPDB1 | grep 'Connected to:'
}

# Wait for Oracle to start
until check_oracle_ready; do
  echo "Waiting for Oracle DB to be ready..."
  sleep 10
done

echo "Oracle DB is ready. Executing the SQL script..."
sqlplus SYSTEM/Sep2023N@db:1521/XEPDB1 @/create_tables.sql

echo "SQL script executed. Oracle DB initialization complete."
