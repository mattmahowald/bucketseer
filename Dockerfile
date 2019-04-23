from python:3.6-alpine

RUN apk add --update python3-dev build-base

RUN mkdir -p /var/secrets/google && touch /var/secrets/google/kube-cron-jobs-service-account-key.json

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY src/ /app
WORKDIR /app
CMD ["python", "main.py"]
