""" Этот узел является частью системы управления для двух черепах,
где одна черепаха следит за другой и перемещается в её направлении
с использованием трансформаций и команд управления """

import math
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node

from tf2_ros import TransformException

# Буфер трансформаций предназначен для хранения и управления
# информацией о трансформациях между различными фреймами
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from turtlesim.srv import Spawn
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException


class FrameListener(Node):

    def __init__(self):
        super().__init__('turtle_tf2_frame_listener')

        # Объявление и получение параметра `target_frame`
        self.target_frame = self.declare_parameter(
            'target_frame', 'turtle1').get_parameter_value().string_value

        # Создание буфера и слушателя трансформаций
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.delay = float(self.declare_parameter('delay', '5.0').get_parameter_value().string_value)

        # Создание клиента для спавна черепашки
        self.spawner = self.create_client(Spawn, 'spawn')
        
        # Булевы переменные для хранения информации
        # о доступности сервиса создания черепашки
        self.turtle_spawning_service_ready = False
        
        # Была ли черепаха успешно создана
        self.turtle_spawned = False

        # Создание издателя для отправки команд управления turtle2
        self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 1)

        # Вызов функции on_timer каждую секунду
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        # Сохранение имен кадров в переменных, которые будут использоваться
        # для вычисления трансформаций
        from_frame_rel = self.target_frame
        to_frame_rel = 'turtle2'

        # Если условие turtle_spawning_service_ready выполняется,
	    # то проверяется, была ли черепаха успешно создана
        if self.turtle_spawning_service_ready:

            # Если она была создана, узел пытается найти
            # трансформацию между to_frame_rel и from_frame_rel (turtle1 и turtle2)
            # и отправляет команды управления черепахой turtle2
            # в направлении turtle1 на основе этих трансформаций.
            
            if self.turtle_spawned:
                # Поиск трансформации между target_frame и turtle2
                # и отправка команд управления для turtle2 для достижения target_frame
                try:
		    # Вычисляем момент времени, который будет использоваться при поиске трансформации между
		    # turtle1 и turtle2
                    when = self.get_clock().now() - rclpy.time.Duration(seconds=self.delay)
			
		    # Выполняем поиск и получение трансформации между turtle1 и turtle2
                    trans = self.tf_buffer.lookup_transform_full(
                        target_frame = to_frame_rel,
                        target_time = rclpy.time.Time(),
                        source_frame = from_frame_rel,
                        source_time = when,
                        fixed_frame = 'world',
                        timeout=rclpy.duration.Duration(seconds=0.05))
                
                # From tutorial
		# Обработка исключений, которые могут возникнуть при попытке выполнить операцию поиска и получения trans
                except (LookupException, ConnectivityException, ExtrapolationException):
                   self.get_logger().info('transform not ready')
                   return

                # Движение turtle2 в направлении turtle1,
		# используя вычисленные угловую и линейную скорости.
                msg = Twist()
                scale_rotation_rate = 1.0
                msg.angular.z = scale_rotation_rate * math.atan2(
                    trans.transform.translation.y,
                    trans.transform.translation.x)

                scale_forward_speed = 0.5
                msg.linear.x = scale_forward_speed * math.sqrt(
                    trans.transform.translation.x ** 2 +
                    trans.transform.translation.y ** 2)

                self.publisher.publish(msg)

            # Если черепаха ещё не была создана, узел проверяет,
            # завершился ли сервис создания черепахи (result.done()), и, если это так,
            # выводит сообщение об успешном создании черепахи.
            # В противном случае, выводится сообщение о том, что создание ещё не завершено.
            else:
                if self.result.done():
                    self.get_logger().info(
                        f'Successfully spawned {self.result.result().name}')
                    self.turtle_spawned = True
                else:
                    self.get_logger().info('Spawn is not finished')
        
        # Если условие turtle_spawning_service_ready не выполняется,
        # то узел проверяет, готов ли сервис для создания черепахи (spawner.service_is_ready())
        else:

            # Если сервис готов, он инициализирует запрос для создания черепахи (Spawn.Request()),
            # указывая name и x, y, theta. 
            if self.spawner.service_is_ready():

                # Инициализация запроса с именем черепахи и координатами
                # Обратите внимание, что x, y и theta определены как вещественные числа в turtlesim/srv/Spawn
                request = Spawn.Request()
                request.name = 'turtle2'
                request.x = 4.0
                request.y = 2.0
                request.theta = 0.0

                # Вызов запроса
                self.result = self.spawner.call_async(request)
                self.turtle_spawning_service_ready = True
            else:
                # Проверка готовности сервиса
                self.get_logger().info('Service is not ready')


def main():
    rclpy.init()
    node = FrameListener()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
