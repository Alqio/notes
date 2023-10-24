FROM python:3.11

COPY app /app
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload"]
