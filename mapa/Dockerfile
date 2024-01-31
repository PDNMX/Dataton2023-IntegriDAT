FROM node:18-alpine

MAINTAINER Sergio Rodríguez <sergio.rdzsg@gmail.com>

ADD . /mapa
WORKDIR /mapa

RUN npm i -g serve 

EXPOSE 5000

CMD ["serve", "-s", "/mapa", "-l", "5000"]
