import math

from geometry_msgs.msg import TransformStamped

import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster
import time


class DynamicFrameBroadcaster(Node):

    def init(self):
        super().init('dynamic_frame_tf2_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.01, self.broadcast_timer_callback)
        self.target_frame = self.declare_parameter(
          'radius', 3).get_parameter_value().integer_value

    def broadcast_timer_callback(self):
        msec = time.time()
        seconds = self.get_clock().now().nanoseconds #.seconds_nanoseconds()
        x = msec * 1000 * math.pi

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'turtle1'
        t.child_frame_id = 'carrot1'
        t.transform.translation.x = self.target_frame * math.sin(x)
        t.transform.translation.y = self.target_frame * math.cos(x)
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
