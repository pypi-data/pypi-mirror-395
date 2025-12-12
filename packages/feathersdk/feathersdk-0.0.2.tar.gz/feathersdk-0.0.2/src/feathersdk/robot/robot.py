import time
from .motors.motors_manager import MotorsManager
from .steppable_system import SteppableSystem
from .navigation_platform import ThreeWheelServeDrivePlatform
from .manipulation_platform import BimanualManipulationPlatform
from .neck_platform import MyActuatorNeckPlatform
from .torso_platform import EZMotionTorsoPlatform
from .test_system import TestSystem
from ..comms import CommsManager
from ..comms.system import get_all_physical_can_interfaces
import threading
import atexit, signal, sys

class Robot(SteppableSystem):
    def __init__(self, robot_name: str):
        self.robot_name = robot_name
        # 10000 Hz
        self.operating_frequency = 10000
        self.systems = {}
        self.should_continue = True
        atexit.register(self.on_abort)
        signal.signal(signal.SIGTERM, self._handle_exit)
        signal.signal(signal.SIGINT, self._handle_exit)

    def start(self):
        super().start(is_root_step=True)
        for system in self.systems.values():
            if system:
                system.start()

    def _after_step(self):
        current_time = time.time()
        for system in self.systems.values():
            if system and system.get_next_step_start_time() <= current_time:
                system.step()
        
        super()._after_step()

    def _handle_exit(self, signum, frame):
        self.on_abort()
        sys.exit(0)

    def on_abort(self):
        self.should_continue = False

        for system in self.systems.values():
            if system:
                system.on_abort()

    def robot_loop(self):
        self.start()
        while self.should_continue:
            self.step()

        time.sleep(0.1)

    def start_loop_in_background(self):
        robot_thread = threading.Thread(target=self.robot_loop)

        robot_thread.daemon = True
        robot_thread.start()

class FeatherRobot(Robot):
    def __init__(self, robot_name: str, config: dict = {}):
        super().__init__(robot_name)
        
        self.comms = CommsManager()
        self.comms.start(get_all_physical_can_interfaces(), allow_no_enable_can=True)

        self.motors_manager = MotorsManager()
        self.navigation_platform = ThreeWheelServeDrivePlatform(self.motors_manager)

        # Find the base motor can interface to use for EZMotion motors. Assume same for all base motors
        base_can_iface = self.motors_manager.motors["BrC"].can_interface

        # self.manipulation_platform = BimanualManipulationPlatform(self.motors_manager)
        self.manipulation_platform = None
        self.neck = MyActuatorNeckPlatform(self.motors_manager, base_can_iface)
        self.battery_system = None
        self.torso = EZMotionTorsoPlatform(self.motors_manager, base_can_iface)
        self.vision_system = None
        self.audio_system = None
        self.listening_system = None
        self.visual_system = None

        if config.get("testing", False):
            self.test_system = TestSystem(self.motors_manager)

        self.systems = {
            "navigation_platform": self.navigation_platform,
            "manipulation_platform": self.manipulation_platform,
            "battery_system": self.battery_system,
            "torso": self.torso,
            "vision_system": self.vision_system,
            "audio_system": self.audio_system,
            "listening_system": self.listening_system,
            "visual_system": self.visual_system,
            "neck": self.neck,
        }

    def get_battery_voltage(self):
        return 0

    def _step(self):
        pass

    def on_abort(self):
        super().on_abort()


