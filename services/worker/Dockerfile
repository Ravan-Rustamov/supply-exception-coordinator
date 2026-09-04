FROM python:3.12-slim

WORKDIR /app

RUN pip install redis python-dateutil

COPY main.py .

CMD ["python", "main.py"]
