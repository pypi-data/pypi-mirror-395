Overview

This Python library provides a simple interface for controlling industrial robots over TCP/IP socket connections. The library handles communication, movement commands, and system initialization for robotic control systems.

Installation

Simply include the commands.py file in your project and import it:
from epsonrc.commands import connect, send, command, go, move, go_here, move_here, begin

Quick Start

# Connect to the robot controller
connect(HOST='10.0.0.1', PORT=5000)

# Initialize the system with default parameters
begin()

# Move to absolute coordinates
go(100, 50, 200)

# Execute a custom command
command("On 14")

Core Functions
Connection Management
connect(HOST='127.0.0.1', PORT=5000)
Establishes a connection to the robot controller.

Parameters:

HOST (str): IP address of the controller (default: '127.0.0.1')

PORT (int): Port number (default: 5000)

Returns: True if connection successful, False otherwise

Example:

if connect('192.168.1.100', 5000):
    print("Connected successfully")
else:
    print("Connection failed")

begin(speed=50, speeds=1000, accel=60, accels=200, weight=0, inertia=0, speedfactor=50, power='Low', homeset=[0,0,0,0,0,0])

Initializes the robot system with specified parameters Parameters:

speed (int): Base movement speed (default: 50)

speeds (int): S-axis rotation speed (default: 1000)

accel (int): Acceleration rate for linear axes (default: 60)

accels (int): Acceleration rate for rotation axis (default: 200)

weight (int): Payload weight (default: 0)

inertia (int): Inertia setting (default: 0)

speedfactor (int): Speed multiplier percentage (default: 50)

power (str): Power mode - 'Low' or 'High' (default: 'Low')

homeset (list): Home position coordinates (default: [0,0,0,0,0,0])

Example:

# Initialize with custom parameters
robot_control.begin(
    speed=75,
    speedfactor=80,
    power='High',
    homeset=[10, 20, 30, 0, -90, -90]
)

Movement Commands

go(x, y, z, u=0, v=-90, w=-90)

Moves to absolute coordinates with specified orientation.

Parameters:

x, y, z (float): Position coordinates

u, v, w (float): Orientation angles (default: 0, -90, -90)

Example:

# Move to position (100, 200, 300) with default orientation
go(100, 200, 300)

# Move with custom orientation
go(100, 200, 300, u=45, v=-45, w=0)
move(x, y, z, u=0, v=-90, w=-90)

Similar to go() but may use different motion planning depending on controller implementation.
go_here(x, y, z=0)
Moves relative to current position.

Parameters:

x, y, z (float): Relative movement distances

Example:

# Move 50mm in X, 100mm in Y from current position
robot_control.go_here(50, 100)

# Move with Z offset
robot_control.go_here(50, 100, 20)
move_here(x, y, z=0)
Similar to go_here() but may use different motion planning.

Communication Functions

send(string)
Sends a raw string command to the controller and receives response.

Parameters:

string (str): Command to send (without protocol framing)

Note: Automatically adds $ prefix and \r\n termination

Example:

response = robot_control.send("GetPosition")
command(string)
Sends an Execute command to the controller.

Parameters:

string (str): Command to execute

Note: Wraps command in $Execute,"command"\r\n

Example:

command("Speed 100")
command("Wait 1000")  # Wait 1 second

Complete Workflow Example

from epsonrc.commands import connect, send, command, go, move, go_here, move_here, begin
import time

# 1. Connect to controller
if not connect('192.168.1.100', 5000):
    print("Failed to connect. Exiting.")
    exit()

# 2. Initialize system
begin(
    speed=60,
    speedfactor=70,
    power='High'
)

# 3. Move to home position
go(0, 0, 0)

# 4. Execute a sequence of movements
positions = [
    (100, 50, 200),
    (150, 75, 180),
    (200, 100, 150)
]

for pos in positions:
    robot_control.go(*pos)
    time.sleep(0.5)  # Brief pause between movements

# 5. Move relative to current position
go_here(50, -25, 10)

# 6. Execute custom commands
command("On 14")  # Turn on tool
command("Wait 2")       # Wait 2 seconds
command("Pulse 50,50,100,200,15,25") # pulses in all joints

# 7. Return to home
command("Home")

Error Handling

The library includes basic error handling:

Connection timeout after 180 seconds

Automatic error reset during initialization

Print statements for debugging communication issues

Common Issues:

Connection timeout: Check network connectivity and controller status

No response: Verify correct IP address and port

Command errors: Ensure controller is in correct operational mode

Protocol Details

The library uses a simple text-based protocol:

Commands start with $ and end with \r\n

send() adds protocol framing automatically

command() wraps commands in Execute statements

All commands expect a response from the controller

Safety Notes

⚠️ Important Safety Considerations:

Emergency Stop: Always have an emergency stop procedure in place

Workspace Awareness: Ensure no obstacles in robot workspace

Speed Settings: Start with low speeds during testing

Weight Configuration: Properly configure weight parameters for payload

Home Position: Verify home position before starting operations

Manual Override: Keep controller manual override accessible

Troubleshooting

Issue	Possible Solution
Connection fails	Check firewall settings, verify controller IP
Commands timeout	Increase timeout in connect() function
Robot doesn't move	Check motor enable status, verify coordinates
Inaccurate positioning	Calibrate home position, check coordinate system
Support

For issues or questions:

Check controller documentation for supported commands

Verify network connectivity

Ensure proper robot calibration

Review command syntax in controller manual

Note: This library is designed for specific robot controllers. Command syntax and functionality may vary between different controller models. Always refer to your controller's documentation for complete command reference.