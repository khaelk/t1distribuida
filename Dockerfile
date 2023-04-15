FROM python:slim

WORKDIR /app

COPY . .

# RUN python client/client.py <client_id>

# EXPOSE 5000

# CMD ["python", "src/lockserver.py", "localhost", "5000"]