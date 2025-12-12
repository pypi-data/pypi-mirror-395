import time
import enum
from ...comms import CommsManager, SocketResult, CanOverloadError
from ...comms.system import get_all_physical_can_interfaces
import math
import struct
from typing import List, Tuple, Union, TypedDict, NamedTuple, Any, Optional
import threading
import asyncio

DRY_RUN = True
DISABLE_HANDS = True

class TimestampedValue(NamedTuple):
    value: float
    timestamp: float


class RunMode(enum.Enum):
    Operation = 0
    Position = 1
    Speed = 2
    Current = 3


param_ids_by_name = {
    "run_mode": 0x7005,
    "iq_ref": 0x7006,
    "spd_ref": 0x700A,
    "limit_torque": 0x700B,
    "cur_kp": 0x7010,
    "cur_ki": 0x7011,
    "cur_fit_gain": 0x7014,
    "loc_ref": 0x7016,
    "limit_spd": 0x7017,
    "limit_cur": 0x7018,
    "mechpos": 0x7019,
    "iqf": 0x701A,
    "mechvel": 0x701B,
    "vbus": 0x701C,
    "loc_kp": 0x701E,
    "spd_kp": 0x701F,
    "spd_ki": 0x7020,
    "spd_filt_gain": 0x7021,
    "vel_max": 0x7024,  # default is 10rad/s
    "acc_set": 0x7025,  # default is 10rad/s^2
}


class MotorError(enum.Enum):
    Undervoltage = 1
    Overcurrent = 2
    Overtemp = 4
    MagneticEncodingFault = 8
    HallEncodingFault = 16
    Uncalibrated = 32


class MotorMode(enum.Enum):
    Reset = 0
    Calibration = 1
    Run = 2


params_names_by_id = {v: k for k, v in param_ids_by_name.items()}

INSPIRE_PROPERTIES_OFFSETS = {"force_set": 12}

INSPIRE_RIGHT_FINGERS = {
    "Gr00R": {
        "motor_id": 1496,
        "ip_address": "192.168.11.210",
        "motor_name": "Gp00R",
        "description": "Right thumb rotation finger",
    },
    "Gp01R": {
        "motor_id": 1494,
        "ip_address": "192.168.11.210",
        "motor_name": "Gp01R",
        "description": "Right thumb bending finger",
    },
    "Gp10R": {
        "motor_id": 1492,
        "ip_address": "192.168.11.210",
        "motor_name": "Gp10R",
        "description": "Right index finger",
    },
    "Gp20R": {
        "motor_id": 1490,
        "ip_address": "192.168.11.210",
        "motor_name": "Gp20R",
        "description": "Right middle finger",
    },
    "Gp30R": {
        "motor_id": 1488,
        "ip_address": "192.168.11.210",
        "motor_name": "Gp30R",
        "description": "Right ring finger",
    },
    "Gp40R": {
        "motor_id": 1486,    
        "ip_address": "192.168.11.210",
        "motor_name": "Gp40R",
        "description": "Right pinky finger",
    },
}

INSPIRE_LEFT_FINGERS = {
    "Gr00L": {
        "motor_id": 1496,
        "ip_address": "192.168.12.210",
        "motor_name": "Gp00L", 
        "description": "Left thumb rotation finger",
    },
    "Gp01L": {
        "motor_id": 1494,
        "ip_address": "192.168.12.210",
        "motor_name": "Gp01L",
        "description": "Left thumb bending finger",
    },
    "Gp10L": {
        "motor_id": 1492,
        "ip_address": "192.168.12.210",
        "motor_name": "Gp10L",
        "description": "Left index finger",
    },
    "Gp20L": {
        "motor_id": 1490,
        "ip_address": "192.168.12.210",
        "motor_name": "Gp20L",
        "description": "Left middle finger",
    },
    "Gp30L": {
        "motor_id": 1488,
        "ip_address": "192.168.12.210",
        "motor_name": "Gp30L",
        "description": "Left ring finger",
    },
    "Gp40L": {
        "motor_id": 1486,
        "ip_address": "192.168.12.210",
        "motor_name": "Gp40L",
        "description": "Left pinky finger",
    },
}

DEFAULT_MAX_FORCE = 500  # for safety purposes.

class InspireFingerJoint:

    def __init__(self, motor_id: int, ip_address: str, motor_name: str):
        self.motor_id = motor_id
        self.motor_name = motor_name
        self.ip_address = ip_address
        self.properties = {}
        self.comms = CommsManager()
        if not DISABLE_HANDS:
            self.set_max_force(DEFAULT_MAX_FORCE)

    def move_percentage(self, percentage: float):
        """
        Move the finger joint. 0% is fully closed, 100% is fully open.
        """
        # Record start time
        # start_time = time.time()
        self.comms.tcpsend_modbus(self.ip_address, 1, 255, 6, self.motor_id, int(percentage * 1000))
        time.sleep(0.01)
        # end_time = time.time()
        # print(f"Move {self.motor_name} to {percentage * 100}% in {end_time - start_time} seconds")

    def set_max_force(self, force: int):
        """
        Set the max force for the finger joint.
        """
        # Convert motor_id from bytes to int, add offset, then convert back to bytes
        force_set_id = int(self.motor_id) + INSPIRE_PROPERTIES_OFFSETS["force_set"]
        self.comms.tcpsend_modbus(self.ip_address, 1, 255, 6, force_set_id, force)
        time.sleep(0.005)


INSPIRE_RIGHT_FINGER_JOINTS_MAP = {}
INSPIRE_LEFT_FINGER_JOINTS_MAP = {}

if not DISABLE_HANDS:
    for motor_name, motor_info in INSPIRE_RIGHT_FINGERS.items():
        INSPIRE_RIGHT_FINGER_JOINTS_MAP[motor_name] = InspireFingerJoint(
            motor_info["motor_id"], motor_info["ip_address"], motor_info["motor_name"]
        )

    for motor_name, motor_info in INSPIRE_LEFT_FINGERS.items():
        INSPIRE_LEFT_FINGER_JOINTS_MAP[motor_name] = InspireFingerJoint(
            motor_info["motor_id"], motor_info["ip_address"], motor_info["motor_name"]
        )


class UnsafeCommandError(Exception):
    pass


class MotorConfig(TypedDict, total=False):
    max_torque: float  # Max torque in N
    max_position_dx: float  # positional difference in radians
    joint_limits: Tuple[float, float]  # joint limits in radians
    max_velocity: float  # Max velocity in radians / seconds


class SafeStopPolicy(enum.Enum):
    DISABLE_MOTORS = 1
    COMPLIANCE_MODE = 2


class FamilyConfig(TypedDict, total=False):
    safe_stop_policy: SafeStopPolicy


_MOTOR_NO_DEFAULT = object()


class Motor:
    def __init__(self, motor_id: int, motor_name: str, motor_config: MotorConfig = {}, can_interface: str = None):
        self.motor_id: int = motor_id
        self.motor_name: str = motor_name

        self.left_pos = None
        self.right_pos = None
        self.middle_pos = None
        self.total_range = None
        self.normalized_angle = (0, -1)

        self.family_name: Union[str, None] = None
        self.can_interface: Union[str, None] = can_interface
        self.properties: dict[str, TimestampedValue] = {}
        self.joint_limits = motor_config.get("joint_limits", None)

        if self.joint_limits is not None:
            if (
                self.joint_limits[0] < -math.pi
                or self.joint_limits[1] > math.pi
                and self.joint_limits[0] <= self.joint_limits[1]
            ):
                print("Warning: Joint limits must be from -pi to pi for ", motor_name)
        self.max_torque = motor_config.get("max_torque", None)
        self.max_position_dx = motor_config.get("max_position_dx", None)
        self.max_velocity = motor_config.get("max_velocity", None)
        self.run_mode = RunMode.Operation
        self.compliance_mode: bool = False
        self.target_position = 0
        self.last_compliance_pos = 0
        self.compliance_mode_torque_threshold = motor_config.get("compliance_mode_torque_threshold", 1.0)
        self.compliance_mode_dx = motor_config.get("compliance_mode_dx", 0.01)

        # TODO: properly initialize
        self.mode = (MotorMode.Reset, -1)
        self.angle = (0, -1)
        self.velocity = (0, -1)
        self.torque = (0, -1)
        self.temp = (0, -1)

    def update_feedback(
        self, angle: float, velocity: float, torque: float, temp: float, errors: List[MotorError], mode: MotorMode
    ):
        last_update = time.time()
        # Raw angle coming from the encoder.
        self.angle: TimestampedValue = TimestampedValue(angle, last_update)
        if self.middle_pos is not None:
            # Normalized angle useful for control the robot between different machines to account for encoder differences.
            self.normalized_angle = (angle - self.middle_pos, last_update)
        self.velocity: TimestampedValue = TimestampedValue(velocity, last_update)
        self.torque: TimestampedValue = TimestampedValue(torque, last_update)
        self.temp: TimestampedValue = TimestampedValue(temp, last_update)
        self.errors: tuple[List[MotorError], float] = (errors, last_update)
        self.mode: TimestampedValue = TimestampedValue(mode, last_update)  # Update mode from feedback

    def update_property(self, property_name: str, value: Union[float, int]):
        self.properties[property_name] = TimestampedValue(value, time.time())
    
    def get_property_value(self, property_name: str, default: Any = _MOTOR_NO_DEFAULT) -> Any:
        """Get the currently stored value for a property in this motor. 
        
        If the property is not found, return the default value. If the default value is not provided, raise a KeyError.
        """
        if property_name in self.properties:
            return self.properties[property_name].value
        if default is not _MOTOR_NO_DEFAULT:
            return default
        raise KeyError(f"Property {property_name} not found in motor {self.motor_name}")

    def get_property_timestamp(self, property_name: str, default: Any = _MOTOR_NO_DEFAULT) -> Any:
        """Get the timestamp of the currently stored value for a property in this motor. 
        
        If the property is not found, return the default value. If the default value is not provided, raise a KeyError.
        """
        if property_name in self.properties:
            return self.properties[property_name].timestamp
        if default is not _MOTOR_NO_DEFAULT:
            return default
        raise KeyError(f"Property {property_name} not found in motor {self.motor_name}")

    def is_safe_position_update(self, target_position: float) -> bool:
        if self.max_position_dx is not None:
            return abs(target_position - self.angle[0]) <= self.max_position_dx
        return True

    def update_target_position(self, target_position: float) -> None:
        """
        Used for safety purposes.
        If max_position_dx is set, the motor will be stopped if the position is outside the max_position_dx.
        """
        if self.compliance_mode:
            raise UnsafeCommandError("Commands are currently blocked because compliance mode is activated.")

        self.target_position = target_position

    def should_trigger_compliance_mode(self):
        if self.compliance_mode or self.mode[0] == MotorMode.Reset:
            return False

        if self.max_position_dx is not None:
            if abs(self.angle[0] - self.target_position) > self.max_position_dx:
                print(
                    f"Compliance mode triggered: Motor {self.motor_name} Position {self.angle[0]} is outside max position dx {self.max_position_dx} Target position {self.target_position}"
                )
                return True

        if self.max_torque is not None:
            if abs(self.torque[0]) > self.max_torque:
                print(
                    f"Compliance mode triggered: Motor {self.motor_name} Torque {self.torque[0]} is greater than max torque {self.max_torque}"
                )
                return True

        if self.joint_limits is not None:
            if self.angle[0] > self.joint_limits[1] or self.angle[0] < self.joint_limits[0]:
                print(
                    f"Compliance mode triggered: Motor {self.motor_name} Angle {self.angle[0]} is outside joint limits {self.joint_limits}"
                )
                return True

        if self.max_velocity is not None:
            if abs(self.velocity[0]) > self.max_velocity:
                print(
                    f"Compliance mode triggered: Motor {self.motor_name} Velocity {self.velocity[0]} is greater than max velocity {self.max_velocity}"
                )
                return True

        return False

MotorMap = dict[str, Motor]

class RobstrideMotorMsg(enum.Enum):
    Info = 0x00
    Control = 0x01
    Feedback = 0x02
    Enable = 0x03
    Disable = 0x04
    ZeroPos = 0x06
    SetID = 0x07
    ReadParam = 0x11
    WriteParam = 0x12


class OperationCommand:
    def __init__(self, motor_name_or_id: Union[str, int], target_torque, target_angle, target_velocity, kp, kd):
        self.motor_name_or_id = motor_name_or_id
        self.target_torque = target_torque
        self.target_angle = target_angle
        self.target_velocity = target_velocity
        self.kp = kp
        self.kd = kd


class MotorsManager:
    """
    Handles sending commands to and receiving feedback from motors.
    Handles caching the state of the motors.
    Abstractions to make it easy to work with motors.
    """

    def __init__(self) -> None:
        self.motors: MotorMap = {}
        # Create a map of motor IDs to motors for faster lookup
        self.motors_by_id: dict[int, Motor] = {}
        self.motor_families: dict[str, MotorMap] = {}
        self.motor_families_config: dict[str, FamilyConfig] = {}
        self.motor_families_compliance_threads: dict[str, threading.Thread] = {}
        self.comms = CommsManager()
        self.host_id = 0xFD
        self.comms.add_callback(lambda result: self.on_motor_message(result))

    def add_motors(self, motors_map: MotorMap, family_name: str, family_config: FamilyConfig = {}) -> None:
        self.motor_families[family_name] = motors_map
        self.motor_families_config[family_name] = family_config
        for motor_name, motor in motors_map.items():
            self.motors_by_id[motor.motor_id] = motor
            self.motors[motor_name] = motor
            motor.family_name = family_name
    
    def find_motors(self, motor_names: Optional[List[str]] = None) -> None:
        """Find the motors on the physical CAN interfaces.
        
        If motor_names is not provided, find all motors in the motors map.
        """
        if motor_names is None:
            motor_names = list(self.motors.keys())
        
        for motor_name in motor_names:
            motor = self.motors[motor_name]
            if motor.can_interface is None:
                for can_interface in get_all_physical_can_interfaces():
                    try:
                        motor.can_interface = can_interface
                        motor.update_property("loc_ref", None)
                        self.read_param(motor_name, "loc_ref")
                        time.sleep(0.01)
                        if motor.properties["loc_ref"].value is not None:
                            break
                    except Exception as e:
                        pass
                else:
                    motor.can_interface = None
                    print(f"Warning: Could not find motor {motor_name} on any physical CAN interface")

    def stop_compliance_mode(self, family_name: str) -> None:
        family_motors = self.motor_families[family_name]
        for m in family_motors.values():
            m.compliance_mode = False
            self.disable(m.motor_name)
        # by setting it to None, trigger_compliance_mode will be called again from handle_msg from m.motor_name.
        del self.motor_families_compliance_threads[family_name]

    def compliance_mode_main(self, family_name: str) -> None:
        family_motors = self.motor_families[family_name]
        while True:
            for m in family_motors.values():
                if m.compliance_mode == False:
                    return  # exit.

                if abs(m.torque[0]) > m.compliance_mode_torque_threshold:
                    proposed_new_pos = m.last_compliance_pos + m.torque[0] * -m.compliance_mode_dx
                    if m.joint_limits is None:
                        m.last_compliance_pos = proposed_new_pos
                    elif m.joint_limits[0] <= proposed_new_pos and m.joint_limits[1] >= proposed_new_pos:
                        m.last_compliance_pos = proposed_new_pos
                # self.write does a time.sleep(0.0002) for each motor.
                self.write_param(m.motor_name, "loc_ref", m.last_compliance_pos, force_run=True)
                # time.sleep(0.01)

    def trigger_compliance_mode(self, family_name: str) -> None:
        # disable all motors
        family_motors = self.motor_families[family_name]
        safe_stop_policy = self.motor_families_config[family_name].get(
            "safe_stop_policy", SafeStopPolicy.COMPLIANCE_MODE
        )
        for m in family_motors.values():
            m.compliance_mode = True
            self.disable(m.motor_name)
            if safe_stop_policy == SafeStopPolicy.COMPLIANCE_MODE:
                self.set_run_mode(m.motor_name, RunMode.Position)
                self.enable(m.motor_name)
                self.write_param(m.motor_name, "loc_ref", m.angle[0] - m.velocity[0] * 0.01, force_run=True)
                m.last_compliance_pos = m.angle[0] - m.velocity[0] * 0.01

        if family_name not in self.motor_families_compliance_threads:
            thread = threading.Thread(target=self.compliance_mode_main, args=(family_name,), daemon=True)
            self.motor_families_compliance_threads[family_name] = thread
            thread.start()

    def on_feedback_message(self, can_id: int, motor_id: int, data: bytes):
        # Find the corresponding motor
        target_motor: Motor = None
        for motor in self.motors.values():
            if motor.motor_id == motor_id:
                target_motor = motor
                break
        else:
            return
        
        # Parse error bits and mode from arbitration ID
        error_bits = (can_id & (0x1F0000 << 2)) >> 16
        errors = []
        for i in range(6):
            value = 1 << i
            if value & error_bits:
                errors.append(MotorError(value))

        mode = MotorMode((can_id & (0x300000 << 2)) >> 22)
        
        # Convert values using same scaling as robstride_client
        angle_raw = int.from_bytes(data[0:2], "big")
        angle = (float(angle_raw) / 65535 * 8 * math.pi) - 4 * math.pi

        velocity_raw = int.from_bytes(data[2:4], "big")
        velocity_range = 88  # Assuming motor_model 1
        velocity = (float(velocity_raw) / 65535 * velocity_range) - velocity_range / 2

        torque_raw = int.from_bytes(data[4:6], "big")
        torque_range = 34  # Assuming motor_model 1
        torque = (float(torque_raw) / 65535 * torque_range) - torque_range / 2

        temp_raw = int.from_bytes(data[6:8], "big")
        temp = float(temp_raw) / 10

        # Update the motor's feedback values
        old_mode = target_motor.mode[0]
        target_motor.update_feedback(angle, velocity, torque, temp, errors, mode)
        if target_motor.should_trigger_compliance_mode() and old_mode != MotorMode.Reset:
            self.trigger_compliance_mode(target_motor.family_name)
        
    def on_read_message(self, can_id: int, motor_id: int, data: bytes):
        # Extract parameter ID and value
        param_id = int.from_bytes(data[:2], 'little', signed=False)  # First 2 bytes are param ID
        # Special handling for run_mode parameter (0x7005)
        if param_id == 0x7005:
            value = int(data[4])  # Run mode is a single byte value
        else:
            value = struct.unpack("<f", data[4:8])[0]  # Float value in last 4 bytes
        self.motors_by_id[motor_id].update_property(params_names_by_id[param_id], value)

    def on_motor_message(self, result: SocketResult) -> None:
        # Parse the arbitration ID to get message type and motor ID
        # CAN ID format in hex string: "0280FD73"
        #   msg[0:2] = message type (bits 24-31)
        #   msg[2:4] = error bits + mode (bits 16-23)
        #   msg[4:6] = sender id (bits 8-15)
        #   msg[6:8] = receiver id (bits 0-7)
        msg_type = (result.can_id & 0x1F00_0000) >> 24
        motor_id = (result.can_id & 0x0000_FF00) >> 8

        # Only process feedback messages (type 2)
        if msg_type == RobstrideMotorMsg.Feedback.value:
            self.on_feedback_message(result.can_id, motor_id, result.data)
        elif msg_type == RobstrideMotorMsg.ReadParam.value and motor_id != self.host_id:
            self.on_read_message(result.can_id, motor_id, result.data)

    def get_motor(self, motor_name_or_id: Union[str, int]) -> Motor:
        if isinstance(motor_name_or_id, str):
            return self.motors[motor_name_or_id]
        else:
            return self.motors_by_id[motor_name_or_id]
    
    def _default_can_id(self, op: RobstrideMotorMsg, motor_id: int) -> int:
        return (op.value << 24) | (self.host_id << 8) | motor_id

    def enable(self, motor_name_or_id: Union[str, int]):
        try:
            motor = self.get_motor(motor_name_or_id)
            can_id = self._default_can_id(RobstrideMotorMsg.Enable, motor.motor_id)
            self.comms.cansend(motor.can_interface, True, can_id, bytes([0] * 8))
        except Exception as e:
            print(f"[ERROR MotorsManager.enable]: Exception occurred: {e}")
            import traceback

            traceback.print_exc()
            raise

    def disable(self, motor_name_or_id: Union[str, int]):
        motor = self.get_motor(motor_name_or_id)
        can_id = self._default_can_id(RobstrideMotorMsg.Disable, motor.motor_id)
        self.comms.cansend(motor.can_interface, True, can_id, bytes([0] * 8))

    def zero_position(self, motor_name_or_id: Union[str, int]):
        motor = self.get_motor(motor_name_or_id)
        can_id = self._default_can_id(RobstrideMotorMsg.ZeroPos, motor.motor_id)
        self.comms.cansend(motor.can_interface, True, can_id, bytes([0x01] + [0] * 7))

    def read_param_sync(self, motor_name_or_id: Union[str, bytes], param_id: Union[int, str]) -> float:
        motor = self.get_motor(motor_name_or_id)
        update_time = time.time()

        self.read_param(motor_name_or_id, param_id)
        time.sleep(0.001)
        retry_cnt = 50
        max_retry_cnt = 0
        while motor.get_property_timestamp(param_id, default=-1) < update_time:
            time.sleep(0.001)
            retry_cnt -= 1
            if retry_cnt <= 0:
                self.read_param(motor_name_or_id, param_id)    
                retry_cnt = 50
            max_retry_cnt += 1
            if max_retry_cnt > 25:
                raise TimeoutError(f"Failed to read parameter {param_id} within timeout")
        return motor.get_property_value(param_id)

    async def read_param_async(self, motor_name_or_id: Union[str, bytes], param_id: Union[int, str]) -> float:
        """
        Asynchronously reads a motor parameter, waiting for the value to be updated.
        Replaces blocking time.sleep with non-blocking asyncio.sleep.
        """

        # 1. Initial setup and parameter read
        motor = self.get_motor(motor_name_or_id)

        # Use time.monotonic() for sleep/timeout checks, as it's not affected by system clock changes.
        start_time = time.monotonic()
        # The 'update_time' from the original code: get the current time before requesting the update.
        update_time = time.time()

        # Initiate the read request (assuming self.read_param is already non-blocking or schedules a background action)
        self.read_param(motor_name_or_id, param_id)

        # Initial pause and setup
        await asyncio.sleep(0.001)  # Replace the first time.sleep(0.01) with non-blocking asyncio.sleep
        retry_cnt = 5
        max_retry_cnt = 0

        # Define the maximum total time to wait for the parameter to update (e.g., 0.5 seconds, as 25 * 0.02 is 0.5s total wait)
        # The original logic used 25 iterations of the main loop. With an inner sleep of 0.01s and an outer sleep/read sequence,
        # it's best to rely on a total timeout based on time.monotonic() rather than a fixed retry count.
        # We will stick close to the original retry/max_retry logic, but use a more explicit maximum duration for robustness.

        # 2. Asynchronous Polling Loop
        while motor.get_property_timestamp(param_id, default=-1) < update_time:

            # Replace time.sleep(0.01) with non-blocking asyncio.sleep
            await asyncio.sleep(0.001)

            retry_cnt -= 1

            if retry_cnt <= 0:
                # Re-request the parameter read
                self.read_param(motor_name_or_id, param_id)
                retry_cnt = 5

            max_retry_cnt += 1

            # Original maximum loop count check (25 * 0.02s delay approx = 0.5s total wait)
            if max_retry_cnt > 25:
                # If a TimeoutError is raised, it's better to use the time-based check below,
                # but for a direct reimplementation, we keep the original logic.
                raise TimeoutError(f"Failed to read parameter {param_id} within timeout")

        # 3. Return the updated parameter value
        return motor.get_property_value(param_id, default=-1)

    def read_param(self, motor_name_or_id: Union[str, int], param_id: Union[int, str]) -> float:
        """Read a parameter from the specified motor."""
        motor = self.get_motor(motor_name_or_id)

        # Convert string param_id to int if needed
        if isinstance(param_id, str):
            param_id = param_ids_by_name[param_id]
        
        can_id = self._default_can_id(RobstrideMotorMsg.ReadParam, motor.motor_id)
        self.comms.cansend(motor.can_interface, True, can_id, param_id.to_bytes(2, 'little') + bytes([0] * 6))
        # Note: Response handling will be done by on_motor_message callback
        
    def set_run_mode(self, motor_name_or_id: Union[str, int], run_mode: RunMode):
        motor = self.get_motor(motor_name_or_id)
        self.write_param(motor_name_or_id, "run_mode", run_mode.value)
        motor.run_mode = run_mode

    def write_param(self, motor_name_or_id: Union[str, int], param_id: Union[int, str], param_value: Union[float, int], force_run=False) -> None:
        """Write a parameter value to the specified motor.

        force_run: should only be set to true when running commands from compliance mode. Otherwise, it defeats the safety purposes of compliance mode.
        """
        motor = self.get_motor(motor_name_or_id)

        # Convert string param_id to int if needed
        if isinstance(param_id, str):
            param_id = param_ids_by_name[param_id]

        # Prepare the parameter data
        param_bytes = param_id.to_bytes(2, 'little') + bytes([0] * 2)

        # Handle special case for run_mode (0x7005)
        if param_id == 0x7005:
            value_bytes = bytes([int(param_value), 0, 0, 0])
            motor.run_mode = RunMode(param_value)
        else:
            value_bytes = struct.pack("<f", param_value)
            
        data = param_bytes + value_bytes
        if not force_run and param_id == param_ids_by_name["loc_ref"]:
            if motor.is_safe_position_update(param_value):
                motor.update_target_position(param_value)  # can raise an exception to cancel the run.
            else:
                self.trigger_compliance_mode(motor.family_name)
                raise UnsafeCommandError(f"Safety Error: Target position {param_value} is too far from current position {motor.angle[0]} (max dx: {motor.max_position_dx})") # stop the program safely.

        can_id = self._default_can_id(RobstrideMotorMsg.WriteParam, motor.motor_id)

        try:
            self.comms.cansend(motor.can_interface, True, can_id, data)
        except CanOverloadError:
            time.sleep(0.01)
            self.comms.cansend(motor.can_interface, True, can_id, data)
        
    def operation_command(self, motor_name_or_id: Union[str, int], target_torque: float, target_angle: float, target_velocity: float, kp: float, kd: float):
        """ target_torque range (-60Nm to 60Nm)"""
        can_id, data, can_interface = self.operation_batch_command(motor_name_or_id, target_torque, target_angle, target_velocity, kp, kd, apply_target_position=True)
        self.comms.cansend(can_interface, True, can_id, data)

    def operation_batch_command(self, motor_name_or_id: Union[str, int], target_torque: float, target_angle: float, target_velocity: float, kp: float, kd: float, apply_target_position: bool = True):
        """
        apply_target_position: if True, the target position will be applied to the motor.
        """
        motor = self.get_motor(motor_name_or_id)

        torque_in_65535 = int(((target_torque + 60) / 120) * 65535)

        angle_in_65535 = int(((target_angle + 4 * math.pi) / (8 * math.pi)) * 65535)
        velocity_in_65535 = int(((target_velocity + 15) / 30) * 65535)
        kp_in_65535 = int(((kp) / 5000) * 65535)
        kd_in_65535 = int(((kd) / 100) * 65535)

        target_angle_bytes = angle_in_65535.to_bytes(2, 'big')
        target_velocity_bytes = velocity_in_65535.to_bytes(2, 'big')
        target_kp_bytes = kp_in_65535.to_bytes(2, 'big')
        target_kd_bytes = kd_in_65535.to_bytes(2, 'big')

        data = target_angle_bytes + target_velocity_bytes + target_kp_bytes + target_kd_bytes
        if apply_target_position:
            if motor.is_safe_position_update(target_angle):
                motor.update_target_position(target_angle)  # can raise an exception to cancel the run.
            else:
                self.trigger_compliance_mode(motor.family_name)
                raise UnsafeCommandError(f"Safety Error: Target position {target_angle} is too far from current position {motor.angle[0]} (max dx: {motor.max_position_dx})") # stop the program safely.

        can_id = self._default_can_id(RobstrideMotorMsg.Control, motor.motor_id)
        return ((can_id & 0xFF00_00FF) | (torque_in_65535 << 8), data, motor.can_interface)

    def send_operation_commands(self, operation_commands: List[OperationCommand]):
        for operation_command in operation_commands:
            can_id, data, can_interface = self.operation_batch_command(
                operation_command.motor_name_or_id,
                operation_command.target_torque,
                operation_command.target_angle,
                operation_command.target_velocity,
                operation_command.kp,
                operation_command.kd,
                apply_target_position=True,
            )
            self.comms.cansend(can_interface, True, can_id, data)

    def get_range(
        self,
        motor_name,
        start_pos=None,
        step_size=0.01,
        step_time=0.01,
        max_torque=4.5,
        expected_range=math.pi,
        verbose=False,
    ):
        motor = self.motors[motor_name]
        self.set_run_mode(motor_name, RunMode.Position)
        self.enable(motor_name)
        if start_pos is None:
            self.read_param(motor_name, "loc_ref")
            time.sleep(step_time)
            curr_pos = motor.properties["loc_ref"][0]
            start_pos = curr_pos
        else:
            curr_pos = start_pos
        while True:
            curr_pos += step_size
            self.write_param(motor_name, "loc_ref", curr_pos)
            time.sleep(step_time)
            if verbose:
                print("torque, angle", motor.torque[0], motor.angle[0], curr_pos)
            if abs(motor.torque[0]) > max_torque:
                left_pos = motor.angle[0]
                if verbose:
                    print("final_mech_pos 1", motor.angle[0], curr_pos)
                print("trying to go to left position", left_pos - (expected_range * 0.8))
                self.write_param(motor_name, "loc_ref", left_pos - (expected_range * 0.8))
                time.sleep(1.0)
                break

        curr_pos = left_pos - (expected_range * 0.8)

        while True:
            curr_pos -= step_size
            self.write_param(motor_name, "loc_ref", curr_pos)
            time.sleep(step_time)
            if verbose:
                print("torque, angle", motor.torque[0], motor.angle[0])
            if abs(motor.torque[0]) > max_torque:
                right_pos = motor.angle[0]
                if verbose:
                    print("final_mech_pos 2", motor.angle[0])
                break

        middle_pos = (left_pos + right_pos) / 2

        self.write_param(motor_name, "loc_ref", middle_pos)
        time.sleep(2.5)

        return left_pos, right_pos, middle_pos, abs(left_pos) + abs(right_pos)
