#!/bin/bash
set -e

# 1. تفعيل بيئة ROS 2 Jazzy الأساسية
source /opt/ros/jazzy/setup.bash

# 2. الانتقال إلى المجلد الرئيسي للمستودع في الكودسبايس
WORKSPACE_DIR="/workspaces/ros2_gazebo_codespace"
cd $WORKSPACE_DIR

# 3. تحديث مراجع الاعتماديات وتثبيت أي نقص يخص حزمتك (arm_mobile)
rosdep update
rosdep install --from-paths src --ignore-src -r -y || true

# 4. بناء حزمة الذراع والروبوت المتنقل الخاصة بك
colcon build --symlink-install

# 5. تفعيل بيئة مشروعك تلقائياً عند فتح أي Terminal جديدة
if ! grep -q "source $WORKSPACE_DIR/install/setup.bash" /root/.bashrc; then
    echo "source $WORKSPACE_DIR/install/setup.bash" >> /root/.bashrc
fi

# 6. تشغيل سطح المكتب الافتراضي (noVNC) في الخلفية لتشغيل rviz2
nohup start-desktop.sh > /tmp/desktop.log 2>&1 &

echo "✅ Setup complete for arm_mobile_robot!"
