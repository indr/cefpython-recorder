#!/bin/bash

if [ ! -e fifo.bgra ]
then
  mkfifo fifo.bgra
fi

# python capture.py http://localhost:8082/clock.html 320 240 25
# python capture.py http://localhost:8082/fps.html 320 240 50
python capture.py http://localhost:8081/?channel=program 1080 720 25

