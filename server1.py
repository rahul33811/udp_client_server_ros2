import rclpy
from rclpy.node import Node
import socket
import struct
import math
from std_msgs.msg import Float64

# Replace proprietary/custom message with a generic placeholder
# from atg_interfaces.msg import ActorState
from example_interfaces.msg import Float64MultiArray as ActorState


class UDPServerNode(Node):

    def __init__(self):
        super().__init__('udp_server_node')

        # Use ROS parameter for port instead of hardcoding
        self.declare_parameter('udp_port', 3000)
        self.udp_port = self.get_parameter('udp_port').value

        # UDP socket setup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.udp_port))

        # Publishers (topics generalized)
        self.final_velocity_pub = self.create_publisher(Float64, 'final_velocity', 10)
        self.actor_state_pub = self.create_publisher(ActorState, 'actor_state', 10)

    def parse_batch_a(self, data):
        """Parse inertial sensor batch (generalized)."""

        # General sensor parsing structure (units removed for safety)
        try:
            timestamp = struct.unpack('<H', data[0:2])[0]
            accel_x = struct.unpack('<h', data[2:4])[0]
            accel_y = struct.unpack('<h', data[4:6])[0]
            accel_z = struct.unpack('<h', data[6:8])[0]
            gyro_x = struct.unpack('<h', data[8:10])[0]
            gyro_y = struct.unpack('<h', data[10:12])[0]
            gyro_z = struct.unpack('<h', data[12:14])[0]

            # Minimal logging to avoid exposing raw sensor data
            self.get_logger().debug(f"Batch A parsed (timestamp={timestamp})")

        except struct.error:
            self.get_logger().warn("Failed to parse Batch A packet")

    def parse_batch_b(self, data):
        """Parse navigation/kinematic batch (generalized)."""

        try:
            # Values generalized — no GPS or sensitive units
            value_1 = struct.unpack('<d', data[0:8])[0]
            value_2 = struct.unpack('<d', data[8:16])[0]
            value_3 = struct.unpack('<f', data[16:20])[0]

            vx = struct.unpack('<h', data[20:22])[0]
            vy = struct.unpack('<h', data[22:24])[0]

            # Compute derived magnitude (non-sensitive)
            velocity_mag = math.sqrt(vx**2 + vy**2)

            # Publish derived value
            vel_msg = Float64()
            vel_msg.data = velocity_mag
            self.final_velocity_pub.publish(vel_msg)

            # Publish generalized structured data
            state_msg = ActorState()
            state_msg.data = [value_1, value_2, value_3, float(velocity_mag)]
            self.actor_state_pub.publish(state_msg)

            self.get_logger().debug("Batch B parsed successfully")

        except struct.error:
            self.get_logger().warn("Failed to parse Batch B packet")

    def run(self):
        """Main loop to receive and process UDP packets."""

        while rclpy.ok():
            try:
                data, addr = self.sock.recvfrom(128)  # Generic buffer size

                # Basic structural validation without exposing protocol
                if len(data) < 32:
                    self.get_logger().warn("Received incomplete packet")
                    continue

                # Process batches (format generalized)
                self.parse_batch_a(data[0:16])
                self.parse_batch_b(data[16:48])

            except BlockingIOError:
                pass
            except Exception as e:
                self.get_logger().error(f"Unexpected error: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = UDPServerNode()
    node.run()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
