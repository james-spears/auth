FROM nginx:1.27.5-alpine-slim

## Copy our default nginx config
COPY ./ /etc/nginx

## Create an empty logs folder
RUN mkdir /etc/nginx/logs

## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

CMD ["nginx", "-g", "daemon off;"]