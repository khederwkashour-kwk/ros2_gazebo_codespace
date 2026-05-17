#!/bin/bash
set -e
source /opt/ros/jazzy/setup.bash

mkdir -p /root/drone_ws/src
cd /root/drone_ws/src
git clone https://github.com/NovoG93/sjtu_drone.git

cd /root/drone_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y || true
colcon build --symlink-install

echo "source /root/drone_ws/install/setup.bash" >> /root/.bashrc

nohup start-desktop.sh > /tmp/desktop.log 2>&1 &
echo "✅ Setup complete!"
