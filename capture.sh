#!/bin/bash

if [ ! -e fifo.rgba ]
then
  mkfifo fifo.rgba
fi

# python capture.py http://localhost:8082/clock.html 320 240 25
# python capture.py http://localhost:8082/fps.html 320 240 50
# python capture.py https://threejs.org/examples/webgl_points_dynamic.html 320 240 25
python capture.py http://www.indr.ch/ 320 240 25

