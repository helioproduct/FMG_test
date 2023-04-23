FROM python:3.9-slim-buster
LABEL maintainer="nikolay.p998@gmail.com"

RUN apt-get update && apt-get install -y iputils-ping

COPY requirements.txt /app/requirements.txt

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
