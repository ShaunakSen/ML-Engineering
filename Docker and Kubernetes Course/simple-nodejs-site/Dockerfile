FROM alpine:latest
RUN apk update
RUN apk add nodejs
RUN apk add npm
RUN mkdir src
COPY ./ /src
WORKDIR /src
EXPOSE 3000
CMD [ "node", "server.js" ]