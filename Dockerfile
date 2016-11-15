FROM python:2.7-alpine

# Update
RUN apk add --update python py-pip

RUN apk add --update curl #&& \
#    rm -rf /var/cache/apk/*

VOLUME /app-src

RUN mkdir -p /local-deps

WORKDIR /local-deps

COPY docker-files/requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app-src

EXPOSE  8000
#CMD ["python", "/app-src/user-service.py", "-p 8000"]

ENTRYPOINT /app-src/run-py-app.sh
