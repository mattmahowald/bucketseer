from python:3.6-alpine

EXPOSE 8000

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY src/ /app
WORKDIR /app
CMD ["gunicorn", "-w 4", "--log-level=debug", "--bind=0.0.0.0:8000", "main:app"]
