FROM python:alpine3.17

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./sota /app/sota

CMD ["uvicorn", "sota.main:app", "--host", "0.0.0.0", "--port", "80"]