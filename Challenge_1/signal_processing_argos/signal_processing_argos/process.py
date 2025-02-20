import rclpy
import numpy as np
from rclpy.node import Node

from std_msgs.msg import Float32

class SignalProcessing(Node):
    def __init__(self):
        super().__init__('signal_proce')
        self.subscription_i = self.create_subscription(
            Float32, 'time_argos', self.time_callback, 10)
        self.subscription_w = self.create_subscription(
            Float32, 'signal_argos', self.signal_callback, 10)
        self.publisher1 = self.create_publisher(Float32, 'proc_signal_argos', 10)
        timer_period = 0.05  # 10Hz
        self.timer = self.create_timer(timer_period, self.timer_cb)
        self.last_w = 0.0
        self.last_i = 0.0
        self.phase_shift =5.0

    def time_callback(self, msg):
        self.last_i = msg.data

    def signal_callback(self, msg):
        self.last_w = msg.data

    def timer_cb(self):
        self.last_w = np.sin(self.last_i - self.phase_shift)#gap
        self.proc_w=((self.last_w+1.0)/ 2)#Reduce the amplitude in half

        proc_signal=Float32()
        proc_signal.data= self.proc_w
        self.publisher1.publish(proc_signal)

        self.get_logger().info('Processed Signal: "%f"' % proc_signal.data)

#Main
def main(args=None):
    rclpy.init(args=args)

    signal_processor = SignalProcessing()

    try:
        rclpy.spin(signal_processor)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():  # Ensure shutdown is only called once
            rclpy.shutdown()
        signal_processor.destroy_node()


#Execute Node
if __name__ == '__main__':
    main()
