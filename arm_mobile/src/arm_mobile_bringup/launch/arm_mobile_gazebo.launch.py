import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():

    # 1. تعريف المسارات (تأكد من أسماء الحزم الصحيحة)
    pkg_description = get_package_share_directory('arm_mobile_description')
    pkg_bringup = get_package_share_directory('arm_mobile_bringup') # افترضنا اسم حزمة التشغيل هكذا
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    urdf_path = os.path.join(pkg_description, 'urdf', 'arm_mobile.urdf.xacro')
    rviz_config_path = os.path.join(pkg_description, 'rviz', 'config.rviz')
    
    # تصحيح مسار ملف الـ Bridge (يجب أن يشير إلى الحزمة التي تحتوي على ملف الـ yaml)
    gazebo_bridge_config_path = os.path.join(pkg_bringup, 'config', 'gazebo_bridge.yaml')
    
    # تصحيح مسار ملف العالم (World)
    world_path = os.path.join(pkg_bringup, 'worlds', 'test_world.sdf')

    # 2. معالجة الـ Xacro
    robot_description = {'robot_description': Command(['xacro ', urdf_path])}

    # 3. عقدة Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # 4. تضمين Gazebo (تشغيل العالم الخاص بك بدلاً من empty.sdf)
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': [world_path, ' -r']}.items(),
    )

    # 5. إنشاء الروبوت في Gazebo
    node_gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'arm_mobile'],
        output='screen',
    )

    # 6. عقدة الـ Bridge (تصحيح تمرير المعاملات)
    node_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': gazebo_bridge_config_path}],
        output='screen',
    )

    # 7. عقدة RViz2
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen'
    )
    # node_teleop = Node(
    #     package='teleop_twist_keyboard',
    #     executable='teleop_twist_keyboard',
    #     name='teleop_twist_keyboard',
    #     output='screen',
    #     prefix='xterm -e', # يفتح نافذة جديدة للتحكم (اختياري لكن ينصح به)
    #     parameters=[{'stamped': True}], # أضف هذا إذا كان الـ Bridge يتوقع TwistStamped
    #     remappings=[
    #         ('/cmd_vel', '/model/my_car/cmd_vel'), # تأكد من مطابقة المسار مع Gazebo
    #     ]
    # )

    return LaunchDescription([
        node_robot_state_publisher,
        gz_sim,
        node_gz_spawn_entity,
        node_gz_bridge,
        node_rviz,
        # node_teleop
    ])