from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, Command
import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    model_arg = DeclareLaunchArgument(
        name="model", 
        default_value=os.path.join(
            get_package_share_directory("robot_description"), "urdf", "description.urdf.xacro"),
        description="Path of the URDF file"
    )

    env_var = SetEnvironmentVariable(
        name="GAZEBO_MODEL_PATH", 
        value=os.path.join(get_package_prefix("robot_description"), "share")
    )
    
    robot_description = ParameterValue(Command(["xacro ", LaunchConfiguration("model")]), value_type=str)
    
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    # joint_state_publisher_gui = Node(
    #     package="joint_state_publisher_gui",
    #     executable="joint_state_publisher_gui"
    # )

    # rviz = Node(
    #     package="rviz2",
    #     executable="rviz2",
    #     name="rviz2",
    #     output="screen",
    #     arguments=["-d", os.path.join(get_package_share_directory("robot_description"), "rviz", "display.rviz")]
    # )

    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzserver.launch.py"))
    )

    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzclient.launch.py"))
    )
    
    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-entity", "robot_demo", "-topic", "robot_description"]
    )

    return LaunchDescription([
        model_arg,
        env_var,
        robot_state_publisher,
        # joint_state_publisher_gui,
        # rviz,
        start_gazebo_server,
        start_gazebo_client,
        spawn_robot
    ])
