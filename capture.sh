#!/bin/bash

if [ ! -e fifo.rgba ]
then
  mkfifo fifo.rgba
fi

python capture.py http://localhost:8082/index.html 320 240 25

