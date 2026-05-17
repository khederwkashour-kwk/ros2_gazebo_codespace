#!/bin/bash
export DISPLAY=:0
rm -f /tmp/.X0-lock /tmp/.X11-unix/X0 2>/dev/null
Xvfb :0 -screen 0 1280x800x24 &
sleep 1
fluxbox &
x11vnc -display :0 -forever -nopw -shared -rfbport 5900 -quiet &
sleep 1
/opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &
echo "Desktop ready at port 6080"
wait
