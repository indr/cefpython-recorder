#!/usr/bin/env bash

if [ -f output.mp4 ]
then
  rm output.mp4
fi

ffmpeg \
  -re \
  -i big_buck_bunny_720p_h264.mov \
  -f rawvideo \
  -pix_fmt bgra \
  -s:v 1280x720 \
  -i fifo.bgra \
  -filter_complex "[1:v]setpts='(RTCTIME - RTCSTART) / (TB * 1000000)'[o1];[0:v][o1]overlay" \
  output.mp4

