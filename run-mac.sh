#!/bin/bash

docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker build . -t cs5331
docker run -p 1888:80 -p 8080:8080 -t cs5331
