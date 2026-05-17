FROM ros:jazzy-perception

# تجنب الأسئلة التفاعلية أثناء apt
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:0
ENV TURTLEBOT3_MODEL=burger

RUN apt-get update && apt-get install -y \
    ros-jazzy-turtlesim \
    ros-jazzy-gz-ros2-control \
    ros-jazzy-rviz2 \
    ros-jazzy-xacro \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-teleop-twist-keyboard \
    xvfb fluxbox novnc websockify x11vnc \
    python3-colcon-common-extensions \
    python3-rosdep \
    git curl wget sudo \
    && rm -rf /var/lib/apt/lists/*

# noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC \
    && ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# سكريبت تشغيل البيئة الرسومية
RUN cat > /usr/local/bin/start-desktop.sh << 'EOF'
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
EOF
chmod +x /usr/local/bin/start-desktop.sh

# source تلقائي
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc \
    && echo "export DISPLAY=:0" >> /root/.bashrc \
    && echo "export TURTLEBOT3_MODEL=burger" >> /root/.bashrc

EXPOSE 6080 5900
