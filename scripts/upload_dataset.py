#!/bin/bash

for FILE in $(ls lfw-deepfunneled/train/**/*.jpg); do echo Subiendo $FILE; curl -X 'POST' 'http://127.0.0.1:8000/files/train' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F "upload_file=@${FILE};type=image/jpeg"; done
for FILE in $(ls lfw-deepfunneled/test/**/*.jpg); do echo Subiendo $FILE; curl -X 'POST' 'http://127.0.0.1:8000/files/test' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F "upload_file=@${FILE};type=image/jpeg"; done
