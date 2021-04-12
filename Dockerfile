
FROM balenalib/raspberrypi3-debian-python:run

COPY requirements.txt /

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 80

COPY ./api /api

CMD ["uvicorn", "api.endpoints:app", "--host", "0.0.0.0", "--port", "80"]
