FROM frolvlad/alpine-python2

RUN apk update
RUN apk add ca-certificates gcc musl-dev libjpeg-turbo-dev zlib-dev bash zlib python-dev readline-dev ncurses-dev make

RUN CFLAGS="$CFLAGS -L/lib" pip install pillow
RUN pip install yowsup2
RUN pip install paho-mqtt

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN rm /usr/src/app/waserver/config.py
COPY ./waserver/config-prod.py /usr/src/app/waserver/config.py

RUN python waserver/waserver.py noconn

CMD ["python", "waserver/waserver.py"]
