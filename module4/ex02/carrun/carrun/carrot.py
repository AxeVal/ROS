import math

from geometry_msgs.msg import TransformStamped

from turtlesim.msg import Pose
import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster


class DynamicFrameBroadcaster(Node):

    def __init__(self):
        super().__init__('dynamic_frame_tf2_broadcaster')
        self.radius = self.declare_parameter(
          'radius', 1.0).get_parameter_value().double_value
        self.direction = -self.declare_parameter(
          'direction_of_rotation', 1).get_parameter_value().integer_value
        
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_timer_callback)

    def broadcast_timer_callback(self):
        seconds, nanosecs= self.get_clock().now().seconds_nanoseconds()
        time = (seconds + nanosecs*0.000000001)

        t = TransformStamped()

        turtlesim = Pose()
        t.transform.translation.x = turtlesim.x + self.radius * math.cos(time*self.direction)
        t.transform.translation.y = turtlesim.x + self.radius * math.sin(time*self.direction)


        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'turtle1'
        t.child_frame_id = 'carrot1'
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = DynamicFrameBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
