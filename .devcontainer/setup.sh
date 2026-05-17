#!/bin/bash
set -e

# إنشاء workspace وبناء sjtu_drone
mkdir -p /root/drone_ws/src
cd /root/drone_ws/src
git clone https://github.com/NovoG93/sjtu_drone.git

cd /root/drone_ws
source /opt/ros/jazzy/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y || true
colcon build --symlink-install

# source في bashrc
echo "source /root/drone_ws/install/setup.bash" >> /root/.bashrc

# تشغيل البيئة الرسومية في الخلفية
nohup start-desktop.sh > /tmp/desktop.log 2>&1 &

echo "✅ Setup complete! Open port 6080 to see the desktop."
