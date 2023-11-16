import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from action_turtle_commands.action import MessageTurtleCommands

# Класс, представляющий клиент для отправки действий черепахе
class CommandActionClient(Node):

    def __init__(self):
        super().__init__('action_turtle_client')
        self._action_client = ActionClient(self, MessageTurtleCommands, 'move_turtle')
        self._action_client.wait_for_server()
        self.send_goals()

    def send_goals(self):
        def send_goal(goal_msg, delay_seconds):
            # Логгируем отправку цели
            self.get_logger().info(f'Sending goal: {goal_msg.command}')
            # Отправляем цель асинхронно и регистрируем обратные вызовы
            self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
            self._send_goal_future.add_done_callback(self.goal_response_callback)

        # Список целей для выполнения черепахой
        goal_messages = [
            {'command': 'forward', 's': 2, 'angle': 0},
            {'command': 'turn_right', 's': 0, 'angle': 90},
            {'command': 'forward', 's': 1, 'angle': 0},
            {'command': 'turn_right', 's': 0, 'angle': 90},
        ]

        for goal_data in goal_messages:
            goal_msg = MessageTurtleCommands.Goal()
            goal_msg.command = goal_data['command']
            goal_msg.s = goal_data['s']
            goal_msg.angle = goal_data['angle']

            # Отправляем цель с задержкой
            send_goal(goal_msg, delay_seconds=1)

    # Обратный вызов для обработки ответа на цель
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            # Цель была отклонена
            self.get_logger().info('Goal rejected')
        else:
            # Цель была принята
            self.get_logger().info('Goal accepted')
            # Запрашиваем результат выполнения цели асинхронно
            self._get_result_future = goal_handle.get_result_async()
            self._get_result_future.add_done_callback(self.get_result_callback)

    # Обратный вызов для обработки результата выполнения цели
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.result}')
        rclpy.shutdown()  # Завершаем работу ROS 2

    # Обратный вызов для обработки обратной связи от сервера
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.odom}')

# Главная функция программы
def main(args=None):
    rclpy.init(args=args)  # Инициализируем ROS 2
    action_client = CommandActionClient()  # Создаем экземпляр клиента
    rclpy.spin(action_client)  # Запускаем цикл событий ROS 2

if __name__ == '__main__':
    main()  # Выполняем главную функцию, если скрипт запущен как основная программа

