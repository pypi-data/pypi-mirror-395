import os
from typing import TYPE_CHECKING, cast

from antioch.module.token import TokenType
from antioch.session.error import SessionArkError, SessionAssetError
from antioch.session.objects.articulation import Articulation
from antioch.session.objects.camera import Camera
from antioch.session.objects.imu import Imu
from antioch.session.objects.pir_sensor import PirSensor
from antioch.session.objects.radar import Radar
from antioch.session.record import NodeOutputRecorder
from antioch.session.session import SessionContainer
from common.ark import Ark as ArkDefinition, ArkReference, Environment, HardwareAccessMode
from common.ark.hardware import ActuatorGroupHardware, HardwareType
from common.ark.scheduler import NodeCompleteEvent, NodeStartEvent, OnlineScheduler
from common.ark.sim import SimNodeComplete, SimNodeStart
from common.core import (
    Agent,
    ArkStateResponse,
    ContainerSource,
    get_ark_version_reference,
    list_local_arks,
    list_remote_arks,
    load_local_ark,
    pull_remote_ark,
)
from common.message import JointStates, JointTargets, Pose
from common.utils.comms import CommsAsyncSubscriber, CommsPublisher
from common.utils.time import now_us, us_to_s
from common.utils.usd import sanitize_usd_path

if TYPE_CHECKING:
    from antioch.session.scene import Scene

NODE_START_PUBLISHER_PATH = "_ark/node_start/{module}/{node}"
NODE_COMPLETE_SUBSCRIBER_PATH = "_ark/node_complete/{module}/{node}"


class Ark(SessionContainer):
    """
    Complete runtime for an Ark in simulation.

    Manages entire Ark lifecycle from loading through execution. The runtime is designed to be
    robust and deterministic:
    - Events/time increase monotonically via the deterministic scheduler
    - Each execution is processed exactly once via execution tracking
    - Multiple nodes can execute at the same LET

    Example:
        scene = Scene()

        # Build and start Ark
        ark = scene.add_ark(
            name="my_robot",
            version="1.0.0",
            debug=True
        )

        # Step simulation
        scene.step(dt=0.01)  # Delegates to ark.step()
    """

    def __init__(
        self,
        path: str,
        scene: "Scene",
        name: str,
        version: str,
        world_pose: Pose | None = None,
        local_pose: Pose | None = None,
        source: ContainerSource = ContainerSource.LOCAL,
        debug: bool = False,
        timeout: float = 30.0,
    ):
        """
        Initialize and build complete Ark runtime.

        :param path: USD path where the Ark will be built.
        :param scene: Scene instance this Ark belongs to.
        :param name: Name of the Ark.
        :param version: Version of the Ark.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :param source: Container image source.
        :param debug: Enable debug mode.
        :param timeout: Timeout in seconds for the Ark to start.
        """

        super().__init__()
        self._path = path
        self._scene = scene
        self._agent = Agent()

        # Load Ark definition
        self._ark_def = load_local_ark(name, version)
        self._ark_ref = get_ark_version_reference(name, version)
        self._base_path = f"{path}/{sanitize_usd_path(self._ark_def.name)}"

        # Start Ark via agent
        self._agent.start_ark(
            ark=self._ark_def,
            source=source,
            environment=Environment.SIM,
            debug=debug,
            timeout=timeout,
        )

        # Initialize scheduler
        self._scheduler = OnlineScheduler(self._ark_def.edges, self._ark_def.modules)
        self._next_event = self._scheduler.next()
        self._node_start_times_us: dict[tuple[str, str], int] = {}

        # Create publishers and subscribers for node coordination
        self._node_start_publishers: dict[tuple[str, str], CommsPublisher] = {}
        self._node_complete_subscribers: dict[tuple[str, str], CommsAsyncSubscriber] = {}
        for module in self._ark_def.modules:
            for node_name in module.nodes:
                start_path = NODE_START_PUBLISHER_PATH.format(module=module.name, node=node_name)
                complete_path = NODE_COMPLETE_SUBSCRIBER_PATH.format(module=module.name, node=node_name)
                self._node_start_publishers[(module.name, node_name)] = self._session.comms.declare_publisher(start_path)
                self._node_complete_subscribers[(module.name, node_name)] = self._session.comms.declare_async_subscriber(complete_path)

        # Build in scene
        self._load_ark_asset(world_pose=world_pose, local_pose=local_pose)
        self._build_hardware()

    @property
    def path(self) -> str:
        """
        Get the USD path where this Ark is built.

        :return: The USD path of this Ark.
        """

        return self._path

    @property
    def definition(self) -> ArkDefinition:
        """
        Get the Ark definition.

        :return: The Ark definition.
        """

        return self._ark_def

    @property
    def name(self) -> str:
        """
        Get the Ark name.

        :return: The Ark name.
        """

        return self._ark_def.name

    @property
    def state(self) -> ArkStateResponse:
        """
        Get current state of all modules.

        :return: Ark state with module information.
        """

        return self._agent.get_ark_state()

    @staticmethod
    def list_local() -> list[ArkReference]:
        """
        List all locally available Arks.

        :return: List of ArkReference objects from local storage.
        """

        return list_local_arks()

    @staticmethod
    def list_remote() -> list[ArkReference]:
        """
        List all Arks from remote registry.

        Requires authentication. Call session.login() first if not authenticated.

        :return: List of ArkReference objects from remote registry.
        :raises SessionAuthError: If not authenticated.
        """

        return list_remote_arks()

    @staticmethod
    def pull(name: str, version: str, overwrite: bool = False) -> ArkDefinition:
        """
        Pull an Ark from remote registry to local storage.

        Requires authentication. Call session.login() first if not authenticated.
        If the Ark already exists locally, returns the existing Ark unless overwrite=True.

        :param name: Name of the Ark.
        :param version: Version of the Ark.
        :param overwrite: Overwrite local Ark if it already exists.
        :return: The loaded Ark definition.
        :raises SessionAuthError: If not authenticated.
        """

        return pull_remote_ark(name=name, version=version, overwrite=overwrite)

    def step(self, dt_us: int = 1_000_000) -> None:
        """
        Step the Ark simulation forward by exactly dt_us microseconds.

        :param dt_us: Amount of time to step in microseconds (default 1 second).
        """

        current_sim_time_us = self._scene.time_us
        target_sim_time_us = current_sim_time_us + dt_us
        while current_sim_time_us < target_sim_time_us:
            event = self._next_event

            # Step physics directly to target time and break
            if event.let_us > target_sim_time_us:
                self._scene._step_physics(target_sim_time_us - current_sim_time_us)
                break

            # Step physics to event time if needed
            if event.let_us > current_sim_time_us:
                self._scene._step_physics(event.let_us - current_sim_time_us)
                current_sim_time_us = self._scene.time_us

            # Node start: read hardware for node and send non-blocking start to nodes
            if isinstance(event, NodeStartEvent):
                hardware_reads = self._read_node_hardware(event.module, event.node)
                self._node_start_times_us[(event.module, event.node)] = now_us()
                self._node_start_publishers[(event.module, event.node)].publish(
                    SimNodeStart(
                        module_name=event.module,
                        node_name=event.node,
                        start_let_us=event.start_let_us,
                        start_timestamp_us=self._node_start_times_us[(event.module, event.node)],
                        input_tokens=event.input_tokens,
                        hardware_reads=hardware_reads,
                    )
                )

            # Node complete: wait for completion message or budget to elapse and write hardware for node
            elif isinstance(event, NodeCompleteEvent):
                node_config = next(m for m in self._ark_def.modules if m.name == event.module).nodes[event.node]
                node_complete_subscriber = self._node_complete_subscribers[(event.module, event.node)]
                target_time_us = self._node_start_times_us[(event.module, event.node)] + node_config.budget_us
                while True:
                    remaining_time_s = us_to_s(max(0, target_time_us - now_us()))
                    complete = node_complete_subscriber.recv_timeout(SimNodeComplete, timeout=remaining_time_s)
                    if complete is None and now_us() > target_time_us:
                        break
                    if complete is not None and complete.completion_let_us == event.completion_let_us:
                        if complete.hardware_writes is not None:
                            self._write_node_hardware(event.module, event.node, complete.hardware_writes)
                        break

            # Fetch next event
            self._next_event = self._scheduler.next()

    def get_articulation(self) -> Articulation:
        """
        Get the articulation for the Ark.

        :return: The articulation instance.
        """

        return self._articulation

    def get_camera(self, module_name: str, hardware_name: str) -> Camera:
        """
        Get camera hardware view.

        :param module_name: Module name.
        :param hardware_name: Hardware name.
        :return: Camera view.
        """

        if (module_name, hardware_name) not in self._cameras:
            raise SessionArkError(f"Camera '{hardware_name}' not found in module '{module_name}'")
        return self._cameras[(module_name, hardware_name)]

    def get_imu(self, module_name: str, hardware_name: str) -> Imu:
        """
        Get IMU hardware view.

        :param module_name: Module name.
        :param hardware_name: Hardware name.
        :return: IMU view.
        """

        if (module_name, hardware_name) not in self._imus:
            raise SessionArkError(f"IMU '{hardware_name}' not found in module '{module_name}'")
        return self._imus[(module_name, hardware_name)]

    def get_radar(self, module_name: str, hardware_name: str) -> Radar:
        """
        Get radar hardware view.

        :param module_name: Module name.
        :param hardware_name: Hardware name.
        :return: Radar view.
        """

        if (module_name, hardware_name) not in self._radars:
            raise SessionArkError(f"Radar '{hardware_name}' not found in module '{module_name}'")
        return self._radars[(module_name, hardware_name)]

    def get_pir(self, module_name: str, hardware_name: str) -> PirSensor:
        """
        Get PIR sensor hardware view.

        :param module_name: Module name.
        :param hardware_name: Hardware name.
        :return: PIR sensor view.
        """

        if (module_name, hardware_name) not in self._pirs:
            raise SessionArkError(f"PIR sensor '{hardware_name}' not found in module '{module_name}'")
        return self._pirs[(module_name, hardware_name)]

    def list_hardware(self) -> dict[str, list[tuple[str, str]]]:
        """
        List all hardware in the Ark.

        :return: Dictionary of hardware (module name, hardware name) keyed by hardware type.
        """

        return {
            "CAMERA": list(self._cameras.keys()),
            "IMU": list(self._imus.keys()),
            "PIR": list(self._pirs.keys()),
            "RADAR": list(self._radars.keys()),
        }

    def record_node_output(
        self,
        module_name: str,
        node_name: str,
        output_name: str,
        token_type: TokenType | None = TokenType.DATA,
        last_n: int = 10,
    ) -> NodeOutputRecorder:
        """
        Create a recorder for monitoring node output tokens.

        :param module_name: Module name.
        :param node_name: Node name within module.
        :param output_name: Output name within node.
        :param token_type: Token type to record (default: TokenType.DATA, None = all types).
        :param last_n: Number of recent tokens to buffer.
        :return: NodeOutputRecorder instance.
        """

        return NodeOutputRecorder(
            comms=self._session.comms,
            ark_def=self._ark_def,
            module_name=module_name,
            node_name=node_name,
            output_name=output_name,
            token_type=token_type,
            last_n=last_n,
        )

    def _read_node_hardware(self, module_name: str, node_name: str) -> dict[str, bytes]:
        """
        Read hardware state for node execution.

        :param module_name: Module name.
        :param node_name: Node name.
        :return: Hardware reads keyed by hardware name.
        """

        hardware_reads = {}
        node_def = next(m for m in self._ark_def.modules if m.name == module_name).nodes[node_name]
        for hardware_name, access_mode in node_def.hardware_access.items():
            if access_mode not in (HardwareAccessMode.READ, HardwareAccessMode.READ_WRITE):
                continue

            # Read from camera
            if camera := self._cameras.get((module_name, hardware_name)):
                camera_frame = camera.get_frame()
                if camera_frame is not None:
                    hardware_reads[hardware_name] = camera_frame.pack()

            # Read from IMU
            elif imu := self._imus.get((module_name, hardware_name)):
                imu_sample = imu.get_sample()
                if imu_sample is not None:
                    hardware_reads[hardware_name] = imu_sample.pack()

            # Read from radar
            elif radar := self._radars.get((module_name, hardware_name)):
                radar_scan = radar.get_scan()
                if radar_scan is not None:
                    hardware_reads[hardware_name] = radar_scan.pack()

            # Read from PIR sensor
            elif pir := self._pirs.get((module_name, hardware_name)):
                pir_status = pir.get_detection_status()
                if pir_status is not None:
                    hardware_reads[hardware_name] = pir_status.pack()

            # Read from actuator group
            else:
                joint_states = self._articulation.get_joint_states()
                if joint_states is not None:
                    hardware_reads[hardware_name] = JointStates(states=joint_states).pack()

        return hardware_reads

    def _write_node_hardware(self, module_name: str, node_name: str, hardware_writes: dict[str, bytes]) -> None:
        """
        Write hardware state from node execution.

        :param module_name: Module name.
        :param node_name: Node name.
        :param hardware_writes: Hardware writes keyed by hardware name.
        """

        node_def = next(m for m in self._ark_def.modules if m.name == module_name).nodes[node_name]
        for hardware_name, write_data in hardware_writes.items():
            access_mode = node_def.hardware_access.get(hardware_name)
            if access_mode not in (HardwareAccessMode.WRITE, HardwareAccessMode.READ_WRITE):
                continue

            # Write to actuator group
            targets = JointTargets.unpack(write_data)
            self._articulation.set_joint_targets(joint_targets=targets.targets)

    def _build_hardware(self) -> None:
        """
        Create articulation and sensor views from hardware configs.
        """

        actuator_group_configs = [
            cast(ActuatorGroupHardware, hardware.config)
            for hardware in self._ark_def.hardware
            if hardware.type == HardwareType.ACTUATOR_GROUP
        ]

        # Create single articulation view with all joint configs from actuator groups
        self._articulation = self._scene.add_articulation(
            path=self._base_path,
            joint_configs=sum([config.config.joint_configs for config in actuator_group_configs], []),
        )

        # Create sensor views
        self._cameras: dict[tuple[str, str], Camera] = {}
        self._imus: dict[tuple[str, str], Imu] = {}
        self._pirs: dict[tuple[str, str], PirSensor] = {}
        self._radars: dict[tuple[str, str], Radar] = {}
        for hardware in self._ark_def.hardware:
            if hardware.type == HardwareType.CAMERA:
                self._cameras[(hardware.module, hardware.name)] = self._scene.add_camera(
                    path=f"{self._base_path}{hardware.path}",
                    config=hardware.config,
                    local_pose=hardware.pose,
                )

            elif hardware.type == HardwareType.IMU:
                self._imus[(hardware.module, hardware.name)] = self._scene.add_imu(
                    path=f"{self._base_path}{hardware.path}",
                    config=hardware.config,
                    local_pose=hardware.pose,
                )

            elif hardware.type == HardwareType.PIR:
                self._pirs[(hardware.module, hardware.name)] = self._scene.add_pir_sensor(
                    path=f"{self._base_path}{hardware.path}",
                    config=hardware.config,
                    local_pose=hardware.pose,
                )

            elif hardware.type == HardwareType.RADAR:
                self._radars[(hardware.module, hardware.name)] = self._scene.add_radar(
                    path=f"{self._base_path}{hardware.path}",
                    config=hardware.config,
                    local_pose=hardware.pose,
                )

    def _load_ark_asset(self, world_pose: Pose | None = None, local_pose: Pose | None = None) -> None:
        """
        Load the asset for the Ark.

        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :raises SessionAssetError: If the asset file is not found.
        """

        if (asset_path := self._ark_ref.asset_path) is None or not os.path.exists(asset_path):
            raise SessionAssetError(f"Asset file not found for Ark {self._ark_def.name}")

        self._scene.add_asset(
            path=self._base_path,
            asset_file_path=asset_path,
            world_pose=world_pose,
            local_pose=local_pose,
        )
