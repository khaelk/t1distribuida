# FROM python:latest
# FROM python:3.10.11-slim-buster
FROM python:3.10.11-alpine

WORKDIR /app

COPY . .

WORKDIR /app/src

# RUN python client/client.py <client_id>

EXPOSE 5000

CMD ["python", "lockserver.py", "172.18.2.1", "5000"]