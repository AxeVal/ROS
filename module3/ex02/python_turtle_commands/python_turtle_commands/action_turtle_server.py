import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from action_turtle_commands.action import MessageTurtleCommands
import time
import math

class TurtleCommandActionServer(Node):

    def __init__(self):
        super().__init__('turtle_command_action_server')
        self.current_odom = 0.0  # Текущее значение одометрии
        self.flag = 0  # Флаг для определения начальной и конечной позиции при движении
        self.twist = Twist()  # Сообщение для управления движением черепахи
        self.before_pose = Pose()  # Позиция перед началом движения
        self.after_pose = Pose()  # Позиция после завершения движения
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)  # Публикатор для управления черепахой
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.callback, 10)  # Подписчик на данные о позиции черепахи
        self.subscription
        self._action_server = ActionServer(
            self,
            MessageTurtleCommands,
            'move_turtle',
            self.execute_callback)  # Action-сервер для обработки команд черепахи
        self.goal_handle = None  # Обработчик текущей цели
        self.rasst = 0  # Пройденное расстояние

    def callback(self, msg):
        if self.flag == 1:
            self.before_pose = msg
            self.flag = 0
        self.after_pose = msg

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = MessageTurtleCommands.Feedback()

        if goal_handle.request.command == 'forward':
            self.twist.linear.x = float(goal_handle.request.s)
            self.twist.angular.z = 0.0
            self.twist.angular.z = float(goal_handle.request.angle * math.pi / 180)  # Преобразование угла в радианы
            self.rasst += float(goal_handle.request.s)
        elif goal_handle.request.command == 'turn_right':
            self.twist.linear.x = 0.0
            self.twist.angular.z = -float(goal_handle.request.angle * math.pi / 180)  # Преобразование угла в радианы

        self.flag = 1
        self.publisher_.publish(self.twist)
        
        time.sleep(6)
        
        goal_handle.publish_feedback(feedback_msg)
        
        goal_handle.succeed()
        self.goal_handle = goal_handle
        return MessageTurtleCommands.Result(result=True)

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Goal canceled')
        self.publisher_.publish(Twist())  # Остановить движение при отмене цели
        goal_handle.canceled()
        self.flag = 0

def main(args=None):
    rclpy.init(args=args)
    action_turtle_server = TurtleCommandActionServer()

    rclpy.spin(action_turtle_server)


if __name__ == '__main__':
    main()

