from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
#from launch.conditions import IfConditions

from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
	pkg = get_package_share_directory('carrun')
	return LaunchDescription([
		Node(
			package='turtlesim',
		      executable='turtlesim_node',
		      name='sim'
		),
		Node(
			package='carrun',
		      executable='broadcaster',
		      name='broadcaster1',
		      parameters=[
		          {'turtlename': 'turtle1'}
		      ]
		),
		Node(
		      package='carrun',
		      executable='broadcaster',
		      name='broadcaster2',
		      parameters=[
		          {'turtlename': 'turtle2'}
		      ]
		),
		Node(
		      package='carrun',
		      executable='listener',
		      name='listener',
		      parameters=[
		          {'target_frame': 'carrot1'}
		      ]
	 	),
		Node(
		      package='carrun',
		      executable='carrot',
		      name='carrot1',	
		),
		#Node(
		#  	package='rviz2',
		#  	executable='rviz2',
		#  	arguments=['-d', os.path.join(pkg, 'carrun.rviz')],
		#  	condition=IfCondition(LaunchConfiguration('rviz'))
		#),
	])
