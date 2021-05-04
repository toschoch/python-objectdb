FROM shocki/rpi-rdm-processor as run

COPY  requirements.txt /

RUN pip install --upgrade pip --index-url https://www.piwheels.org/simple && \
 pip install -r requirements.txt --index-url https://www.piwheels.org/simple

ENV DATA_DIRECTORY=/data
ENV BUCKETS_CONFIG=/config/buckets.yml
EXPOSE 80

COPY ./api /api

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "80"]
