""" Этот узел используется для издания трансформаций между системами координат, 
связанными с черепашкой и координатной системой world """ 


import math
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose


def quaternion_from_euler(ai, aj, ak):
    # Деление на 2 приводит к получению половины угла для каждой из трех осей
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0

    # Косинусы половинных углов
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)

    # Синусы половинных углов
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)

    # Произведения косинусов и синусов половинных углов
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    # Вычисления коэффициентов кватерниона 
    # Преобразование углов Эйлера в кватернионы
    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q

# Класс FramePublisher
class FramePublisher(Node):

    def __init__(self):
        super().__init__('turtle_tf2_frame_publisher')

        # Объявляем и получаем параметр turtlename
        self.turtlename = self.declare_parameter(
            'turtlename', 'turtle').get_parameter_value().string_value

        # Инициализируем вещателя трансформаций
        self.tf_broadcaster = TransformBroadcaster(self)

        # Подписываемся на тему turtle{1}{2}/pose
        # Вызываем функцию handle_turtle_pose
        self.subscription = self.create_subscription(
            Pose,
            f'/{self.turtlename}/pose',
            self.handle_turtle_pose,
            1)
        self.subscription  # предотвращаем предупреждение о неиспользованной переменной

    def handle_turtle_pose(self, msg):
        t = TransformStamped()

        # Читаем содержимое сообщения
        # Присваиваем его соответствующим переменным трансформации
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.turtlename

        # Черепаха существует только в двух измерениях, поэтому мы получаем координаты x и y из сообщения
        # и устанавливаем координату z в 0
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0

        # По той же причине черепаха может вращаться только вокруг одной оси,
        # и поэтому мы устанавливаем вращение по x и y в 0 и получаем
        # угол вращения вокруг оси z из сообщения
        q = quaternion_from_euler(0, 0, msg.theta)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # Отправляем трансформацию
        self.tf_broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = FramePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()