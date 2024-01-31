FROM node:18-alpine

MAINTAINER Sergio Rodríguez <sergio.rdzsg@gmail.com>

ADD . /mapa
WORKDIR /mapa

RUN npm install \
&& npm run build \
&& npm i -g serve 

EXPOSE 5000

CMD ["serve", "-s", "dist", "-l", "5000"]
