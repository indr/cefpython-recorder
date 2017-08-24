#!/bin/bash

if [ ! -e fifo.rgba ]
then
  mkfifo fifo.rgba
fi

if [ -f output.mp4 ]
then
  rm output.mp4
fi

ffmpeg -f rawvideo -pix_fmt rgba -s:v 320x240 -r 25 -i fifo.rgba -pix_fmt yuv420p -c:v libx264 output.mp4

