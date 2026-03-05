import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float64
from sbg_driver.msg import SbgGpsPos
from math import radians, sin, cos, atan2, degrees


class AntennaTracker(Node):

    def __init__(self):
        super().__init__('antenna_tracker')

        self.my_lat = None
        self.my_lon = None

        self.target_lat = None
        self.target_lon = None

        self.yaw = None

        # antenna GPS
        self.create_subscription(
            NavSatFix,
            "/fix",
            self.antenna_gps_callback,
            10)

        # rover GPS
        self.create_subscription(
            SbgGpsPos,
            "/sbg/gps_pos",
            self.rover_gps_callback,
            10)

        # IMU yaw
        self.create_subscription(
            Float64,
            "/witmotion_eular/yaw",
            self.yaw_callback,
            10)

    # -------------------------
    # Rover GPS (target)
    # -------------------------
    def rover_gps_callback(self, msg: SbgGpsPos):
        self.target_lat = msg.latitude
        self.target_lon = msg.longitude

    # -------------------------
    # Antenna GPS (tracker)
    # -------------------------
    def antenna_gps_callback(self, msg: NavSatFix):
        self.my_lat = msg.latitude
        self.my_lon = msg.longitude

        self.compute_tracking()

    # -------------------------
    # Yaw from IMU
    # -------------------------
    def yaw_callback(self, msg: Float64):
        self.yaw = msg.data

    # -------------------------
    # Bearing calculation
    # -------------------------
    def bearing(self, curr_lat, curr_lon, target_lat, target_lon):

        target_lat, target_lon, curr_lat, curr_lon = map(
            radians,
            [target_lat, target_lon, curr_lat, curr_lon]
        )

        d_lon = target_lon - curr_lon

        return degrees(
            atan2(
                sin(d_lon) * cos(target_lat),
                cos(curr_lat) * sin(target_lat) -
                sin(curr_lat) * cos(target_lat) * cos(d_lon)
            )
        ) % 360

    # -------------------------
    # Compute antenna direction
    # -------------------------
    def compute_tracking(self):

        if None in [self.my_lat, self.my_lon,
                    self.target_lat, self.target_lon,
                    self.yaw]:
            return

        bearing_to_target = self.bearing(
            self.my_lat,
            self.my_lon,
            self.target_lat,
            self.target_lon
        )

        # antenna rotation needed
        rotation = bearing_to_target - self.yaw
        rotation = (rotation + 540) % 360 - 180

        self.get_logger().info(
            f"Bearing: {bearing_to_target:.2f}° | "
            f"Yaw: {self.yaw:.2f}° | "
            f"Rotate: {rotation:.2f}°"
        )


def main(args=None):

    rclpy.init(args=args)
    node = AntennaTracker()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
