#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from rover_interfaces.msg import Signal

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SignalNode(Node):

    def __init__(self):
        super().__init__('signal_node')

        self.publisher_ = self.create_publisher(Signal, 'wifi_signal', 10)
        self.timer = self.create_timer(0.5, self.get_signal)

        self.login_url = "https://192.168.1.8/api/auth"
        self.data_url = "https://192.168.1.8/signal.cgi"

        self.session = requests.Session()
        self.session.verify = False

        self.login()

    def login(self):
        auth = {
            "username": "ubnt",
            "password": "mt-rover_123"
        }

        try:
            self.session.post(self.login_url, data=auth).raise_for_status()
            self.get_logger().info("Logged in successfully")
        except Exception as e:
            self.get_logger().error(f"Login failed: {e}")

    def get_signal(self):
        try:
            response = self.session.get(self.data_url)
            response.raise_for_status()
            data = response.json()

            msg = Signal()
            msg.signal = data["signal"]
            msg.rssi = data["rssi"]
            msg.noisef = data["noisef"]
            msg.chbw = data["chbw"]
            msg.rx_chainmask = data["rx_chainmask"]

            msg.chainrssi = data["chainrssi"]
            msg.chainrssimgmt = data["chainrssimgmt"]
            msg.chainrssiext = data["chainrssiext"]

            self.publisher_.publish(msg)

            self.get_logger().info(
                f"RSSI: {msg.rssi} dBm | Noise: {msg.noisef} dBm"
            )

        except Exception as e:
            self.get_logger().error(f"Failed to get signal: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = SignalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
