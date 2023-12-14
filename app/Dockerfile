FROM python:3.8

WORKDIR /usr/src/app

COPY src/ ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000


CMD ["python", "./data_processing.py"]
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["python", "./file_upload_gui.py"]
