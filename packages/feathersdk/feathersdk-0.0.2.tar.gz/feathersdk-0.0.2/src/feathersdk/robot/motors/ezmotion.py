# Run the motor on 48v
import canopen # pip install canopen
import time

# 10 max, -90,
ROTATION_POSITION = -50
MAX_ROTATIONS_PER_SECOND = 300

safe_range = [-100, 20]
if ROTATION_POSITION < safe_range[0] or ROTATION_POSITION > safe_range[1]:
    print("out of safe range")
    exit


network = canopen.Network()
network.connect(channel='can0', bustype="socketcan", bitrate=1000000)

# Default ID is 2
node = network.add_node(2, "/home/glorifiedstatistics/Workspace/featheros/lib/motors/MMS760200-48-C2-1.eds")

# node.sdo[0x6040].raw = 0x0006


node.sdo[0x6040].raw = 0x0006

# Profile Position Mode
node.sdo[0x6060].raw = 1

# shutdown
node.sdo[0x6040].raw = 0x0006

# enable operation
node.sdo[0x6040].raw = 0x000F

# node.sdo[0x6040].raw = 0x0006
target_pos = ROTATION_POSITION * 65536
node.sdo[0x607A].raw = target_pos # set the destination position

node.sdo[0x6081].raw = MAX_ROTATIONS_PER_SECOND * 65536 # max velocity
node.sdo[0x6083].raw = 3276800  # max acceleration
node.sdo[0x6084].raw = 3276800 / 4 # max decceleration
# node.sdo[0x6071].raw = 3000

node.sdo[0x6040].raw = 0x001F # enable operation to new set point

while True:
    status_word = node.sdo[0x6041].raw
    current_pos = node.sdo[0x6064].raw
    curr_torque = node.sdo[0x6077].raw
    if status_word & (1 << 10):
        print("Target reached", status_word, status_word & (1 << 10))
        print('curr', current_pos)
        break
    else:
        print(status_word, status_word & (1 << 10))
        print('curr', current_pos, curr_torque)
    time.sleep(0.01)

node.sdo[0x6040].raw = 0x0006

network.disconnect()