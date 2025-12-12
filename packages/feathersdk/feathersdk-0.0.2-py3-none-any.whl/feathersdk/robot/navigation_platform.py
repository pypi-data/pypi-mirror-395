from .steppable_system import SteppableSystem
from .motors.motors_manager import MotorsManager, Motor, MotorMode, RunMode, MotorMap
from ..comms.comms_manager import UnknownInterfaceError
from ..utils.trajectory import change_in_vel
import math
import numpy as np
import time
import enum
from abc import ABC, abstractmethod



class NavigationPlanner(ABC):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.target_x = 0
        self.target_y = 0
        self.target_theta = 0

    def reset(self):
        self.x = 0
        self.y = 0
        self.theta = 0

    @abstractmethod
    def is_at_target_position(self):
        return (
            math.isclose(self.x, self.target_x, abs_tol=0.001)
            and math.isclose(self.y, self.target_y, abs_tol=0.001)
            and math.isclose(self.theta, self.target_theta, abs_tol=0.001)
        )


class RemoteNavigationPlanner(NavigationPlanner):
    """A navigation planner that is remote-controlled by a user."""

    BRC_MOTOR_DIRECTION = -1  # -1 if shaft is facing left, 1 if shaft is facing right

    class DriveDirection(enum.Enum):
        FORWARD = 1
        BACKWARD = -1
        BREAK = 0

    def __init__(
        self, nav_platform, max_velocity, max_acceleration, max_jerk, max_rotation_velocity, max_rotation_acceleration
    ):
        super().__init__()
        self.current_wheel_angle = 0
        self.nav_platform = nav_platform
        self.operating_frequency = nav_platform.operating_frequency
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        # rad/s and rad/s2
        self.max_rotation_velocity = max_rotation_velocity
        self.max_rotation_acceleration = max_rotation_acceleration
        self.acceleration_ramp_time = self.max_acceleration / max_jerk
        self.acceleration_ramp_delta_velocity = change_in_vel(0, max_jerk, 0, self.acceleration_ramp_time)
        self.max_jerk = max_jerk
        self.delta_acceleration_hz = self.max_jerk / self.operating_frequency
        self.current_velocity = 0
        self.current_loc_ref = {"BpC": 0, "BpR": 0, "BpL": 0}
        self.current_acceleration = 0
        self.key_map = {
            "e": self.invoke_forward,
            "d": self.invoke_backward,
            "s": self.invoke_turn_left,
            "f": self.invoke_turn_right,
            "a": self.invoke_orient_left,
            "g": self.invoke_orient_right,
            "3": self.invoke_orient_forward,
            "c": self.invoke_orient_backward,
            "w": self.invoke_rotate_ccw,
            "r": self.invoke_rotate_cw,
            "p": self.invoke_debug,
        }
        self.last_drive_direction = (
            RemoteNavigationPlanner.DriveDirection.BREAK
        )  # 1 for forward, -1 for backward, 0 for break.
        self.last_drive_key = time.time()
        self.last_turn_key = time.time()
        self.is_rotating = False
        self.is_recalibrating = False
        self.last_rotate_key = time.time()
        self.rotate_key_start_time = -1
        self.rotation_direction = RemoteNavigationPlanner.DriveDirection.BREAK
        self.rotation_target_angles = {
            "BrC": self.BRC_MOTOR_DIRECTION * -1 * math.pi / 2,
            "BrR": math.pi / 4,
            "BrL": -math.pi / 4,
        }
        self.rotation_velocity = 0
        self.rotation_acceleration = 0

    def is_moving_forward(self):
        return self.current_velocity > 0

    def is_moving_backward(self):
        return self.current_velocity < 0

    def ramp_up_acceleration(self):
        if self.last_drive_direction == RemoteNavigationPlanner.DriveDirection.FORWARD:
            self.update_acceleration(self.delta_acceleration_hz, -self.max_acceleration, self.max_acceleration)
        else:
            self.update_acceleration(-self.delta_acceleration_hz, -self.max_acceleration, self.max_acceleration)

    def ramp_down_acceleration(self):
        if self.last_drive_direction == RemoteNavigationPlanner.DriveDirection.FORWARD:
            self.update_acceleration(-self.delta_acceleration_hz, 0, self.max_acceleration)
        else:
            self.update_acceleration(self.delta_acceleration_hz, -self.max_acceleration, 0)

    def ramp_up_deceleration(self):
        if self.is_moving_forward():
            # print("ramp_up_deceleration forward", -self.delta_acceleration_hz, -self.max_acceleration)
            self.update_acceleration(-self.delta_acceleration_hz, -self.max_acceleration, self.max_acceleration)
        else:
            self.update_acceleration(self.delta_acceleration_hz, -self.max_acceleration, self.max_acceleration)

    def ramp_down_deceleration(self):
        if self.is_moving_forward():
            self.update_acceleration(self.delta_acceleration_hz, -self.max_acceleration, 0)
        else:
            self.update_acceleration(-self.delta_acceleration_hz, 0, self.max_acceleration)

    def continue_acceleration(self):
        if self.acceleration_ramp_delta_velocity + self.current_velocity > self.max_velocity:
            # ramp-down acceleration phase.
            self.ramp_down_acceleration()
        elif self.acceleration_ramp_delta_velocity > abs(self.current_velocity):
            # ramp-up acceleration phase.
            self.ramp_up_acceleration()
        self.update_velocity()

    def continue_deceleration(self):
        # Check if in accell ramp-up, max acceleration, or ramp-down phase.
        if self.acceleration_ramp_delta_velocity > abs(self.current_velocity):
            # ramp-down phase.
            self.ramp_down_deceleration()
        if self.acceleration_ramp_delta_velocity * 2 < abs(self.current_velocity):
            # ramp-up acceleration phase.
            self.ramp_up_deceleration()
        self.update_velocity()

    def update_acceleration(self, change_in_acceleration, min_value, max_value):
        self.current_acceleration = max(min_value, min(self.current_acceleration + change_in_acceleration, max_value))

    def update_velocity(self):
        if self.current_velocity == 0:
            self.current_velocity = max(
                -self.max_velocity, min((self.current_acceleration / self.operating_frequency), self.max_velocity)
            )
        elif self.is_moving_forward():
            self.current_velocity = max(
                0,
                min(self.current_velocity + (self.current_acceleration / self.operating_frequency), self.max_velocity),
            )
        else:
            self.current_velocity = max(
                -self.max_velocity,
                min(self.current_velocity + (self.current_acceleration / self.operating_frequency), 0),
            )

    def update_loc_ref(self):
        total_displacement = self.current_velocity / self.operating_frequency
        total_displacement_radians = 2 * math.pi * (total_displacement / self.nav_platform.WHEEL_CIRCUMFERENCE)

        for motor_name in self.nav_platform.SPINNING_MOTORS:
            if motor_name == "BpL" or (self.BRC_MOTOR_DIRECTION == -1 and motor_name == "BpC"):
                self.current_loc_ref[motor_name] -= total_displacement_radians
            else:
                self.current_loc_ref[motor_name] += total_displacement_radians
            self.nav_platform._get_motor_manager().write_param(motor_name, "loc_ref", self.current_loc_ref[motor_name])

    def update_wheel_angle(self):
        for motor_name in self.nav_platform.TURNING_MOTORS:
            self.nav_platform._get_motor_manager().write_param(motor_name, "loc_ref", self.current_wheel_angle)

    def update_rotation_angle(self):
        for motor_name, target in self.rotation_target_angles.items():
            self.nav_platform._get_motor_manager().write_param(motor_name, "loc_ref", target)

    def has_exceed_rotate_key_timeout(self):
        if time.time() - self.rotate_key_start_time > 0.75:
            return time.time() - self.last_rotate_key > 0.3
        else:
            return False

    def update_rotation_process(self):
        if self.has_exceed_rotate_key_timeout() and abs(self.rotation_velocity) < 0.001:
            # Return wheels to original position after stopping
            self.update_wheel_angle()
            if self.is_at_target_wheel_angle():
                self.is_rotating = False
                self.rotate_key_start_time = -1
        elif not self.is_at_target_rotation_angle():
            self.update_rotation_angle()
        else:
            if self.has_exceed_rotate_key_timeout():
                self.continue_rotation_deceleration()
                # Handle rotation movement similar to forward/backward
            elif abs(self.rotation_velocity) <= self.max_rotation_velocity:
                self.continue_rotation_acceleration()
            if abs(self.rotation_velocity) > 0:
                self.update_rotation_loc_ref()

    def step(self):
        if self.is_recalibrating:
            return
        elif self.is_rotating:
            self.update_rotation_process()
        else:
            if (
                time.time() - self.last_drive_key > 0.75
                or self.last_drive_direction == RemoteNavigationPlanner.DriveDirection.BREAK
            ):
                if abs(self.current_velocity) > 0:
                    # if random.random() < 0.01:
                    #     print("decelerating", self.current_velocity, self.current_acceleration)
                    self.continue_deceleration()
            else:
                if abs(self.current_velocity) < self.max_velocity:
                    # start accelerating.
                    # if random.random() < 0.01:
                    #     print("accelerating", self.current_velocity, self.current_acceleration)
                    self.continue_acceleration()

        if not self.is_at_target_position() or not self.is_at_target_wheel_angle() or self.is_rotating:
            if not self.nav_platform.is_motors_enabled():
                mm = self.nav_platform._get_motor_manager()
                for motor in self.nav_platform.motors_map.values():
                    mm.enable(motor.motor_name)
        else:
            # if self.nav_platform.is_motors_enabled():
            # purpose of 0.5s delay is to not disable the motor when there is still some momentum.
            if time.time() - self.last_drive_key > 0.5 and time.time() - self.last_rotate_key > 0.5 and time.time() - self.last_turn_key > 0.5:
                mm = self.nav_platform._get_motor_manager()
                for motor in self.nav_platform.motors_map.values():
                    if motor.mode[0] == MotorMode.Run:
                        # motor that mode is not always updated.
                        mm.disable(motor.motor_name)

        if abs(self.current_velocity) > 0:
            self.update_loc_ref()

        elif not self.is_at_target_wheel_angle() and not self.is_rotating:
            self.update_wheel_angle()

    def invoke_forward(self):
        if self.is_moving_backward():
            self.last_drive_direction = RemoteNavigationPlanner.DriveDirection.BREAK
        else:
            self.last_drive_direction = RemoteNavigationPlanner.DriveDirection.FORWARD
            self.last_drive_key = time.time()

    def invoke_backward(self):
        if self.is_moving_forward():
            self.last_drive_direction = RemoteNavigationPlanner.DriveDirection.BREAK
        else:
            self.last_drive_direction = RemoteNavigationPlanner.DriveDirection.BACKWARD
            self.last_drive_key = time.time()

    def invoke_turn_left(self):
        self.current_wheel_angle += math.pi / 40
        if self.current_wheel_angle > math.pi / 2:
            self.current_wheel_angle = math.pi / 2

    def invoke_turn_right(self):
        self.current_wheel_angle -= math.pi / 40
        if self.current_wheel_angle < -math.pi / 2:
            self.current_wheel_angle = -math.pi / 2

    def invoke_orient_left(self):
        self.current_wheel_angle = math.pi / 2

    def invoke_orient_right(self):
        self.current_wheel_angle = -math.pi / 2

    def invoke_orient_forward(self):
        self.current_wheel_angle = 0

    def invoke_orient_backward(self):
        self.current_wheel_angle = 0

    def invoke_rotate_ccw(self):
        if self.is_at_target_position() or self.is_rotating:
            self.is_rotating = True
            self.rotation_direction = RemoteNavigationPlanner.DriveDirection.FORWARD
            self.last_rotate_key = time.time()
            if self.rotate_key_start_time == -1:
                self.rotate_key_start_time = time.time()
        # only do if velocity = 0.

    def invoke_rotate_cw(self):
        if self.is_at_target_position() or self.is_rotating:
            self.is_rotating = True
            self.rotation_direction = RemoteNavigationPlanner.DriveDirection.BACKWARD
            self.last_rotate_key = time.time()
            if self.rotate_key_start_time == -1:
                self.rotate_key_start_time = time.time()

    def invoke_debug(self):
        print(
            "debug",
            self,
            "vel",
            self.current_velocity,
            "loc_ref",
            self.current_loc_ref,
            "at_target_wheel_angle",
            self.is_at_target_wheel_angle(),
        )

    def is_at_target_position(self):
        return math.isclose(self.current_velocity, 0, abs_tol=0.001)

    def is_at_target_wheel_angle(self):
        for motor_name in self.nav_platform.TURNING_MOTORS:
            motor = self.nav_platform.motors_map[motor_name]
            if not math.isclose(motor.angle[0], self.current_wheel_angle, abs_tol=0.001):
                return False
        return True

    def is_at_target_rotation_angle(self):
        for motor_name in self.nav_platform.TURNING_MOTORS:
            motor = self.nav_platform.motors_map[motor_name]
            target = self.rotation_target_angles[motor_name]
            if not math.isclose(motor.angle[0], target, abs_tol=0.01):
                print("failed target", motor_name, motor.angle[0], target)
                return False
        return True

    def key_pressed(self, key):
        if key in self.key_map:
            self.key_map[key]()

    def continue_rotation_acceleration(self):
        if self.rotation_direction == self.DriveDirection.FORWARD:
            self.rotation_acceleration = min(
                self.rotation_acceleration + self.delta_acceleration_hz, self.max_rotation_acceleration
            )
        else:
            self.rotation_acceleration = max(
                self.rotation_acceleration - self.delta_acceleration_hz, -self.max_rotation_acceleration
            )
        self.update_rotation_velocity()

    def continue_rotation_deceleration(self):
        if self.rotation_velocity > 0:
            self.rotation_acceleration = max(
                self.rotation_acceleration - self.delta_acceleration_hz, -self.max_rotation_acceleration
            )
        else:
            self.rotation_acceleration = min(
                self.rotation_acceleration + self.delta_acceleration_hz, self.max_rotation_acceleration
            )
        self.update_rotation_velocity()

    def update_rotation_velocity(self):
        if self.rotation_velocity == 0:
            self.rotation_velocity = max(
                -self.max_rotation_velocity,
                min((self.rotation_acceleration / self.operating_frequency), self.max_rotation_velocity),
            )
        elif self.rotation_direction == self.DriveDirection.FORWARD:
            self.rotation_velocity = max(
                0,
                min(
                    self.rotation_velocity + (self.rotation_acceleration / self.operating_frequency),
                    self.max_rotation_velocity,
                ),
            )
        else:
            self.rotation_velocity = max(
                -self.max_rotation_velocity,
                min(self.rotation_velocity + (self.rotation_acceleration / self.operating_frequency), 0),
            )

    def update_rotation_loc_ref(self):
        total_displacement = self.rotation_velocity / self.operating_frequency
        total_displacement_radians = 2 * math.pi * (total_displacement / self.nav_platform.WHEEL_CIRCUMFERENCE)

        for motor_name in self.nav_platform.SPINNING_MOTORS:
            self.current_loc_ref[motor_name] += total_displacement_radians
            self.nav_platform._get_motor_manager().write_param(motor_name, "loc_ref", self.current_loc_ref[motor_name])


class NaiveNavigationPlanner(NavigationPlanner):

    @staticmethod
    def generate_s_curve_trajectory(T, dt, jerk, a_max, v_max, v0=0.0, a0=0.0):
        """
        Generate a jerk-limited (S-curve) trajectory.

        Parameters:
            T (float): Total trajectory time (s).
            dt (float): Time step (s).
            jerk (float): Constant jerk (m/s^3).
            a_max (float): Maximum acceleration (m/s^2).
            v_max (float): Maximum velocity (m/s).
            v0 (float): Starting velocity (m/s). Default is 0.
            a0 (float): Starting acceleration (m/s^2). Default is 0.

        Returns:
            t_arr (np.array): Array of time values.
            a_arr (np.array): Acceleration profile.
            v_arr (np.array): Velocity profile.
            x_arr (np.array): Position (displacement) profile.

        Assumes a symmetric S-curve profile where the deceleration phase is the mirror of acceleration.
        """
        # Time to ramp from a0 to a_max
        t_ramp = (a_max - a0) / jerk  # typically, a0 is 0

        # Velocity gained during one ramp (integrating acceleration from 0 to a_max)
        # For a ramp starting at 0: Δv_ramp = 0.5 * a_max * t_ramp.
        delta_v_ramp = 0.5 * a_max * t_ramp

        # Determine constant acceleration duration needed to reach v_max:
        # Total increase during acceleration phase = ramp-up + constant acceleration + ramp-down
        # = delta_v_ramp + (a_max * T_const_acc) + delta_v_ramp = a_max*T_const_acc + 2*delta_v_ramp.
        T_const_acc = (v_max - 2 * delta_v_ramp) / a_max

        # Total time for the full acceleration phase (acceleration ramp-up, constant acceleration, ramp-down)
        t_acc_phase = t_ramp + T_const_acc + t_ramp  # = T_const_acc + 2*t_ramp

        # For symmetric deceleration, deceleration phase takes the same time.
        # The remaining time is the cruise period at constant v_max.
        cruise_time = T - 2 * t_acc_phase
        if cruise_time < 0:
            raise ValueError("Total time T is too short for the given constraints.")

        # Define key time nodes:
        t1 = t_ramp  # End of acceleration ramp-up
        t2 = t1 + T_const_acc  # End of constant acceleration segment
        t3 = t2 + t_ramp  # End of acceleration ramp-down (v_max reached)
        t4 = t3 + cruise_time  # End of cruise at v_max
        t5 = t4 + t_ramp  # End of deceleration ramp-down start (acceleration = -a_max)
        t6 = t5 + T_const_acc  # End of constant deceleration segment
        t7 = t6 + t_ramp  # End of deceleration ramp-up back to 0

        # Create the time array.
        t_arr = np.arange(0, T + dt, dt)
        a_arr = np.zeros_like(t_arr)

        # Define the piecewise acceleration profile:
        # Segment 1: [0, t1]: ramp-up (a = a0 + jerk*t)
        seg1 = (t_arr >= 0) & (t_arr < t1)
        a_arr[seg1] = a0 + jerk * (t_arr[seg1])

        # Segment 2: [t1, t2]: constant acceleration (a = a_max)
        seg2 = (t_arr >= t1) & (t_arr < t2)
        a_arr[seg2] = a_max

        # Segment 3: [t2, t3]: ramp-down (a = a_max - jerk*(t - t2))
        seg3 = (t_arr >= t2) & (t_arr < t3)
        a_arr[seg3] = a_max - jerk * (t_arr[seg3] - t2)

        # Segment 4: [t3, t4]: cruise at constant velocity (a = 0)
        seg4 = (t_arr >= t3) & (t_arr < t4)
        a_arr[seg4] = 0.0

        # Segment 5: [t4, t5]: deceleration ramp (a = 0 - jerk*(t - t4))
        seg5 = (t_arr >= t4) & (t_arr < t5)
        a_arr[seg5] = -jerk * (t_arr[seg5] - t4)

        # Segment 6: [t5, t6]: constant deceleration (a = -a_max)
        seg6 = (t_arr >= t5) & (t_arr < t6)
        a_arr[seg6] = -a_max

        # Segment 7: [t6, t7]: ramp-up from deceleration (a = -a_max + jerk*(t - t6))
        seg7 = (t_arr >= t6) & (t_arr <= t7)
        a_arr[seg7] = -a_max + jerk * (t_arr[seg7] - t6)

        # Integrate acceleration to get velocity and position.
        # Using cumulative sum for a simple Euler integration.
        v_arr = np.cumsum(a_arr) * dt + v0
        x_arr = np.cumsum(v_arr) * dt

        return t_arr, a_arr, v_arr, x_arr

    @staticmethod
    def generate_s_curve_trajectory_by_displacement_math(S, dt, jerk, a_max, v_max, v0=0.0, a0=0.0):
        """
        Generate a jerk-limited (S-curve) trajectory for a given displacement S,
        handling three regimes:
        • Regime 1 (Long distance): trajectory reaches v_max.
        • Regime 2 (Intermediate): trajectory reaches a_max but not v_max.
        • Regime 3 (Short distance): trajectory is fully jerk-limited (a_max not reached).

        Parameters:
        S      : desired total displacement (m)
        dt     : time step (s)
        jerk   : constant jerk (m/s^3)
        a_max  : maximum acceleration (m/s^2)
        v_max  : maximum velocity (m/s)
        v0, a0 : initial velocity and acceleration (assumed 0)

        Returns:
        t_arr, a_arr, v_arr, x_arr : arrays of time, acceleration, velocity, and displacement.
        """
        # Threshold displacement for reaching a_max:
        S_thr = 2 * a_max**3 / jerk**2
        # Displacement required for a full profile (reaching v_max) in the acceleration phase:
        S_full = (v_max**2) / a_max + (v_max * a_max) / jerk  # note: this is the displacement in both accel+decel

        if S >= S_full:
            # Regime 1: v_max is reached.
            T_total = 2 * (v_max / a_max + a_max / jerk) + (S - S_full) / v_max
            return NaiveNavigationPlanner.generate_s_curve_trajectory(T_total, dt, jerk, a_max, v_max, v0, a0)
        elif S >= S_thr:
            # Regime 2: a_max is reached, but v_max is not.
            # In a profile that attains a_max (with no cruise), the displacement in the acceleration phase is:
            #    S_acc = a_max^3/jerk^2 + (a_max^2/jerk)*T_const + 0.5*a_max*T_const^2.
            # Setting 2*S_acc = S and solving for T_const yields:
            T_const = math.sqrt((S - a_max**3 / jerk**2) / a_max) - a_max / jerk
            # Total time:
            T_total = 4 * a_max / jerk + 2 * T_const
            # Define key time nodes:
            t1 = a_max / jerk
            t2 = t1 + T_const
            t3 = t2 + a_max / jerk  # end of acceleration phase
            t4 = t3 + a_max / jerk  # deceleration phase, first ramp
            t5 = t4 + T_const
            t6 = t5 + a_max / jerk  # end of deceleration phase

            t_arr = np.arange(0, T_total + dt, dt)
            a_arr = np.zeros_like(t_arr)
            # Acceleration phase:
            a_arr[(t_arr >= 0) & (t_arr < t1)] = jerk * t_arr[(t_arr >= 0) & (t_arr < t1)]
            a_arr[(t_arr >= t1) & (t_arr < t2)] = a_max
            a_arr[(t_arr >= t2) & (t_arr < t3)] = a_max - jerk * (t_arr[(t_arr >= t2) & (t_arr < t3)] - t2)
            # Deceleration phase (mirror the acceleration phase):
            a_arr[(t_arr >= t3) & (t_arr < t4)] = -jerk * (t_arr[(t_arr >= t3) & (t_arr < t4)] - t3)
            a_arr[(t_arr >= t4) & (t_arr < t5)] = -a_max
            a_arr[(t_arr >= t5) & (t_arr <= t6)] = -a_max + jerk * (t_arr[(t_arr >= t5) & (t_arr <= t6)] - t5)

            v_arr = np.cumsum(a_arr) * dt + v0
            x_arr = np.cumsum(v_arr) * dt
            return t_arr, a_arr, v_arr, x_arr
        else:
            # Regime 3: The distance is too short to reach a_max.
            # In a fully jerk-limit3ed (no saturation) profile the acceleration phase is composed of two segments,
            # and by symmetry the total time is T_total = 4*t_j, where:
            t_j = (S / (2 * jerk)) ** (1 / 3)
            T_total = 4 * t_j
            t1 = t_j
            t2 = 2 * t_j
            t3 = 3 * t_j
            t4 = 4 * t_j

            t_arr = np.arange(0, T_total + dt, dt)
            a_arr = np.zeros_like(t_arr)
            a_arr[(t_arr >= 0) & (t_arr < t1)] = jerk * t_arr[(t_arr >= 0) & (t_arr < t1)]
            a_arr[(t_arr >= t1) & (t_arr < t2)] = jerk * (2 * t_j - t_arr[(t_arr >= t1) & (t_arr < t2)])
            a_arr[(t_arr >= t2) & (t_arr < t3)] = -jerk * (t_arr[(t_arr >= t2) & (t_arr < t3)] - 2 * t_j)
            a_arr[(t_arr >= t3) & (t_arr <= t4)] = -jerk * (4 * t_j - t_arr[(t_arr >= t3) & (t_arr <= t4)])

            v_arr = np.cumsum(a_arr) * dt + v0
            x_arr = np.cumsum(v_arr) * dt
            return t_arr, a_arr, v_arr, x_arr

    def __init__(
        self, operating_frequency, max_velocity, max_acceleration, max_jerk, dtheta, dtheta_accel, dtheta_jerk
    ):
        super().__init__()
        self.operating_frequency = operating_frequency
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.current_wheel_angle = 0
        self.max_jerk = max_jerk

        # Currently not supported.
        self.dtheta = dtheta
        self.dtheta_accel = dtheta_accel
        self.dtheta_jerk = dtheta_jerk

        self.curr_index = 0

    def update_trajectory_planner(self):

        target_wheel_angle = math.atan2(self.target_y, self.target_x)
        # calculate the distance to the target position
        distance = math.sqrt(self.target_x**2 + self.target_y**2)
        # calculate the time to reach the target position
        time = distance / self.target_velocity

        t_arr, a_arr, v_arr, x_arr = NaiveNavigationPlanner.generate_s_curve_trajectory_by_displacement_math(
            self.dtheta, self.operating_frequency, self.max_jerk, self.max_acceleration, self.max_velocity
        )


class VelocityNavigationPlanner(NavigationPlanner):
    """Allows the robot to be controlled by a specified velocity."""

    BRC_MOTOR_DIRECTION = -1
    WHEEL_CIRCUMFERENCE_MM = 376.991

    def __init__(
        self, nav_platform, max_velocity, max_acceleration, max_jerk, max_rotation_velocity, max_rotation_acceleration
    ):
        super().__init__()
        self.current_wheel_angle = 0
        self.nav_platform = nav_platform
        self.operating_frequency = nav_platform.operating_frequency
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        # rad/s and rad/s2
        self.max_rotation_velocity = max_rotation_velocity
        self.max_rotation_acceleration = max_rotation_acceleration
        self.acceleration_ramp_time = self.max_acceleration / max_jerk
        self.acceleration_ramp_delta_velocity = change_in_vel(0, max_jerk, 0, self.acceleration_ramp_time)
        self.max_jerk = max_jerk
        self.delta_acceleration_hz = self.max_jerk / self.operating_frequency
        self.current_velocity = 0
        self.current_angle = {"BrC": 0, "BrR": 0, "BrL": 0}
        self.current_spd_ref = {"BpC": 0, "BpR": 0, "BpL": 0}
        self.current_acceleration = 0
        self.last_drive_direction = (
            RemoteNavigationPlanner.DriveDirection.BREAK
        )  # 1 for forward, -1 for backward, 0 for break.
        self.last_drive_key = time.time()
        self.last_turn_key = time.time()
        self.is_rotating = False
        self.last_rotate_key = time.time()
        self.rotate_key_start_time = -1
        self.rotation_direction = RemoteNavigationPlanner.DriveDirection.BREAK
        self.rotation_target_angles = {
            "BrC": self.BRC_MOTOR_DIRECTION * -1 * math.pi / 2,
            "BrR": math.pi / 4,
            "BrL": -math.pi / 4,
        }
        self.rotation_velocity = 0
        self.rotation_acceleration = 0

    def _get_motor_manager(self):
        return self.nav_platform._get_motor_manager()

    def reset(self):
        mm = self._get_motor_manager()
        try:
            self.nav_platform.disable_motors()
            for motor_name in self.nav_platform.TURNING_MOTORS:
                mm.write_param(motor_name, "run_mode", RunMode.Position.value)
            for motor_name in self.nav_platform.SPINNING_MOTORS:
                mm.write_param(motor_name, "run_mode", RunMode.Speed.value)
                print(f"reset {motor_name}")
        except UnknownInterfaceError as e:
            print(f"Could not find interface for motors: {e}, navigation platform will be disabled")
            self.nav_platform._enabled = False

    def step(self):
        pass

    def ensure_motors_enabled(self, motors):
        mm = self._get_motor_manager()
        for motor_name in motors:
            if mm.motors[motor_name].mode[0] != MotorMode.Run:
                mm.enable(motor_name)

    def orient_rotate(self):
        mm = self._get_motor_manager()
        self.ensure_motors_enabled(self.nav_platform.TURNING_MOTORS)
        # Move the wheels into a position so that's ready to rotate in place.
        for motor_name, angle in self.rotation_target_angles.items():
            mm.write_param(motor_name, "loc_ref", mm.motors[motor_name].middle_pos + angle)
            self.current_angle[motor_name] = angle

    def rotate_in_place(self, speed):
        # speed is in degrees/s. You can compute angles.
        mm = self._get_motor_manager()
        for motor_name, angle in self.rotation_target_angles.items():
            if self.current_angle[motor_name] != angle:
                self.orient_rotate()
                break
        self.ensure_motors_enabled(self.nav_platform.SPINNING_MOTORS)
        target = self.degrees_to_radians(speed)
        print("target", target)
        for motor_name in self.nav_platform.SPINNING_MOTORS:
            mm.write_param(motor_name, "spd_ref", target)
            self.current_velocity = speed

    def _orient_angle(self, degrees):
        mm = self._get_motor_manager()
        target_angle = self.degrees_to_radians(-1 * degrees) # debug root cause of why it's -1?
        for motor_name in self.nav_platform.TURNING_MOTORS:
            motor = mm.motors[motor_name]
            mm.write_param(motor_name, "loc_ref", motor.middle_pos + target_angle)
            self.current_angle[motor_name] = target_angle

    def _set_speed(self, speed):
        degrees = speed / self.WHEEL_CIRCUMFERENCE_MM * 360
        target = self.degrees_to_radians(degrees)
        self.current_velocity = speed
        mm = self._get_motor_manager()
        for motor_name in self.nav_platform.SPINNING_MOTORS:
            if motor_name == "BpR":
                mm.write_param(motor_name, "spd_ref", target)
            else:
                mm.write_param(motor_name, "spd_ref", -1 * target)

    def go_to(self, degrees, speed, motors_is_on=False):
        if not motors_is_on:
            self.ensure_motors_enabled(self.nav_platform.TURNING_MOTORS)
            self.ensure_motors_enabled(self.nav_platform.SPINNING_MOTORS)
        self._orient_angle(degrees)
        self._set_speed(speed)

    def orient_angle(self, degrees):
        self.ensure_motors_enabled(self.nav_platform.TURNING_MOTORS)
        self._orient_angle(degrees)

        # angle should be in degrees from -90 to 90 degrees. 0 represents the center. All the wheels will be turned to this angle.
        # clockwise convention. clockwise is positive.

    def set_speed(self, speed):
        # speed should be in mm / s # degrees/s
        self.ensure_motors_enabled(self.nav_platform.SPINNING_MOTORS)
        self._set_speed(speed)

    def degrees_to_radians(self, degrees: float) -> float:
        """
        Convert an angle from degrees to radians.

        Args:
            degrees (float): Angle in degrees.

        Returns:
            float: Angle in radians.
        """
        return degrees * (math.pi / 180)

    def is_at_target_position(self):
        return True


class ThreeWheelServeDrivePlatform(SteppableSystem):

    TURNING_MOTORS = ["BrC", "BrR", "BrL"]
    SPINNING_MOTORS = ["BpC", "BpR", "BpL"]

    WHEEL_DIAMETER = 0.12
    WHEEL_RADIUS = WHEEL_DIAMETER / 2
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi

    def __init__(self, motors_manager: MotorsManager):
        self.motors_map = {
            "BrC": Motor(0x70, "BrC"),
            "BrR": Motor(0x71, "BrR"),
            "BrL": Motor(0x72, "BrL"),
            "BpC": Motor(0x73, "BpC"),
            "BpR": Motor(0x74, "BpR"),
            "BpL": Motor(0x75, "BpL"),
        }
        self.motors_manager = motors_manager
        self.motors_manager.add_motors(self.motors_map, family_name="wheels")
        self.motors_manager.find_motors(list(self.motors_map.keys()))

        self.operating_frequency = 100
        self.nav_planner = VelocityNavigationPlanner(
            nav_platform=self,
            max_velocity=0.2,
            max_acceleration=0.1,
            max_jerk=1.0,
            max_rotation_velocity=0.075,
            max_rotation_acceleration=0.15,
        )

        self.reset()

    def reset(self):
        # Reset to a safe state
        try:
            for motor_name in self.SPINNING_MOTORS:
                self.motors_manager.disable(motor_name)
                self.motors_manager.write_param(motor_name, "run_mode", 1)
                self.motors_manager.write_param(motor_name, "limit_spd", 4 * math.pi) # for safety right now.
                self.motors_manager.zero_position(motor_name)
            for motor_name in self.TURNING_MOTORS:
                self.motors_manager.disable(motor_name)
                self.motors_manager.write_param(motor_name, "run_mode", 1)
                self.motors_manager.write_param(motor_name, "limit_spd", math.pi / 2) # for safety right now.
                # self.motors_manager.zero_position(motor_name)
        except UnknownInterfaceError as e:
            print(f"Could not find interface for motors: {e}, navigation platform will be disabled")
            self._enabled = False
        self._enabled = True
        self.nav_planner.reset()
    
    def _get_motor_manager(self):
        if not self._enabled:
            raise ValueError("Navigation platform is not enabled")
        return self.motors_manager

    def on_abort(self):
        if not self._enabled:
            return
        mm = self._get_motor_manager()
        for motor_name in self.SPINNING_MOTORS:
            mm.disable(motor_name)
        for motor_name in self.TURNING_MOTORS:
            mm.disable(motor_name)

    def is_at_target_position(self):
        return (
            math.isclose(self.x, self.target_x, abs_tol=0.001)
            and math.isclose(self.y, self.target_y, abs_tol=0.001)
            and math.isclose(self.theta, self.target_theta, abs_tol=0.001)
        )

    def is_motors_enabled(self):
        for motor in self.motors_map.values():
            if not motor.mode[0] == MotorMode.Run:
                return False
        return True

    def _step(self):
        # self.nav_planner.step()
        # Move to target position
        pass
        # TODO: If the motor is at the right angle:

    def reset_global_origin(self):
        self.x = 0
        self.y = 0
        self.theta = 0

    def update_trajectory_plan(self):
        # x is forward, y is left, wheel_angle starts at 0 and is CCW
        # calculate the wheel angle to reach the target position
        target_wheel_angle = math.atan2(self.target_y, self.target_x)
        # calculate the distance to the target position
        distance = math.sqrt(self.target_x**2 + self.target_y**2)
        # calculate the time to reach the target position
        time = distance / self.target_velocity

    def set_target_position(self, x=None, y=None, theta=None):
        if x is not None:
            self.target_x = x
        if y is not None:
            self.target_y = y
        if x is not None or y is not None:
            self.update_trajectory_plan()
        if theta is not None:
            self.target_theta = theta

    def set_target_velocity(self, velocity=None, dtheta=None):
        if velocity is not None:
            self.target_velocity = velocity
        if dtheta is not None:
            self.target_dtheta = dtheta

    def set_target_acceleration(self, acceleration=None, dtheta_accel=None):
        if acceleration is not None:
            self.target_accel = acceleration
        if dtheta_accel is not None:
            self.target_dtheta_accel = dtheta_accel

    def set_target_jerk(self, jerk=None, dtheta_jerk=None):
        if jerk is not None:
            self.target_jerk = jerk
        if dtheta_jerk is not None:
            self.target_dtheta_jerk = dtheta_jerk

    def set_target_state(
        self,
        x=None,
        y=None,
        theta=None,
        velocity=None,
        dtheta=None,
        acceleration=None,
        dtheta_accel=None,
        jerk=None,
        dtheta_jerk=None,
    ):
        self.set_target_position(x, y, theta)
        self.set_target_velocity(velocity, dtheta)
        self.set_target_acceleration(acceleration, dtheta_accel)
        self.set_target_jerk(jerk, dtheta_jerk)

    def is_valid_range(self, total_range, expected_range=math.pi, tolerance=0.005):
        return total_range >= expected_range * (1.0 - tolerance) and total_range <= expected_range * (1 + tolerance)

    def center_motor(self, motor_name, verbose=False):
        mm = self._get_motor_manager()
        FULL_ROTATION = 2 * math.pi
        left_pos, right_pos, middle_pos, total_range = mm.get_range(
            motor_name, expected_range=(220 * math.pi) / 180, verbose=verbose
        )
        while not self.is_valid_range(total_range, expected_range=(220 * math.pi) / 180):
            print("Warning: Range (", total_range, ") is not close to 220 degrees, recalibrating")
            mm.disable(motor_name)
            mm.zero_position(motor_name)
            time.sleep(0.1)
            mm.zero_position(motor_name)
            print("failed", left_pos, right_pos, middle_pos, total_range)
            left_pos, right_pos, middle_pos, total_range = mm.get_range(
                motor_name, expected_range=(220 * math.pi) / 180, verbose=verbose
            )
            time.sleep(0.1)

        mm.disable(motor_name)
        mm.zero_position(motor_name)
        time.sleep(0.1)
        mm.zero_position(motor_name)
        time.sleep(0.1)

        if verbose:
            print(
                "Positions: left_pos",
                left_pos,
                "right_pos",
                right_pos,
                "middle_pos",
                middle_pos,
                "total_range",
                total_range,
            )

        print(left_pos, right_pos, middle_pos, total_range)
        left_pos, right_pos, middle_pos, total_range = mm.get_range(
            motor_name,
            # start_pos=1.4,
            step_size=0.001,
            step_time=0.01,
            expected_range=(220 * math.pi) / 180,
            verbose=verbose,
        )
        print("after checking", left_pos, right_pos, middle_pos, total_range)
        return left_pos, right_pos, middle_pos, total_range

    def disable_motors(self):
        mm = self._get_motor_manager()
        for motor_name in self.SPINNING_MOTORS:
            mm.disable(motor_name)
        for motor_name in self.TURNING_MOTORS:
            mm.disable(motor_name)

    def recalibrate(self, verbose=False):
        #self.nav_planner.is_recalibrating = True
        mm = self._get_motor_manager()
        for motor_name in self.TURNING_MOTORS:
            motor = mm.motors[motor_name]
            total_range = 0
            middle_pos = 0
            while not self.is_valid_range(total_range, expected_range=(220 * math.pi) / 180) and abs(middle_pos) < 0.15:
                left_pos, right_pos, middle_pos, total_range = self.center_motor(motor_name, verbose)
            motor.left_pos, motor.right_pos, motor.middle_pos, motor.total_range = (
                left_pos,
                right_pos,
                middle_pos,
                total_range,
            )
            time.sleep(0.1)

        # self.nav_planner.is_recalibrating = False
