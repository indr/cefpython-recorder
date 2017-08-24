#!/bin/bash

if [ ! -e fifo.rgba ]
then
  mkfifo fifo.rgba
fi

ffplay -f rawvideo -pixel_format rgba -video_size 320x240 -framerate 25 fifo.rgba

