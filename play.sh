#!/usr/bin/env bash

if [ ! -e fifo.bgra ]
then
  mkfifo fifo.bgra
fi

ffplay -f rawvideo -pixel_format bgra -video_size 640x480 -framerate 25 fifo.bgra
