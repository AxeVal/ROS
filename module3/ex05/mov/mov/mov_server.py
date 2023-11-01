import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math as m
import sys
import time


class MovService(Node):
    def __init__(self):
        super().__init__('minimal_service')

        self.subscriber_ = self.create_subscription(Pose, "/turtle1/pose",
                                                    self.pose_callback,
                                                    10)
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.cur_pose_ = Pose()
        self.status = 0
        self.goal_pose = Pose()
        # self.rate = rclpy.Rate()

    def pose_callback(self, msg):
        self.cur_pose_ = msg
        
        if self.status == 0:
            self.goal_pose.x = float(input("Координата X: "))
            self.goal_pose.y = float(input("Координата Y: "))
            self.status = 1
        self.raw_coords_callback(self.goal_pose)
        
    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return ((goal_pose.x - self.cur_pose_.x)**2 +
                (goal_pose.y - self.cur_pose_.y)**2)**0.5

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)
    
    def steering_angle(self, goal_pose):
       """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
       return m.atan2(goal_pose.y - self.cur_pose_.y, goal_pose.x - self.cur_pose_.x)

    def angular_vel(self, goal_pose, constant=6):
       """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
       return constant * (self.steering_angle(goal_pose) - self.cur_pose_.theta)

    def raw_coords_callback(self, goal_pose):
        tolerance = 0.2
        vel_msg = Twist()
        
        if self.euclidean_distance(goal_pose) >= tolerance and self.status == 1:
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.angular.z = self.angular_vel(goal_pose)
            self.publisher_.publish(vel_msg)
            
        elif self.status == 1:
            vel_msg.linear.x = 0.
            vel_msg.angular.z = 0.
            self.publisher_.publish(vel_msg)
            self.status = 0
            
        
def main():
    rclpy.init()
    minimal_service = MovService()
    rclpy.spin(minimal_service)
    minimal_service.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
