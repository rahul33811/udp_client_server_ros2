ros2_adas_udp_interface
ROS2 package for receiving sensor/navigation UDP data and publishing it as ROS2 topics for ADAS and robotics applications.
🚀 Overview

ros2_adas_udp_interface is a ROS2 package that receives binary UDP packets from an external ADAS/vehicle navigation system and publishes decoded values into ROS2 topics.
It is designed for developers integrating robotics or autonomous driving systems with low-level hardware or simulators that output UDP telemetry.

The package contains a simple, reliable UDP server node written in Python, which:

✔ Listens to binary UDP packets
✔ Decodes ADAS navigation fields (position, velocity, orientation, status)
✔ Publishes ROS2 topics such as:

actor_state (custom message)

Actor_State (final velocity magnitude)
✔ Provides structured logging & data validation

This package can be used in autonomous driving R&D, ADAS prototyping, simulation systems, and vehicle telemetry analysis.

📦 Features

UDP server compatible with binary sensor/navigation packets

Batch A/B data parsing (IMU, GPS, Velocity, Orientation)

Batch S navigation status decoding

ROS2 publishers for processed data

Clean modular structure → easy to extend

Fully Python-based

Works on all ROS2 distros (Humble, Iron, Jazzy, etc.)

▶️ Running the Node
Start the UDP Server Node
