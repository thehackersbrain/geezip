#!/bin/bash

docker build -t web .
docker run -p 8080:8080 web
