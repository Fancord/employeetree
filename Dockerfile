FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY . /code/

RUN pip install --no-cache-dir -r requirements.txt


# EXPOSE 8000

