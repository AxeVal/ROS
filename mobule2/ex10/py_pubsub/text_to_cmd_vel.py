# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist

class PublisherSubscriber(Node):

	def __init__(self):
		super().__init__('text_to_cmd_vel')
		self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
		self.subscription = self.create_subscription(String, 'cmd_text', self.callback, 10)
		self.msg = Twist()
		self.subscription # prevent unused variable warn
	        
	def callback(self, msg):
		self.get_logger().info('I heard: "%s"' % msg.data)
		if msg.data == 'turn_right':
			self.msg.angular.z = -1.57
			self.msg.linear.x = 0.0
		elif msg.data == 'turn_left':
			self.msg.angular.z = 1.57
			self.msg.linear.x = 0.0
		elif msg.data == 'move_forward':
			self.msg.linear.x = 2.0
			self.msg.angular.z = 0.0
		elif msg.data == 'move_backward':
			self.msg.linear.x = -2.0
			self.msg.angular.z = 0.0
		else:
			self.get_logger().info('Wrong command: choose <turn_left> or <turn_right> or <move_forward> or <move_backward>')
		self.publisher_.publish(self.msg)
		self.get_logger().info('Publishing: "%s"' % self.msg)

def main(args=None):
    rclpy.init(args=args)

    text_to_cmd_vel = PublisherSubscriber()

    rclpy.spin(text_to_cmd_vel)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    text_to_cmd_vel.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
