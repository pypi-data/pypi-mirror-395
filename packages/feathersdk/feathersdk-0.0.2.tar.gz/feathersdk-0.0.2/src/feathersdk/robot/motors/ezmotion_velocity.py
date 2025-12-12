# Run the motor on 48v
import canopen # pip install canopen
import time

# 10 max, -90,
ROTATION_POSITION = -10
MAX_ROTATIONS_PER_SECOND = 100

safe_range = [-100, 20]
if ROTATION_POSITION < safe_range[0] or ROTATION_POSITION > safe_range[1]:
    print("out of safe range")
    exit


network = canopen.Network()
network.connect(channel='can0', bustype="socketcan", bitrate=1000000)

# Default ID is 2
node = network.add_node(2, "/home/feather/Workspace/featheros/lib/motors/MMS760200-48-C2-1.eds")

# node.sdo[0x6040].raw = 0x0006


node.sdo[0x6040].raw = 0x0006

# Profile Velocity Mode
node.sdo[0x6060].raw = 3

# shutdown
node.sdo[0x6040].raw = 0x0006



# enable operation
node.sdo[0x6040].raw = 0x000F

# node.sdo[0x6040].raw = 0x0006
# target_pos = ROTATION_POSITION * 65536
# node.sdo[0x607A].raw = target_pos # set the destination position

# node.sdo[0x6081].raw = MAX_ROTATIONS_PER_SECOND * 65536 # max velocity

node.sdo[0x60FF].raw = 65536 * -5 # positive goes down, negative goes up.
node.sdo[0x6083].raw = 3276800  # max acceleration
node.sdo[0x6084].raw = 3276800 / 4 # max decceleration
# node.sdo[0x6071].raw = 3000

node.sdo[0x6040].raw = 0x001F # enable operation to new set point

i = 0
rps = 5

while True:
    try:
        if i % 10 == 0:
            print("=================== Decreasing speed ==================")
            if i > 0:
                rps = 0
            else:
                rps = 5
            node.sdo[0x60FF].raw = 65536 * -rps
            # node.sdo[0x6081].raw = rps * 65536
            # node.sdo[0x6083].raw = 3276800 / 4
            # node.sdo[0x6084].raw = 3276800 / 4
            # node.sdo[0x6040].raw = 0x001F

        status_word = node.sdo[0x6041].raw
        current_pos = node.sdo[0x6064].raw
        current_vel = node.sdo[0x606C].raw
        curr_torque = node.sdo[0x6077].raw
        if status_word & (1 << 10):
            print("Target reached", status_word, status_word & (1 << 10))
            print('curr', current_pos, current_vel, curr_torque)
            # break
        else:
            print(status_word, status_word & (1 << 10))
            print('curr', current_pos, curr_torque, current_vel)
    except Exception as e:
        print(e)
        pass
    time.sleep(0.01)
    i += 1
    if i > 100:
        break

node.sdo[0x6040].raw = 0x0006

network.disconnect()