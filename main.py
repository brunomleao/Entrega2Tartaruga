import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose as TPose
from collections import deque

MAX_DIFF = 0.1


class Pose(TPose):
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        super().__init__(x=x, y=y, theta=theta)

    def __repr__(self):
        return f"(x={self.x:.2f}, y={self.y:.2f})"

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __eq__(self, other):
        return abs(self.x - other.x) < MAX_DIFF and abs(self.y - other.y) < MAX_DIFF


class PathController:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, x, y):
        self.queue.append(Pose(x=x, y=y))

    def dequeue(self):
        return self.queue.popleft()

    def is_empty(self):
        return len(self.queue) == 0


class TurtleController(Node):
    def __init__(self, path_controler, control_period=0.02):
        super().__init__('turtle_controller')
        self.pose = Pose(x=-40.0)
        self.setpoint = Pose(x=-40.0)
        self.path_controler = path_controler
        self.publisher = self.create_publisher(
            msg_type=Twist,
            topic="/turtle1/cmd_vel",
            qos_profile=10
        )
        self.subscription = self.create_subscription(
            msg_type=Pose,
            topic="/turtle1/pose",
            callback=self.pose_callback,
            qos_profile=10
        )
        self.control_timer = self.create_timer(
            timer_period_sec=control_period,
            callback=self.control_callback
        )

    def control_callback(self):
        if self.pose.x == -40.0:
            self.get_logger().info("Waiting for the first pose...")
            return

        msg = Twist()
        x_diff = self.setpoint.x - self.pose.x
        y_diff = self.setpoint.y - self.pose.y

        if self.pose == self.setpoint:
            msg.linear.x, msg.linear.y = 0.0, 0.0
            self.update_setpoint()

        if abs(y_diff) > MAX_DIFF:
            msg.linear.y = 0.5 if y_diff > 0 else -0.5
        else:
            msg.linear.y = 0.0

        if abs(x_diff) > MAX_DIFF:
            msg.linear.x = 0.5 if x_diff > 0 else -0.5
        else:
            msg.linear.x = 0.0

        self.publisher.publish(msg)

    def update_setpoint(self):
        try:
            self.setpoint = self.path_controler.dequeue()
            self.get_logger().info(f"Moving to setpoint: {self.setpoint}")
        except IndexError:
            self.get_logger().info("End of the journey!")
            self.get_logger().info(f"Current position: x={self.pose.x}, y={self.pose.y}")
            exit()

    def pose_callback(self, msg):
        self.pose = Pose(x=msg.x, y=msg.y, theta=msg.theta)
        if self.setpoint.x == -40.0:
            self.update_setpoint()


def main(args=None):
    rclpy.init(args=args)
    mc = PathController()
    print("Insira as coordenadas de destino, aperte enter para finalizar.")
    while True:
        x = input("Insira a coordenada x: ")
        if not x:
            break
        y = input("Insira a coordenada y: ")
        if not y:
            break
        mc.enqueue(float(x), float(y))

    tc = TurtleController(mc)
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()