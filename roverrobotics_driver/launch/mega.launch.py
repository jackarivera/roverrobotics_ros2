from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node


def generate_launch_description():
    # urdf = Path(get_package_share_directory(
    #     'roverrobotics_description'), 'urdf', 'rover.urdf')
    # assert urdf.is_file()
    hardware_config = Path(get_package_share_directory(
        'roverrobotics_driver'), 'config', 'mega_config.yaml')
    assert hardware_config.is_file()
    ld = LaunchDescription()

    robot_driver = Node(
        package = 'roverrobotics_driver',
        name = 'roverrobotics_driver',
        executable = 'roverrobotics_driver',
        parameters = [hardware_config],
        respawn=True,
        respawn_delay=1
    )
    
    config_path = Path(get_package_share_directory("ros2_razor_imu"), "config",
                          "razor.yaml")

    imu_node = Node(
        package='ros2_razor_imu', 
        executable='imu_node', 
        parameters=[config_path]
        )
        
    robot_localization_file_path = Path(get_package_share_directory(
        'roverrobotics_driver'), 'config/ekf.yaml')

     # Start robot localization using an Extended Kalman filter
    localization_node = Node(
    	package='robot_localization',
    	executable='ekf_node',
    	name='ekf_filter_node',
    	output='screen',
    	parameters=[robot_localization_file_path]
    	)


    ld.add_action(robot_driver)
    #ld.add_action(imu_node)
    #ld.add_action(localization_node)
    return ld
