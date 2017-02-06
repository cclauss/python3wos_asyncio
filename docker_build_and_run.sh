#!/usr/bin/env bash

APP="python3wos"
docker build -t $APP .
docker run -it -p 8000:8000 --rm --name $APP $APP
# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $APP
