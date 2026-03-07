#!/usr/bin/env python3

import serial
import rclpy
from rclpy.node import Node
from rover_interfaces.msg import Signal

class RssiMover(Node):
    def __init__(self):
        super().__init__('rssi_mover')
        
        # Subscribe to wifi signal
        self.subscription = self.create_subscription(
            Signal,
            '/wifi_signal',
            self.signal_callback,
            10
        )

        # Target RSSI to stop at
        self.target_rssi = -40  # stop moving when RSSI reaches this
        self.last_rssi = None    # store previous RSSI
        self.moving_left = True  # start by moving left
        self.serial = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)

    # Function to "move left"
    def move_left(self):
        print("Move LEFT")
        self.serial.write(b'L')

    # Function to "move right"
    def move_right(self):
        print("Move RIGHT")
        self.serial.write(b'R')

    # Function to stop
    def stop(self):
        print("STOP")
        self.serial.write(b'S')

    # Callback for the wifi signal
    def signal_callback(self, msg: Signal):
        rssi = msg.rssi

        # Stop if target RSSI is reached or exceeded
        if rssi >= self.target_rssi:
            self.stop()
        else:
            if self.last_rssi is None:
                # First measurement, start moving left
                self.move_left()
                self.moving_left = True
            else:
                if rssi < self.last_rssi:
                    # RSSI dropped → wrong direction, switch
                    if self.moving_left:
                        self.move_right()
                        self.moving_left = False
                    else:
                        self.move_left()
                        self.moving_left = True
                else:
                    # RSSI improving → keep moving same direction
                    if self.moving_left:
                        self.move_left()
                    else:
                        self.move_right()

        # Update last RSSI for next comparison
        self.last_rssi = rssi


def main(args=None):
    rclpy.init(args=args)
    node = RssiMover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
