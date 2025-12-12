import math
from .steppable_system import SteppableSystem

from .neck_platform import NeckPlatform
from .motors.motors_manager import MotorsManager, Motor, RunMode, OperationCommand
import time
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

NECK_CAN_INTERFACE = b"can3"  # can3 is the can interface for the neck motors
MAX_VELOCITY = 5.24  # max under rated load is 10.47 rad/s
MAX_TORQUE = 2.0  # max peak torque (peak load) is 5.5 Nm, 1.6 Nm is the rated load


class HoaRobstrideNeckPlatform(NeckPlatform):
    MIN_YAW_ANGLE = math.pi * -1 / 2
    MAX_YAW_ANGLE = math.pi * 1 / 2
    MIN_PITCH_ANGLE = 0
    MAX_PITCH_ANGLE = 120 * math.pi / 180
    YAW_MOTOR_NAME = "NwC"
    PITCH_MOTOR_NAME = "NpC"

    def __init__(self, motors_manager: MotorsManager):
        super().__init__()
        self.motors_manager = motors_manager
        # self.operating_frequency = 100
        self.enabled = False
        self.is_calibrated = False
        self.motors = {
            self.PITCH_MOTOR_NAME: Motor(
                b"30",
                # NECK_CAN_INTERFACE,
                b"can0",
                self.PITCH_MOTOR_NAME,
                # ,
                # {
                #     # "joint_limits": [],  # Pitch range: approximately -32 to +90 degrees
                #     "max_torque": MAX_TORQUE,
                #     "max_velocity": MAX_VELOCITY,
                #     "compliance_mode_torque_threshold": 1.5,
                #     "compliance_mode_dx": 0.001,
                # },
            ),
            self.YAW_MOTOR_NAME: Motor(
                b"31",
                # NECK_CAN_INTERFACE,
                b"can1",
                self.YAW_MOTOR_NAME,
                # ,
                # {
                #     # "joint_limits": [],  # Yaw range: -90 to +90 degrees
                #     "max_torque": MAX_TORQUE,
                #     "max_velocity": MAX_VELOCITY,
                #     "compliance_mode_torque_threshold": 1.5,
                #     "compliance_mode_dx": 0.001,
                # },
            ),
        }
        # Initialize neck motors
        self.motors_manager.add_motors(
            self.motors,
            "neck",
        )
        # self.recover_motors()
        self.enable_motors()

    def enable_motors(self):
        for motor_name in self.motors:
            self.motors_manager.enable(motor_name)

    def disable_motors(self):
        self.motors_manager.write_param(self.PITCH_MOTOR_NAME, "loc_ref", self.motors[self.PITCH_MOTOR_NAME].left_pos)
        self.motors_manager.write_param(self.YAW_MOTOR_NAME, "loc_ref", self.motors[self.YAW_MOTOR_NAME].middle_pos)
        time.sleep(1)
        for motor_name in self.motors:
            self.motors_manager.disable(motor_name)

    def _step(self):
        pass

    def set_movement_profile(self, motor_name, max_velocity, max_acceleration, max_jerk):
        # need to set vel_max, acc_set
        self.motors_manager.write_param(motor_name, "vel_max", max_velocity)
        self.motors_manager.write_param(motor_name, "acc_set", max_acceleration)

    def move(self, pitch_in_degrees=None, yaw_in_degrees=None):

        if pitch_in_degrees is not None:
            pitch_in_radians = pitch_in_degrees * math.pi / 180
            if pitch_in_radians > self.MAX_PITCH_ANGLE or pitch_in_radians < self.MIN_PITCH_ANGLE:
                raise ValueError(f"Pitch in degrees {pitch_in_degrees} is out of range")
            self.motors_manager.write_param(
                "NpC", "loc_ref", self.motors[self.PITCH_MOTOR_NAME].left_pos - pitch_in_radians
            )
        if yaw_in_degrees is not None:
            yaw_in_radians = yaw_in_degrees * math.pi / 180
            if yaw_in_radians > self.MAX_YAW_ANGLE or yaw_in_radians < self.MIN_YAW_ANGLE:
                raise ValueError(f"Yaw in degrees {yaw_in_degrees} is out of range")
            self.motors_manager.write_param(
                "NwC", "loc_ref", self.motors[self.YAW_MOTOR_NAME].middle_pos + yaw_in_radians
            )

    def recalibrate(self):
        for motor_name in [self.PITCH_MOTOR_NAME, self.YAW_MOTOR_NAME]:
            expected_range = (
                math.pi if motor_name == self.YAW_MOTOR_NAME else self.MAX_PITCH_ANGLE - self.MIN_PITCH_ANGLE
            )
            motor = self.motors[motor_name]
            left_pos, right_pos, middle_pos, total_range = self.motors_manager.get_range(
                motor_name, max_torque=1.5, step_time=0.05, expected_range=expected_range, verbose=False
            )
            if motor_name == self.YAW_MOTOR_NAME:
                self.motors_manager.disable(motor_name)
                self.motors_manager.zero_position(motor_name)
                time.sleep(0.2)

            else:
                self.motors_manager.write_param(motor_name, "loc_ref", left_pos)
                time.sleep(2.5)
                self.motors_manager.disable(motor_name)
                self.motors_manager.zero_position(motor_name)
                time.sleep(0.2)

            motor.left_pos, motor.right_pos, motor.middle_pos, motor.total_range = self.motors_manager.get_range(
                motor_name, max_torque=1.5, step_time=0.05, expected_range=expected_range, verbose=False
            )
            self.motors_manager.write_param(motor_name, "loc_ref", motor.left_pos - (math.pi / 2))

    async def get_position(self, force_update: bool = False):
        if force_update:
            pass
            # TODO: make it non-blocking, no time.sleep, ping the motors for the updated angle
        return {"NpC": self.motors_manager.motors["NpC"].angle, "NwC": self.motors_manager.motors["NwC"].angle}

    async def get_state(self, motor_name, property):
        pass

    async def health_check(self):
        pass

    def on_abort(self):
        self.disable_motors()


class RobstrideNeckPlatform(SteppableSystem):
    MIN_PITCH_ANGLE = -2.13
    MAX_PITCH_ANGLE = 0.2  # 0 should be head in down position
    MIN_YAW_ANGLE = -3.14
    MAX_YAW_ANGLE = 0.2

    def __init__(self, motors_manager: MotorsManager):
        """
        Initialize the Robstride neck platform with NwC (neck yaw) and NpC (neck pitch) motors.

        NpC: Neck pitch control motor motor ID 30
        NwC: Neck yaw control motor motor ID 31

        """
        self.motors_manager = motors_manager
        self.operating_frequency = 100
        self.enabled = False
        self.is_calibrated = False

        # Initialize neck motors
        self.motors_manager.add_motors(
            {
                "NpC": Motor(
                    b"30",
                    # NECK_CAN_INTERFACE,
                    b"can0",
                    "NpC",
                    {
                        # "joint_limits": [],  # Pitch range: approximately -32 to +90 degrees
                        "max_torque": MAX_TORQUE,
                        "max_velocity": MAX_VELOCITY,
                        "compliance_mode_torque_threshold": 1.5,
                        "compliance_mode_dx": 0.001,
                    },
                ),
                "NwC": Motor(
                    b"31",
                    # NECK_CAN_INTERFACE,
                    b"can1",
                    "NwC",
                    {
                        # "joint_limits": [],  # Yaw range: -90 to +90 degrees
                        "max_torque": MAX_TORQUE,
                        "max_velocity": MAX_VELOCITY,
                        "compliance_mode_torque_threshold": 1.5,
                        "compliance_mode_dx": 0.001,
                    },
                ),
            },
            "neck",
        )

        # Store references to motors for easy access
        self.nwc = self.motors_manager.motors["NwC"]
        self.npc = self.motors_manager.motors["NpC"]

    def _step(self):
        """Step function for the neck platform."""
        pass

    def health_check(self, motor_name: str):
        """
        Checks if the neck motors are receiving and responding.
        Reads parameters to update motor state without enabling motors.
        Returns temperature, torque, angle, and velocity of the motors.

        Note: Motors may send periodic feedback messages even when disabled.
        This function reads parameters explicitly to ensure fresh data.
        """
        # Request parameter reads to trigger updates (these update motor.properties)
        # These will update motor.properties with fresh values
        self.motors_manager.read_param(motor_name, "mechpos")
        self.motors_manager.read_param(motor_name, "loc_ref")
        self.motors_manager.read_param(motor_name, "mechvel")
        self.motors_manager.read_param(motor_name, "iqf")  # current

        # Small delay to allow CAN responses to be processed
        time.sleep(0.1)

        # Helper to safely get property value
        def get_prop_value(motor, prop_name):
            """Safely get property value, returning None if not available"""
            if prop_name in motor.properties:
                prop_value = motor.properties[prop_name]
                if isinstance(prop_value, tuple) and len(prop_value) >= 1:
                    return prop_value[0]
                return prop_value
            return None

        # Helper to safely get property timestamp
        def get_prop_timestamp(motor, prop_name):
            """Safely get property timestamp, returning None if not available"""
            if prop_name in motor.properties:
                prop_value = motor.properties[prop_name]
                if isinstance(prop_value, tuple) and len(prop_value) == 2:
                    return prop_value[1]
            return None

        return {
            motor_name: {
                "iqf": get_prop_value(self.motors_manager.motors[motor_name], "iqf"),
                "mechpos": get_prop_value(self.motors_manager.motors[motor_name], "mechpos"),
                "loc_ref": get_prop_value(self.motors_manager.motors[motor_name], "loc_ref"),
                "velocity": get_prop_value(self.motors_manager.motors[motor_name], "mechvel"),
                "last_updated_seconds_ago": (
                    round(
                        time.time() - get_prop_timestamp(self.motors_manager.motors[motor_name], "iqf"),
                        2,
                    )
                    if get_prop_timestamp(self.motors_manager.motors[motor_name], "iqf") is not None
                    else None
                ),
            },
        }

    def enable_motors(self):
        self.motors_manager.enable("NpC")
        self.motors_manager.enable("NwC")

    def disable_motors(self):
        self.motors_manager.disable("NpC")
        self.motors_manager.disable("NwC")

    def operation_mode_enable_motors(self):
        self.motors_manager.set_run_mode("NpC", RunMode.Operation)
        self.motors_manager.set_run_mode("NwC", RunMode.Operation)
        self.enable_motors()

    # everytime neck is activated, run caibration sequence and center motors. Then will be able to be controlled within joint limits.

    def _calibrate_pitch(self):
        STEP_SIZE = 0.01

        # run health check here to make sure motors are responding
        health_check = self.health_check("NpC")
        # check if last updated seconds ago is less than 0.2 seconds
        if (
            health_check["NpC"]["last_updated_seconds_ago"] is not None
            and health_check["NpC"]["last_updated_seconds_ago"] > 0.2
        ):
            raise ValueError("NpC last updated over 0.2 seconds ago, motor may not be responding")

        # set motors to position mode and zero position
        self.motors_manager.set_run_mode("NpC", RunMode.Position)
        self.motors_manager.zero_position("NpC")

        self.motors_manager.enable("NpC")

        # Read current position from properties
        self.motors_manager.read_param("NpC", "loc_ref")
        time.sleep(0.1)  # Wait for response
        current_pitch_position = self.npc.properties["loc_ref"][0]

        # move pitch to top most position before hitting hardstop
        while True:
            current_pitch_position += STEP_SIZE  # move downwards
            self.motors_manager.write_param("NpC", "loc_ref", current_pitch_position)
            time.sleep(0.05)  # Wait for feedback to update

            # Get torque and angle from motor feedback
            motor = self.npc
            torque = motor.torque[0] if isinstance(motor.torque, tuple) else motor.torque
            angle = motor.angle[0] if isinstance(motor.angle, tuple) else motor.angle
            print("Torque: ", torque, "Angle: ", angle)

            if abs(torque) > 0.75:
                self.motors_manager.disable("NpC")
                time.sleep(0.2)
                print("Final pitch bottom position loc_ref", current_pitch_position)
                self.motors_manager.zero_position("NpC")
                break
            # time.sleep(0.05)

        self.motors_manager.read_param("NpC", "mechpos")
        time.sleep(0.1)
        current_pitch_position = self.npc.properties["mechpos"][0]
        print("Final pitch bottom position mechpos", current_pitch_position)

        self.npc.joint_limits = [self.MIN_PITCH_ANGLE, self.MAX_PITCH_ANGLE]

    def _calibrate_yaw(self):
        STEP_SIZE = 0.01

        # run health check to make sure motors are responding
        health_check = self.health_check("NwC")
        # check if last updated seconds ago is less than 0.2 seconds
        if (
            health_check["NwC"]["last_updated_seconds_ago"] is not None
            and health_check["NwC"]["last_updated_seconds_ago"] > 0.2
        ):
            raise ValueError("NwC last updated over 0.2 seconds ago, motor may not be responding")

        self.motors_manager.set_run_mode("NwC", RunMode.Position)
        self.motors_manager.zero_position("NwC")

        self.motors_manager.enable("NwC")

        # Read current position from properties
        self.motors_manager.read_param("NwC", "loc_ref")
        time.sleep(0.1)

        current_yaw_position = self.nwc.properties["loc_ref"][0]

        # move yaw to right most position before hitting hardstop
        while True:
            current_yaw_position += STEP_SIZE
            self.motors_manager.write_param("NwC", "loc_ref", current_yaw_position)
            time.sleep(0.05)  # Wait for feedback to update
            # Get torque and angle from motor feedback
            motor = self.nwc
            torque = motor.torque[0] if isinstance(motor.torque, tuple) else motor.torque
            angle = motor.angle[0] if isinstance(motor.angle, tuple) else motor.angle
            print("Torque: ", torque, "Angle: ", angle)

            if abs(torque) > 1.0:
                self.motors_manager.disable("NwC")
                time.sleep(0.2)
                print("Final right loc_ref", current_yaw_position)
                # self.motors_manager.zero_position("NwC")
                break
            # time.sleep(0.05)

        self.motors_manager.read_param("NwC", "mechpos")
        time.sleep(0.1)
        current_yaw_position = self.nwc.properties["mechpos"][0]
        print("finished right position mechpos", current_yaw_position)
        right_position = current_yaw_position

        self.motors_manager.enable("NwC")

        # move yaw to left most position before hitting hardstop
        while True:
            current_yaw_position -= STEP_SIZE
            self.motors_manager.write_param("NwC", "loc_ref", current_yaw_position)
            time.sleep(0.05)  # Wait for feedback to update
            # Get torque and angle from motor feedback
            motor = self.nwc
            torque = motor.torque[0] if isinstance(motor.torque, tuple) else motor.torque
            angle = motor.angle[0] if isinstance(motor.angle, tuple) else motor.angle
            print("Torque: ", torque, "Angle: ", angle)

            if abs(torque) > 1.0:
                self.motors_manager.disable("NwC")
                time.sleep(0.2)
                print("Final left loc_ref", current_yaw_position)
                # self.motors_manager.zero_position("NwC")
                break
            # time.sleep(0.05)

        self.motors_manager.read_param("NwC", "mechpos")
        time.sleep(0.1)
        current_yaw_position = self.nwc.properties["mechpos"][0]
        print("finished left position loc_ref", current_yaw_position)

        left_position = current_yaw_position

        # calculate the middle position
        middle_position = (right_position + left_position) / 2
        print("middle position mechpos", middle_position)

        # Move to the middle position with a step size of STEP_SIZE
        self.motors_manager.enable("NwC")

        delta = middle_position - current_yaw_position
        step_size = STEP_SIZE if delta > 0 else -STEP_SIZE
        num_steps = int(np.ceil(abs(delta) / STEP_SIZE))
        for i in range(num_steps):
            target = current_yaw_position + (i + 1) * step_size
            if (step_size > 0 and target > middle_position) or (step_size < 0 and target < middle_position):
                target = middle_position
            self.motors_manager.write_param("NwC", "loc_ref", target)
            time.sleep(0.1)
        # Ensure the motor is exactly at the middle position
        self.motors_manager.write_param("NwC", "loc_ref", middle_position)
        time.sleep(0.1)

        # Disable the motor after reaching the middle position
        self.motors_manager.disable("NwC")
        time.sleep(0.2)
        self.motors_manager.zero_position("NwC")

        # Calculate joint limits relative to zero position (after zeroing at middle)
        # Limits are relative to the zero position, so subtract the middle position
        min_limit = left_position - middle_position
        max_limit = right_position - middle_position
        # self.nwc.joint_limits = [min_limit, max_limit]
        print(f"Set NwC joint limits (relative to zero): [{min_limit:.3f}, {max_limit:.3f}]")
        print(f"Total range: {max_limit - min_limit:.3f} radians")

    def recalibrate(self):
        self._calibrate_pitch()
        self._calibrate_yaw()
        self.is_calibrated = True

    def look_forward(self):
        if not self.is_calibrated:
            raise ValueError("Neck is not calibrated, please run recalibrate() first")
        self.operation_mode_enable_motors()
        self._go_to_positions({"NwC": 0.0, "NpC": -1.57}, 3.0, 300)

    def home_motors(self):
        self.motors_manager.set_run_mode("NwC", RunMode.Operation)
        self.motors_manager.set_run_mode("NpC", RunMode.Operation)
        self.enable_motors()
        self._go_to_positions({"NwC": 0.0, "NpC": 0.0}, 3.0, 300)
        self.disable_motors()

    def _create_cubic_spline(self, min_value, max_value, num_steps):
        x_points = [0, 1]

        y_points = [min_value, max_value]
        cs = CubicSpline(x_points, y_points, bc_type="clamped")
        x_steps = np.linspace(0, 1, num_steps)
        y_steps = cs(x_steps)
        return y_steps

    def _go_to_positions(self, motors_targets, total_time: float, hz: int):
        spline_map = {}
        for motor_name, target_position in motors_targets.items():
            spline_map[motor_name] = self._create_cubic_spline(
                self.motors_manager.motors[motor_name].target_position,
                target_position,
                int(total_time * hz),
            )

        for i in range(int(total_time * hz)):
            start_time = time.time()
            for motor_name, target_position in motors_targets.items():
                self.motors_manager.send_operation_commands(
                    [OperationCommand(motor_name, 0.0, spline_map[motor_name][i], 0.0, 75, 5)]
                )
                motor = self.motors_manager.motors[motor_name]

                # if i % 50 == 0 and motor_name in ['SpR', 'WpR', 'EpR']: #every 50 hz
                if i % 10 == 0 and motor_name in ["NwC", "NpC"]:
                    print(f"\n{motor_name} state at {i}hz:")
                    print(f"  Current Position: {motor.angle}")
                    print(f"  Temp: {motor.temp} (updated {time.time() - motor.temp[1]:.3f}s ago)")
                    print(f"  Torque: {motor.torque}")
                    print(f"  Velocity: {motor.velocity}")

            elapsed_time = time.time() - start_time
            if elapsed_time < 1.0 / hz:
                time.sleep(1.0 / hz - elapsed_time)
