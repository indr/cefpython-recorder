#!/usr/bin/env bash

if [ ! -e fifo.bgra ]
then
  mkfifo fifo.bgra
fi

if [ -f output.mp4 ]
then
  rm output.mp4
fi

ffmpeg -f rawvideo \
  -pix_fmt bgra \
  -s:v 1280x720 \
  -i fifo.bgra \
  -vf setpts='(RTCTIME - RTCSTART) / (TB * 1000000)' \
  -pix_fmt yuv420p \
  -c:v libx264 \
  output.mp4
