FROM python:3.11

COPY app /app

WORKDIR /app

RUN pip install fastapi "uvicorn[standard]"

CMD ["uvicorn", "main:app", "--reload"]
