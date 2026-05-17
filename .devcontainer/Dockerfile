FROM ros:jazzy-perception

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:0
ENV TURTLEBOT3_MODEL=burger

RUN apt-get update && apt-get install -y \
    ros-jazzy-turtlesim \
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

RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC \
    && ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# انسخ السكريبت مباشرة من المجلد
COPY start-desktop.sh /usr/local/bin/start-desktop.sh
RUN chmod +x /usr/local/bin/start-desktop.sh

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc \
    && echo "export DISPLAY=:0" >> /root/.bashrc \
    && echo "export TURTLEBOT3_MODEL=burger" >> /root/.bashrc

EXPOSE 6080 5900
