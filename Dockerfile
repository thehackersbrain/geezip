FROM python:3.8-alpine3.11

RUN apk add --no-cache gcc alpine-sdk linux-headers gzip=1.10-r0 sed

RUN mkdir -p /usr/src/web
WORKDIR /usr/src/web

COPY ./web .
COPY /web/app.ini .

RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi

RUN echo -e "uwsgi\nuwsgi" | adduser uwsgi

EXPOSE 8080

CMD ["uwsgi", "--ini", "app.ini"]