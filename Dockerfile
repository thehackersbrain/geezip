FROM python:3.8-alpine3.11

RUN apk add --no-cache gcc alpine-sdk linux-headers gzip=1.10-r0 sed

RUN mkdir -p /usr/src/web
WORKDIR /usr/src/web

COPY ./web .
COPY /web/app.ini .

RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi

RUN echo -e "uwsgi\nuwsgi" | adduser uwsgi

RUN mkdir -p /usr/src/logs
RUN chown uwsgi:uwsgi -R /usr/src/logs

RUN echo 'flag{Z1p_Sl1pp3d_:(}' > /home/uwsgi/flag.txt
RUN echo "Note to myself: here's your credentials: 'sup3r_s3cr37_d1n3sh'" | base64 > /home/uwsgi/.note

EXPOSE 8080

CMD ["uwsgi", "--ini", "app.ini"]
