""" Данный код конфигурирует запуск симулятора черепахи
 и связанных с ним узлов (broadcaster и listener), 
 которые работают с системой координат tf2 в ros.
 
 Этот набор узлов будет использоваться для демонстрации передачи координат 
 между различными черепахами"""

# Необходимые классы и функции для определения запускаемых элементов
from launch import LaunchDescription

# Для объявления аргументов, которые могут быть переданы при запуске launch-файла
from launch.actions import DeclareLaunchArgument

# Доступ к значению аргументов, переданных при запуске
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

# Эта функция вызывается для генерации описания запуска.
# Возвращает экземпляр LaunchDescription, 
# который определяет конфигурацию для запуска

def generate_launch_description():
    return LaunchDescription([
        # Этот узел представляет собой симулятор черепашки
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        # Определяем узел вещателя, который будет запускать узел turtle_tf2_broadcaster
        # Передаётся параметр turtlename, который устанавливает имя черепахи в turtle1
        # Этот узел отправляет трансформации в системе координат ROS для черепахи turtle1
        # Это позволяет отслеживать положение и ориентацию черепахи в пространстве
        Node(
            package='follower_of_turtle',
            executable='turtle_tf2_broadcaster',
            name='broadcaster1',
            parameters=[{'turtlename': 'turtle1'}]
        ),
        # Объявляем аргумент target_frame
        DeclareLaunchArgument(
            'target_frame',
            default_value='turtle1',
            description='Target frame name.'
        ),
        # Определяем второй узел
        # Отправляем трансформации в системе координат для черепахи turtle2.
        # Отслеживаем положение и ориентацию уже второй черепахи
        Node(
            package='follower_of_turtle',
            executable='turtle_tf2_broadcaster',
            name='broadcaster2',
            parameters=[{'turtlename': 'turtle2'}]
        ),
        # Определяем узел слушателся
        # Подписываемся на трансформации в системе координат
        # и прослушиваем изменения в положении и ориентации черепахи
        Node(
            package='follower_of_turtle',
            executable='turtle_tf2_listener',
            name='listener',
            parameters=[{'target_frame': LaunchConfiguration('target_frame'), 'delay' : '5.0'}]
        ),
    ])
