import rclpy
from rclpy.node import Node

from sensor_msgs.msg import NavSatFix
from sbg_driver.msg import SbgGpsPos


class DualGpsPublisher(Node):

    def __init__(self):
        super().__init__('dual_gps_input_publisher')

        self.sbg_pub = self.create_publisher(SbgGpsPos, "/sbg/gps_pos", 10)
        self.ublox_pub = self.create_publisher(NavSatFix, "/antenna/fix", 10)

        self.get_logger().info("Dual GPS publisher started")

        self.run()

    def run(self):

        while rclpy.ok():

            try:
                # -------- SBG INPUT --------
                sbg_input = input(
                    "\nSBG GPS (lat lon alt) or ENTER to skip: "
                )

                if sbg_input.strip() != "":
                    lat, lon, alt = map(float, sbg_input.split())

                    sbg_msg = SbgGpsPos()

                    sbg_msg.latitude = lat
                    sbg_msg.longitude = lon
                    sbg_msg.altitude = alt

                    self.sbg_pub.publish(sbg_msg)

                    self.get_logger().info(
                        f"Published SBG GPS: {lat}, {lon}, {alt}"
                    )

                # -------- UBLOX INPUT --------
                ublox_input = input(
                    "Ublox NavSatFix (lat lon alt) or ENTER to skip: "
                )

                if ublox_input.strip() != "":
                    lat, lon, alt = map(float, ublox_input.split())

                    fix_msg = NavSatFix()

                    fix_msg.latitude = lat
                    fix_msg.longitude = lon
                    fix_msg.altitude = alt

                    self.ublox_pub.publish(fix_msg)

                    self.get_logger().info(
                        f"Published UBLOX Fix: {lat}, {lon}, {alt}"
                    )

            except Exception as e:
                self.get_logger().error(f"Input error: {e}")


def main(args=None):

    rclpy.init(args=args)

    node = DualGpsPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
