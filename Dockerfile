FROM python:3.7.2-alpine3.8
LABEL maintainer="nikolay.p998@gmail.com"

# Copy all files from repo
COPY . ./app
WORKDIR /app

# Dependencies
RUN apk update && apk upgrade && apk add bash
RUN ["pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "-r", "requirements.txt"]

# start API process
CMD ["python", "main.py"]