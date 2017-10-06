#!/usr/bin/env bash

if [ ! -e fifo.bgra ]
then
  mkfifo fifo.bgra
fi

# python capture.py http://localhost:8000/fps.html 1280 720 25 fifo.bgra
python capture.py http://localhost:8000/clock.html 1280 720 25 fifo.bgra
