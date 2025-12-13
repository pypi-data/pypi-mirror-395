from typing import Literal, overload

from antioch.session.ark import Ark
from antioch.session.objects import (
    Animation,
    Articulation,
    BasisCurve,
    Camera,
    Geometry,
    GroundPlane,
    Imu,
    Joint,
    Light,
    PirSensor,
    Radar,
    RigidBody,
    XForm,
    get_mesh_approximation,
    has_collision,
    remove_collision,
    set_collision,
    set_pir_material,
)
from antioch.session.session import SessionContainer
from common.core import ContainerSource, get_asset_path
from common.core.agent import Agent
from common.message import Pose, Vector3
from common.session.config import (
    ArticulationConfig,
    ArticulationJointConfig,
    BodyType,
    CameraConfig,
    CameraMode,
    DistortionModel,
    GeometryConfig,
    GeometryType,
    GroundPlaneConfig,
    ImuConfig,
    JointAxis,
    JointConfig,
    JointType,
    LightConfig,
    LightType,
    MeshApproximation,
    PirSensorConfig,
    RadarConfig,
    RigidBodyConfig,
)
from common.session.environment import SessionEnvironment
from common.session.sim import PrimAttributeValue, SceneQueryResponse, SceneTarget, SimulationInfo, SimulationTime


class Scene(SessionContainer):
    """
    Singleton wrapper for scene-level operations.

    Uses a lazy singleton pattern - the first instantiation or call to get_current()
    creates the instance, and all subsequent calls return the same instance.

    Provides low-level scene operations (clear, step, status) and factory methods
    for creating and retrieving views (add_*/get_* pattern).

    Example:
        scene = Scene()  # or Scene.get_current()
        scene.clear()
        scene.toggle_ui(show_ui=False)
        scene.play()
        scene.step(dt_us=1_000_000)

        # Add views
        geometry = scene.add_geometry(path="/World/box", ...)

        # Get existing views
        existing_geometry = scene.get_geometry(path="/World/box")

        # Query scene hierarchy
        from common.session.sim import SceneTarget
        all_prims = scene.query_scene(root_path="/World")
        cameras = scene.query_scene(target=SceneTarget.CAMERA)

        # Add Ark from registry
        ark = scene.add_ark(name="my_robot", version="1.0.0")

        # Add asset from registry
        scene.add_asset(path="/World/my_asset", name="asset_name", version="1.0.0")

        # Or add asset from file path
        scene.add_asset(path="/World/my_model", asset_file_path="/path/to/model.usdz")
    """

    _current: "Scene | None" = None
    _ark: "Ark | None" = None

    def __new__(cls) -> "Scene":
        if cls._current is None:
            cls._current = super().__new__(cls)
        return cls._current

    def __init__(self):
        """
        Initialize scene wrapper.
        """

        if not hasattr(self, "_initialized"):
            super().__init__()
            self._initialized = True
            self._agent = Agent()
            Scene._current = self

    @classmethod
    def get_current(cls) -> "Scene":
        """
        Get the current scene, creating it if it doesn't exist (lazy singleton).

        :return: The current scene.
        """

        if cls._current is None:
            cls._current = Scene()
        return cls._current

    @property
    def info(self) -> SimulationInfo:
        """
        Get comprehensive simulation info.

        :return: Info response with detailed simulation information.
        """

        return self._session.query_sim_rpc(
            endpoint="get_info",
            response_type=SimulationInfo,
        )

    @property
    def time_us(self) -> int:
        """
        Get the current simulation time in microseconds.

        :return: Current simulation time in microseconds.
        """

        return self._session.query_sim_rpc(
            endpoint="get_time",
            response_type=SimulationTime,
        ).time_us

    @property
    def ark(self):
        """
        Get the current Ark if one exists.

        :return: The current Ark or None.
        """

        return self._ark

    def add_ark(
        self,
        name: str,
        version: str,
        path: str = "/World",
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
        source: ContainerSource | None = None,
        debug: bool = False,
        timeout: float = 30.0,
    ) -> "Ark":
        """
        Add an Ark container at the specified path.

        This builds the entire Ark: loads definition, builds kinematics and hardware,
        starts containers via agent, and initializes scheduling. Everything is ready to run.

        :param name: Name of the Ark.
        :param version: Version of the Ark.
        :param path: USD path where the Ark will be built (default: "/World").
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :param source: Container image source.
        :param debug: Enable debug mode.
        :param timeout: Timeout in seconds for the Ark to start.
        :return: The fully initialized Ark container.
        """

        # Auto-select the container source based on session environment
        if source is None:
            source = ContainerSource.LOCAL if SessionEnvironment.check() == SessionEnvironment.LOCAL else ContainerSource.REMOTE

        self._ark = Ark(
            path=path,
            scene=self,
            name=name,
            version=version,
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
            source=source,
            debug=debug,
            timeout=timeout,
        )

        return self._ark

    def play(self) -> None:
        """
        Start or resume playing the simulation.

        Automatically starts the simulation if stopped, or resumes if paused.
        After playing, background rendering is disabled and the viewport is only
        updated with calls to step() or render().
        """

        self._session.query_sim_rpc(endpoint="play")

    def pause(self) -> None:
        """
        Pause the simulation.

        Freezes time but keeps physics initialized, enabling background rendering.
        """

        self._session.query_sim_rpc(endpoint="pause")

    def render(self) -> None:
        """
        Force render the simulation.
        """

        self._session.query_sim_rpc(endpoint="render")

    def step(self, dt_us: int = 1_000_000) -> None:
        """
        Step the simulation forward.

        The simulation must be playing before calling this method. Call play() first.
        If an Ark exists, delegates to Ark.step() which handles both node execution
        and physics stepping. Otherwise steps physics directly.

        :param dt_us: Amount of time to step in microseconds (default 1 second).
        :raises SessionSimRpcClientError: If simulation is not playing.
        """

        # Delegate to Ark if present
        if self._ark is not None:
            self._ark.step(dt_us)
            return

        # No Ark, step physics directly
        self._step_physics(dt_us)

    def set_simulation_controls(
        self,
        max_physics_dt_us: int | None = None,
        render_interval_us: int | None = None,
    ) -> None:
        """
        Set simulation control parameters.

        The max_physics_dt_us is the maximum physics step size in microseconds
        that will be used by the simulation backend. Setting a larger value will
        speed up the simulation, but may cause instability and lower the physics
        fidelity. You should generally stick to values between 1ms and 20ms.

        The render_interval_us is the interval in microseconds at which the viewport
        will be rendered **in simulation time**. Setting a larger value will reduce the
        number of renders and speed up the simulation, but may increase lag and jitter
        in the viewport. You should generally stick to values between 10ms and 100ms.

        :param max_physics_dt_us: Maximum physics timestep in microseconds.
        :param render_interval_us: Render interval in microseconds.
        :raises SessionSimRpcClientError: If parameters are invalid.
        """

        self._session.query_sim_rpc(
            endpoint="set_simulation_controls",
            payload={
                "max_physics_dt_us": max_physics_dt_us,
                "render_interval_us": render_interval_us,
            },
        )

    def clear(self, timeout: float = 30.0) -> None:
        """
        Clear and completely reset the scene.

        Stops any running Ark before clearing the scene.

        :param timeout: Timeout in seconds for stopping the Ark.
        """

        # Always try to stop the Ark via the agent (idempotent)
        self._agent.stop_ark(timeout=timeout)
        self._ark = None

        # Clear the simulation scene completely
        self._session.query_sim_rpc(endpoint="clear")

    def restart(self) -> None:
        """
        Restart the simulation container.

        This endpoint only works in Kubernetes environments. It sends SIGKILL to PID 1
        (the container entrypoint process), which will forcefully terminate the entire
        container and trigger a restart.

        Note: This function will not return as the process will be killed immediately.
        """

        # Always try to stop the Ark via the agent (idempotent)
        self._agent.stop_ark()
        self._ark = None

        # Restart the RPC container
        self._session.query_sim_rpc(endpoint="restart")

    def toggle_ui(self, show_ui: bool) -> None:
        """
        Toggle the Isaac Sim UI visibility.

        :param show_ui: Whether to show or hide the UI.
        """

        self._session.query_sim_rpc(
            endpoint="toggle_ui",
            payload={"show_ui": show_ui},
        )

    def set_camera_view(
        self,
        eye: Vector3 | list[float] | tuple[float, float, float],
        target: Vector3 | list[float] | tuple[float, float, float],
        camera_prim_path: str | None = None,
    ) -> None:
        """
        Set the viewport camera view position and target.

        :param eye: Eye position (camera location) in world coordinates.
        :param target: Target position (look-at point) in world coordinates.
        :param camera_prim_path: Optional USD path to the camera prim to configure.
        """

        self._session.query_sim_rpc(
            endpoint="set_camera_view",
            payload={
                "eye": Vector3.from_any(eye),
                "target": Vector3.from_any(target),
                "camera_prim_path": camera_prim_path,
            },
        )

    def set_active_viewport_camera(self, camera_prim_path: str) -> None:
        """
        Set which camera is active in the viewport.

        :param camera_prim_path: USD path to the camera prim to make active.
        """

        self._session.query_sim_rpc(
            endpoint="set_active_viewport_camera",
            payload={"camera_prim_path": camera_prim_path},
        )

    def get_prim_attribute(self, path: str, attribute_name: str) -> float | int | str | bool | list[float]:
        """
        Get an attribute value from any prim.

        Supports primitive and vector types: float, int, bool, string, Vec2/3/4, Quat.

        :param path: USD path to the prim.
        :param attribute_name: Name of the attribute to get.
        :return: The attribute value (scalar or list for vectors/quaternions).
        :raises ValueError: If prim or attribute doesn't exist, or type is unsupported.
        """

        return self._session.query_sim_rpc(
            endpoint="scene/get_prim_attribute_value",
            response_type=PrimAttributeValue,
            payload={"path": path, "attribute_name": attribute_name},
        ).value

    def set_prim_attribute(self, path: str, attribute_name: str, value: float | int | str | bool | list[float]) -> None:
        """
        Set an attribute value on any prim.

        Supports primitive and vector types: float, int, bool, string, Vec2/3/4, Quat.
        The attribute must already exist.

        :param path: USD path to the prim.
        :param attribute_name: Name of the attribute to set.
        :param value: The value to set (scalar or list for vectors/quaternions).
        :raises ValueError: If prim or attribute doesn't exist, or value is incompatible.
        """

        self._session.query_sim_rpc(
            endpoint="scene/set_prim_attribute_value",
            payload={"path": path, "attribute_name": attribute_name, "value": value},
        )

    def query_scene(self, root_path: str = "/World", target: SceneTarget | None = None) -> SceneQueryResponse:
        """
        Query the USD scene hierarchy for prims matching specific criteria.

        Traverses the scene starting from root_path and finds all prims that match
        the target type (or all applicable targets if target is None). This works
        regardless of simulation state.

        :param root_path: Root path to start the query from (default: "/World").
        :param target: Specific target type to filter for (None returns all).
        :return: Scene query response with matching prims and their applicable targets.
        """

        return self._session.query_sim_rpc(
            endpoint="scene/query_hierarchy",
            response_type=SceneQueryResponse,
            payload={"root_path": root_path, "target": target},
        )

    def delete_prim(self, path: str) -> None:
        """
        Delete a prim from the scene.

        :param path: USD path for the prim to delete.
        """

        self._session.query_sim_rpc(endpoint="scene/delete_prim", payload={"path": path})

    def add_asset(
        self,
        path: str,
        name: str | None = None,
        version: str | None = None,
        asset_file_path: str | None = None,
        asset_prim_path: str | None = None,
        remove_articulation: bool = True,
        remove_rigid_body: bool = False,
        remove_sensors: bool = False,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
        scale: Vector3 | list[float] | tuple[float, float, float] | None = None,
    ) -> str:
        """
        Add and convert an asset file (FBX, OBJ, glTF, USD, etc) to USD.

        Either provide asset_file_path directly OR provide both name and version to load from
        the asset registry. Exactly one option must be used.

        :param path: USD path where the asset will be added (e.g., "/World/my_model").
        :param name: Name of the asset in the registry (requires version).
        :param version: Version of the asset in the registry (requires name).
        :param asset_file_path: Path to the asset file (FBX, OBJ, glTF, STL, USD, etc).
        :param asset_prim_path: Full path to prim in the USD file to reference.
        :param remove_articulation: Whether to remove articulation APIs.
        :param remove_rigid_body: Whether to remove rigid body APIs.
        :param remove_sensors: Whether to remove sensor and graph prims.
        :param world_pose: Optional world pose as Pose (or dict with position/orientation lists).
        :param local_pose: Optional local pose as Pose (or dict with position/orientation lists).
        :param scale: Optional scale as Vector3 (or list/tuple of 3 floats).
        :raises ValueError: If neither option or both options are provided.
        """

        # Validate that exactly one option is provided
        has_file_path = asset_file_path is not None
        has_name_version = name is not None and version is not None
        has_partial_name_version = (name is not None) != (version is not None)
        if has_partial_name_version:
            raise ValueError("Both name and version must be provided together")
        if not has_file_path and not has_name_version:
            raise ValueError("Either asset_file_path or both name and version must be provided")
        if has_file_path and has_name_version:
            raise ValueError("Cannot provide both asset_file_path and name/version")

        # Resolve asset file path from registry if name/version provided
        if has_name_version:
            if name is None or version is None:
                raise ValueError("Name and version must be provided together")
            asset_file_path = str(get_asset_path(name=name, version=version, assert_exists=True))

        if not asset_file_path:
            raise ValueError("Asset file path is required")
        self._session.query_sim_rpc(
            endpoint="scene/add_asset",
            payload={
                "path": path,
                "asset_file_path": asset_file_path,
                "asset_prim_path": asset_prim_path,
                "remove_articulation": remove_articulation,
                "remove_rigid_body": remove_rigid_body,
                "remove_sensors": remove_sensors,
                "world_pose": Pose.from_any(world_pose) if world_pose is not None else None,
                "local_pose": Pose.from_any(local_pose) if local_pose is not None else None,
                "scale": Vector3.from_any(scale) if scale is not None else None,
            },
        )
        return path

    def add_geometry(
        self,
        path: str,
        geometry_type: GeometryType,
        radius: float | None = None,
        height: float | None = None,
        size: float | None = None,
        color: Vector3 | list[float] | tuple[float, float, float] | None = None,
        opacity: float = 1.0,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
        enable_collision: bool = True,
        static_friction: float = 0.5,
        dynamic_friction: float = 0.5,
        restitution: float = 0.2,
        mesh_file_path: str | None = None,
        mesh_approximation: MeshApproximation = MeshApproximation.CONVEX_DECOMPOSITION,
        contact_offset: float | None = None,
        rest_offset: float | None = None,
        torsional_patch_radius: float | None = None,
        min_torsional_patch_radius: float | None = None,
    ) -> Geometry:
        """
        Add geometry to the scene.

        :param path: USD path for the geometry.
        :param geometry_type: Type of geometry (sphere, cube, cylinder, cone, capsule, mesh).
        :param radius: Radius for sphere/cylinder/cone/capsule.
        :param height: Height for cylinder/cone/capsule.
        :param size: Size for cube (uniform).
        :param color: RGB color as Vector3 (or list/tuple of 3 floats) with values 0-1.
        :param opacity: Opacity from 0 (transparent) to 1 (opaque).
        :param world_pose: Optional world pose as Pose (or dict with position/orientation lists).
        :param local_pose: Optional local pose as Pose (or dict with position/orientation lists).
        :param enable_collision: Whether to enable collision.
        :param static_friction: Static friction coefficient.
        :param dynamic_friction: Dynamic friction coefficient.
        :param restitution: Restitution (bounciness).
        :param mesh_file_path: Path to mesh file (FBX, OBJ, glTF, STL, etc.) - required for MESH type.
        :param mesh_approximation: Collision mesh approximation method (for meshes).
        :param contact_offset: Distance at which collision detection begins.
        :param rest_offset: Minimum separation distance between objects.
        :param torsional_patch_radius: Radius for torsional friction calculations.
        :param min_torsional_patch_radius: Minimum radius for torsional friction.
        :return: The geometry instance.
        """

        return Geometry.add(
            path=path,
            config=GeometryConfig(
                geometry_type=geometry_type,
                radius=radius,
                height=height,
                size=size,
                color=Vector3.from_any(color) if color is not None else None,
                opacity=opacity,
                enable_collision=enable_collision,
                static_friction=static_friction,
                dynamic_friction=dynamic_friction,
                restitution=restitution,
                mesh_file_path=mesh_file_path,
                mesh_approximation=mesh_approximation,
                contact_offset=contact_offset,
                rest_offset=rest_offset,
                torsional_patch_radius=torsional_patch_radius,
                min_torsional_patch_radius=min_torsional_patch_radius,
            ),
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
        )

    def get_geometry(self, path: str) -> Geometry:
        """
        Get existing geometry from the scene.

        :param path: USD path for the geometry.
        :return: The geometry instance.
        """

        return Geometry(path)

    def add_articulation(
        self,
        path: str,
        joint_configs: list[ArticulationJointConfig] | None = None,
        solver_position_iterations: int = 32,
        solver_velocity_iterations: int = 1,
        sleep_threshold: float = 0.005,
        stabilization_threshold: float = 0.001,
        enable_self_collisions: bool = False,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
        scale: Vector3 | list[float] | tuple[float, float, float] | None = None,
    ) -> Articulation:
        """
        Add an articulation to the scene.

        :param path: USD path for the articulation.
        :param joint_configs: Per-joint configurations (stiffness, damping, limits, etc).
        :param solver_position_iterations: Number of position iterations for the solver.
        :param solver_velocity_iterations: Number of velocity iterations for the solver.
        :param sleep_threshold: Sleep threshold for the articulation.
        :param stabilization_threshold: Stabilization threshold for the articulation.
        :param enable_self_collisions: Whether to enable self-collisions.
        :param world_pose: Optional world pose as Pose (or dict with position/orientation lists).
        :param local_pose: Optional local pose as Pose (or dict with position/orientation lists).
        :param scale: Optional scale as Vector3 (or list/tuple of 3 floats).
        :return: The articulation instance.
        """

        return Articulation.add(
            path=path,
            config=ArticulationConfig(
                solver_position_iterations=solver_position_iterations,
                solver_velocity_iterations=solver_velocity_iterations,
                sleep_threshold=sleep_threshold,
                stabilization_threshold=stabilization_threshold,
                enable_self_collisions=enable_self_collisions,
                joint_configs=joint_configs or [],
            ),
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
            scale=Vector3.from_any(scale) if scale is not None else None,
        )

    def get_articulation(self, path: str) -> Articulation:
        """
        Get an existing articulation from the scene.

        :param path: USD path for the articulation.
        :return: The articulation instance.
        """

        return Articulation(path)

    def add_joint(
        self,
        path: str,
        parent_path: str,
        child_path: str,
        pose: Pose | dict | None = None,
        joint_type: JointType = JointType.FIXED,
        axis: JointAxis = JointAxis.X,
        lower_limit: float | None = None,
        upper_limit: float | None = None,
        friction: float = 0.01,
        armature: float = 0.1,
        exclude_from_articulation: bool = False,
    ) -> Joint:
        """
        Add a joint to the scene.

        :param path: USD path for the joint.
        :param parent_path: USD path to parent body.
        :param child_path: USD path to child body.
        :param pose: Joint pose relative to parent (defaults to identity).
        :param joint_type: Type of joint motion (FIXED, REVOLUTE, PRISMATIC).
        :param axis: Axis of motion for non-fixed joints.
        :param lower_limit: Lower motion limit (degrees for revolute, meters for prismatic).
        :param upper_limit: Upper motion limit (degrees for revolute, meters for prismatic).
        :param friction: Joint friction coefficient (unitless).
        :param armature: Joint armature (kg for prismatic, kg-m^2 for revolute).
        :param exclude_from_articulation: Whether to exclude this joint from articulation.
        :return: The joint instance.
        """

        return Joint.add(
            path=path,
            config=JointConfig(
                parent_path=parent_path,
                child_path=child_path,
                pose=Pose.from_any(pose) if pose is not None else Pose.identity(),
                joint_type=joint_type,
                axis=axis,
                lower_limit=lower_limit,
                upper_limit=upper_limit,
                friction=friction,
                armature=armature,
                exclude_from_articulation=exclude_from_articulation,
            ),
        )

    def get_joint(self, path: str) -> Joint:
        """
        Get an existing joint from the scene.

        :param path: USD path for the joint.
        :return: The joint instance.
        """

        return Joint(path)

    def add_rigid_body(
        self,
        path: str,
        body_type: BodyType = BodyType.DYNAMIC,
        mass: float = 1.0,
        density: float | None = None,
        center_of_mass: Vector3 | list[float] | tuple[float, float, float] | None = None,
        diagonal_inertia: Vector3 | list[float] | tuple[float, float, float] | None = None,
        principal_axes: Vector3 | list[float] | tuple[float, float, float] | None = None,
        sleep_threshold: float | None = None,
        linear_velocity: Vector3 | list[float] | tuple[float, float, float] | None = None,
        angular_velocity: Vector3 | list[float] | tuple[float, float, float] | None = None,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
        scale: Vector3 | list[float] | tuple[float, float, float] | None = None,
    ) -> RigidBody:
        """
        Add rigid body physics to the scene.

        :param path: USD path for the rigid body.
        :param body_type: Body type (dynamic or kinematic).
        :param mass: Mass in kg.
        :param density: Density in kg/m³ (alternative to mass).
        :param center_of_mass: Center of mass offset as Vector3 (or list/tuple) in body frame.
        :param diagonal_inertia: Diagonal inertia values as Vector3 (or list/tuple).
        :param principal_axes: Principal axes orientation as RPY Vector3 (or list/tuple).
        :param sleep_threshold: Mass-normalized kinetic energy threshold for sleeping.
        :param linear_velocity: Initial linear velocity as Vector3 (or list/tuple).
        :param angular_velocity: Initial angular velocity as Vector3 (or list/tuple).
        :param world_pose: Optional world pose as Pose (or dict with position/orientation lists).
        :param local_pose: Optional local pose as Pose (or dict with position/orientation lists).
        :param scale: Optional scale as Vector3 (or list/tuple of 3 floats).
        :return: The rigid body instance.
        """

        return RigidBody.add(
            path=path,
            config=RigidBodyConfig(
                body_type=body_type,
                mass=mass,
                density=density,
                center_of_mass=Vector3.from_any(center_of_mass) if center_of_mass is not None else None,
                diagonal_inertia=Vector3.from_any(diagonal_inertia) if diagonal_inertia is not None else None,
                principal_axes=Vector3.from_any(principal_axes) if principal_axes is not None else None,
                sleep_threshold=sleep_threshold,
                linear_velocity=Vector3.from_any(linear_velocity) if linear_velocity is not None else None,
                angular_velocity=Vector3.from_any(angular_velocity) if angular_velocity is not None else None,
            ),
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
            scale=Vector3.from_any(scale) if scale is not None else None,
        )

    def get_rigid_body(self, path: str) -> RigidBody:
        """
        Get an existing rigid body from the scene.

        :param path: USD path for the rigid body.
        :return: The rigid body instance.
        """

        return RigidBody(path)

    def add_light(
        self,
        path: str,
        light_type: LightType = LightType.SPHERE,
        intensity: float = 30000.0,
        exposure: float = 10.0,
        color: Vector3 | list[float] | tuple[float, float, float] | None = None,
        radius: float = 0.1,
        width: float | None = None,
        height: float | None = None,
        length: float | None = None,
        angle: float | None = None,
        texture_file: str | None = None,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
    ) -> Light:
        """
        Add a light to the scene.

        :param path: USD path for the light.
        :param light_type: Type of light (sphere, rect, disk, cylinder, distant, dome).
        :param intensity: Light intensity.
        :param exposure: Light exposure value.
        :param color: RGB color as Vector3 (or list/tuple of 3 floats) with values 0-1 (defaults to white).
        :param radius: Light radius in meters (for sphere lights).
        :param width: Width in meters (for rect lights).
        :param height: Height in meters (for rect/cylinder lights).
        :param length: Length in meters (for cylinder lights).
        :param angle: Angle in degrees (for distant lights).
        :param texture_file: Path to texture file (for dome lights).
        :param world_pose: Optional world pose as Pose (or dict with position/orientation lists).
        :param local_pose: Optional local pose as Pose (or dict with position/orientation lists).
        :return: The light instance.
        """

        return Light.add(
            path=path,
            config=LightConfig(
                light_type=light_type,
                intensity=intensity,
                exposure=exposure,
                color=Vector3.from_any(color) if color is not None else Vector3(data=(1.0, 1.0, 1.0)),
                radius=radius,
                width=width,
                height=height,
                length=length,
                angle=angle,
                texture_file=texture_file,
            ),
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
        )

    def get_light(self, path: str) -> Light:
        """
        Get an existing light from the scene.

        :param path: USD path for the light.
        :return: The light instance.
        """

        return Light(path)

    def add_xform(
        self,
        path: str,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
        scale: Vector3 | list[float] | tuple[float, float, float] | None = None,
    ) -> XForm:
        """
        Add an xform to the scene.

        :param path: USD path for the xform.
        :param world_pose: Optional world pose as Pose (or dict with position/orientation lists).
        :param local_pose: Optional local pose as Pose (or dict with position/orientation lists).
        :param scale: Optional scale as Vector3 (or list/tuple of 3 floats).
        :return: The xform instance.
        """

        return XForm.add(
            path=path,
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
            scale=Vector3.from_any(scale) if scale is not None else None,
        )

    def get_xform(self, path: str) -> XForm:
        """
        Get an existing xform from the scene.

        :param path: USD path for the xform.
        :return: The xform instance.
        """

        return XForm(path)

    @overload
    def add_animation(
        self,
        path: str,
        *,
        waypoints: list[Vector3],
        loop: bool = True,
    ) -> Animation: ...

    @overload
    def add_animation(
        self,
        path: str,
        *,
        basis_curve: str,
        samples_per_segment: int = 10,
        sort_by: Literal["X", "Y", "Z"] | None = None,
        ascending: bool = True,
    ) -> Animation: ...

    def add_animation(
        self,
        path: str,
        *,
        waypoints: list[Vector3] | None = None,
        basis_curve: str | None = None,
        samples_per_segment: int = 10,
        sort_by: Literal["X", "Y", "Z"] | None = None,
        ascending: bool = True,
        loop: bool = True,
    ) -> Animation:
        """
        Add an animation to the scene.

        :param path: USD path for the animation (must contain a skeleton root).
        :param waypoints: List of waypoints for the animation path.
        :param basis_curve: Path to the basis curve to use for the animation.
        :param samples_per_segment: The number of samples per segment to use from the basis curve.
        :param sort_by: The axis to sort the points by.
        :param ascending: Whether to sort the points in ascending order.
        :param loop: Whether to loop the animation.
        :return: The animation instance.
        :raises ValueError: If both waypoints and basis curve are provided.
        :raises ValueError: If neither waypoints nor basis curve are provided.
        """
        if waypoints is not None and basis_curve is not None:
            raise ValueError("Must specify either waypoints or basis curve")
        if waypoints is not None:
            return Animation.add(
                path=path,
                waypoints=waypoints,
                loop=loop,
            )
        elif basis_curve is not None:
            return Animation.add(
                path=path,
                basis_curve=basis_curve,
                samples_per_segment=samples_per_segment,
                sort_by=sort_by,
                ascending=ascending,
            )
        else:
            raise ValueError("Must specify either waypoints or basis curve")

    def get_animation(self, path: str) -> Animation:
        """
        Get an existing animation from the scene.

        :param path: USD path for the animation.
        :return: The animation instance.
        """

        return Animation(path)

    def add_ground_plane(
        self,
        path: str,
        size: float = 5000.0,
        z_position: float = 0.0,
        color: Vector3 | list[float] | tuple[float, float, float] | None = None,
        static_friction: float = 0.5,
        dynamic_friction: float = 0.5,
        restitution: float = 0.0,
    ) -> GroundPlane:
        """
        Add a ground plane to the scene.

        :param path: USD path for the ground plane.
        :param size: Size of the ground plane in meters.
        :param z_position: Z position of the ground plane.
        :param color: RGB color as Vector3 (or list/tuple of 3 floats) with values 0-1 (defaults to gray).
        :param static_friction: Friction when objects are not moving.
        :param dynamic_friction: Friction when objects are sliding.
        :param restitution: Bounciness of collisions (0=no bounce, 1=perfect bounce).
        :return: The ground plane instance.
        """

        return GroundPlane.add(
            path=path,
            config=GroundPlaneConfig(
                size=size,
                z_position=z_position,
                color=Vector3.from_any(color) if color is not None else Vector3(data=(0.5, 0.5, 0.5)),
                static_friction=static_friction,
                dynamic_friction=dynamic_friction,
                restitution=restitution,
            ),
        )

    def get_ground_plane(self, path: str) -> GroundPlane:
        """
        Get an existing ground plane from the scene.

        :param path: USD path for the ground plane.
        :return: The ground plane instance.
        """

        return GroundPlane(path)

    def add_camera(
        self,
        path: str,
        config: CameraConfig | None = None,
        mode: CameraMode = CameraMode.RGB,
        frequency: int = 30,
        width: int = 640,
        height: int = 480,
        focal_length: float = 50.0,
        sensor_width: float = 20.4,
        sensor_height: float = 15.3,
        near_clip: float = 0.1,
        far_clip: float = 1000.0,
        f_stop: float = 0.0,
        focus_distance: float = 10.0,
        principal_point_x: float = 0.0,
        principal_point_y: float = 0.0,
        distortion_model: DistortionModel = DistortionModel.PINHOLE,
        distortion_coefficients: list[float] | None = None,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
    ) -> Camera:
        """
        Add a camera to the scene.

        :param path: USD path for the camera.
        :param config: Optional camera configuration (alternative to individual parameters).
        :param mode: Camera capture mode (RGB or depth).
        :param frequency: Camera update frequency in Hz.
        :param width: Image width in pixels.
        :param height: Image height in pixels.
        :param focal_length: Focal length in mm.
        :param sensor_width: Physical sensor width in mm.
        :param sensor_height: Physical sensor height in mm.
        :param near_clip: Near clipping plane in meters.
        :param far_clip: Far clipping plane in meters.
        :param f_stop: F-stop for depth of field.
        :param focus_distance: Focus distance in meters.
        :param principal_point_x: Principal point X offset in pixels.
        :param principal_point_y: Principal point Y offset in pixels.
        :param distortion_model: Lens distortion model.
        :param distortion_coefficients: Distortion coefficients.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The camera instance.
        """

        if config is None:
            config = CameraConfig(
                mode=mode,
                frequency=frequency,
                width=width,
                height=height,
                focal_length=focal_length,
                sensor_width=sensor_width,
                sensor_height=sensor_height,
                near_clip=near_clip,
                far_clip=far_clip,
                f_stop=f_stop,
                focus_distance=focus_distance,
                principal_point_x=principal_point_x,
                principal_point_y=principal_point_y,
                distortion_model=distortion_model,
                distortion_coefficients=distortion_coefficients,
            )

        return Camera.add(
            path=path,
            config=config,
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
        )

    def get_camera(self, path: str) -> Camera:
        """
        Get existing camera from the scene.

        :param path: USD path for the camera.
        :return: The camera instance.
        """

        return Camera(path)

    def add_imu(
        self,
        path: str,
        config: ImuConfig | None = None,
        frequency: int | None = None,
        linear_acceleration_filter_size: int = 10,
        angular_velocity_filter_size: int = 10,
        orientation_filter_size: int = 10,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
    ) -> Imu:
        """
        Add an IMU to the scene.

        :param path: USD path for the IMU.
        :param config: Optional IMU configuration (alternative to individual parameters).
        :param frequency: Sensor update frequency in Hz (optional, defaults to physics rate).
        :param linear_acceleration_filter_size: Filter window size for linear acceleration.
        :param angular_velocity_filter_size: Filter window size for angular velocity.
        :param orientation_filter_size: Filter window size for orientation.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The IMU instance.
        """

        if config is None:
            config = ImuConfig(
                frequency=frequency,
                linear_acceleration_filter_size=linear_acceleration_filter_size,
                angular_velocity_filter_size=angular_velocity_filter_size,
                orientation_filter_size=orientation_filter_size,
            )

        return Imu.add(
            path=path,
            config=config,
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
        )

    def get_imu(self, path: str) -> Imu:
        """
        Get existing IMU from the scene.

        :param path: USD path for the IMU.
        :return: The IMU instance.
        """

        return Imu(path)

    def add_radar(
        self,
        path: str,
        config: RadarConfig | None = None,
        frequency: int = 10,
        max_azimuth: float = 66.0,
        max_elevation: float = 20.0,
        max_range: float = 200.0,
        range_resolution: float = 0.4,
        azimuth_resolution: float = 1.3,
        elevation_resolution: float = 5.0,
        azimuth_noise: float = 0.0,
        range_noise: float = 0.0,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
    ) -> Radar:
        """
        Add a radar to the scene.

        :param path: USD path for the radar.
        :param config: Optional radar configuration (alternative to individual parameters).
        :param frequency: Sensor update frequency in Hz.
        :param max_azimuth: Maximum azimuth angle in degrees (±FOV from center).
        :param max_elevation: Maximum elevation angle in degrees (±FOV from center).
        :param max_range: Maximum detection range in meters.
        :param range_resolution: Range resolution in meters.
        :param azimuth_resolution: Azimuth resolution at boresight in degrees.
        :param elevation_resolution: Elevation resolution at boresight in degrees.
        :param azimuth_noise: Azimuth measurement noise standard deviation in radians.
        :param range_noise: Range measurement noise standard deviation in meters.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The radar instance.
        """

        if config is None:
            config = RadarConfig(
                frequency=frequency,
                max_azimuth=max_azimuth,
                max_elevation=max_elevation,
                max_range=max_range,
                range_resolution=range_resolution,
                azimuth_resolution=azimuth_resolution,
                elevation_resolution=elevation_resolution,
                azimuth_noise=azimuth_noise,
                range_noise=range_noise,
            )

        return Radar.add(
            path=path,
            config=config,
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
        )

    def add_basis_curve_semi_circle(
        self,
        path: str,
        center: Vector3 | list[float] | tuple[float, float, float] = Vector3.zeros(),
        radius: float = 1.0,
        min_angle_deg: float = 0.0,
        max_angle_deg: float = 180.0,
        guide: bool = False,
        color: Vector3 | list[float] | tuple[float, float, float] | None = None,
        width: float = 0.005,
    ) -> BasisCurve:
        """
        Add a basis curve semi-circle to the scene.

        :param path: USD path for the basis curve.
        :param center: Center of the basis curve.
        :param radius: Radius of the basis curve.
        :param min_angle_deg: Minimum angle of the basis curve in degrees.
        :param max_angle_deg: Maximum angle of the basis curve in degrees.
        :param guide: If True, mark as guide purpose (invisible to cameras). If False, default purpose.
        :param color: Optional RGB color [0-1].
        :param width: Width of the curve.
        :return: The basis curve instance.
        """

        return BasisCurve.add(
            path=path,
            center=Vector3.from_any(center),
            radius=radius,
            min_angle_deg=min_angle_deg,
            max_angle_deg=max_angle_deg,
            guide=guide,
            color=Vector3.from_any(color) if color is not None else None,
            width=width,
        )

    @overload
    def add_basis_curve_line(
        self,
        path: str,
        *,
        start: Vector3 | list[float] | tuple[float, float, float],
        end: Vector3 | list[float] | tuple[float, float, float],
        guide: bool = False,
        color: Vector3 | list[float] | tuple[float, float, float] | None = None,
        width: float = 0.005,
    ) -> BasisCurve: ...

    @overload
    def add_basis_curve_line(
        self,
        path: str,
        *,
        start: Vector3 | list[float] | tuple[float, float, float],
        angle_deg: float,
        length: float,
        guide: bool = False,
        color: Vector3 | list[float] | tuple[float, float, float] | None = None,
        width: float = 0.005,
    ) -> BasisCurve: ...

    def add_basis_curve_line(
        self,
        path: str,
        *,
        start: Vector3 | list[float] | tuple[float, float, float],
        end: Vector3 | list[float] | tuple[float, float, float] | None = None,
        angle_deg: float | None = None,
        length: float | None = None,
        guide: bool = False,
        color: Vector3 | list[float] | tuple[float, float, float] | None = None,
        width: float = 0.005,
    ) -> BasisCurve:
        """
        Add a basis curve line to the scene.

        Supports two modes:
        - Cartesian: Provide start and end points directly
        - Polar: Provide start point, angle (degrees from +X axis in XY plane), and length

        Examples:
            # Cartesian mode
            line = scene.add_basis_curve_line(
                "/World/line1",
                start=[0, 0, 0],
                end=[1, 1, 0],
            )

            # Polar mode
            line = scene.add_basis_curve_line(
                "/World/line2",
                start=[0, 0, 0],
                angle_deg=45.0,
                length=2.0,
            )

        :param path: USD path for the basis curve.
        :param start: Start point of the line.
        :param end: End point of the line (Cartesian mode).
        :param angle_deg: Angle in degrees from +X axis in XY plane (polar mode).
        :param length: Length of the line (polar mode).
        :param guide: If True, mark as guide purpose (invisible to cameras). If False, default purpose.
        :param color: Optional RGB color [0-1].
        :param width: Width of the curve.
        :return: The basis curve instance.
        :raises ValueError: If both modes are specified or neither mode is complete.
        """
        if end is not None and (angle_deg is not None or length is not None):
            raise ValueError("Cannot specify both end point and angle/length in Cartesian mode")
        if end is None and angle_deg is None and length is None:
            raise ValueError("Must specify either end point or angle/length")
        if length is not None and angle_deg is None:
            raise ValueError("Must specify angle when length is provided")
        if angle_deg is not None and length is None:
            raise ValueError("Must specify length when angle is provided")

        return BasisCurve.add_line(
            path=path,
            start=Vector3.from_any(start),
            end=Vector3.from_any(end) if end is not None else None,
            angle_deg=angle_deg,
            length=length,
            guide=guide,
            color=Vector3.from_any(color) if color is not None else None,
            width=width,
        )

    def get_basis_curve(self, path: str) -> BasisCurve:
        """
        Get existing basis curve from the scene.

        :param path: USD path for the basis curve.
        :return: The basis curve instance.
        """

        return BasisCurve(path)

    def get_radar(self, path: str) -> Radar:
        """
        Get existing radar from the scene.

        :param path: USD path for the radar.
        :return: The radar instance.
        """

        return Radar(path)

    def add_pir_sensor(
        self,
        path: str,
        config: PirSensorConfig | None = None,
        update_rate_hz: float = 60.0,
        max_range: float = 20.0,
        total_horiz_fov_deg: float = 150.0,
        sensor_side_fov_deg: float = 45.0,
        sensor_center_fov_deg: float = 45.0,
        sensor_rays_horiz: int = 128,
        sensor_rays_vert: int = 16,
        min_vertical_angle_center: float = -30.0,
        max_vertical_angle_center: float = 30.0,
        min_vertical_angle_side: float = -30.0,
        max_vertical_angle_side: float = 30.0,
        gain_center: float = 0.015,
        gain_sides: float = 0.01,
        hp_corner_hz: float = 0.4,
        lp_corner_hz: float = 10.0,
        threshold: float | None = None,
        threshold_scale: float = 1.0,
        blind_time_s: float = 0.5,
        pulse_counter: int = 2,
        window_time_s: float = 2.0,
        count_mode: int = 0,
        lens_transmission: float = 0.9,
        lens_segments_h: int = 6,
        ambient_temp_c: float = 20.0,
        thermal_time_constant_s: float = 0.2,
        pyro_responsivity: float = 4000.0,
        noise_amplitude: float = 20e-6,
        target_delta_t: float = 10.0,
        target_distance: float = 5.0,
        target_emissivity: float = 0.98,
        target_velocity_mps: float = 1.0,
        world_pose: Pose | dict | None = None,
        local_pose: Pose | dict | None = None,
    ) -> PirSensor:
        """
        Add a PIR (Passive Infrared) sensor to the scene.

        PIR sensors detect infrared radiation changes caused by moving warm objects.
        The sensor uses a dual-element design with interleaved zones for motion detection.

        :param path: USD path for the PIR sensor.
        :param config: Optional PIR sensor configuration (alternative to individual parameters).
        :param update_rate_hz: Sensor update frequency in Hz.
        :param max_range: Maximum detection range in meters.
        :param total_horiz_fov_deg: Total horizontal coverage in degrees. Enables automatic fanning.
        :param sensor_side_fov_deg: Horizontal FOV for side sensors in degrees.
        :param sensor_center_fov_deg: Horizontal FOV for center sensor in degrees.
        :param sensor_rays_horiz: Number of rays per sensor in horizontal direction.
        :param sensor_rays_vert: Number of rays per sensor in vertical direction.
        :param min_vertical_angle_center: Minimum vertical angle for center sensor in degrees.
        :param max_vertical_angle_center: Maximum vertical angle for center sensor in degrees.
        :param min_vertical_angle_side: Minimum vertical angle for side sensors in degrees.
        :param max_vertical_angle_side: Maximum vertical angle for side sensors in degrees.
        :param gain_center: Amplifier gain for center sensor.
        :param gain_sides: Amplifier gain for side sensors.
        :param hp_corner_hz: High-pass filter corner frequency in Hz.
        :param lp_corner_hz: Low-pass filter corner frequency in Hz.
        :param threshold: Detection threshold (auto-calibrated if None).
        :param threshold_scale: Scale factor applied to auto-calibrated threshold.
        :param blind_time_s: Blind time after detection in seconds.
        :param pulse_counter: Number of pulses required to trigger detection (1-4).
        :param window_time_s: Window time for pulse counting in seconds.
        :param count_mode: Pulse counting mode (0 = sign change required, 1 = any crossing).
        :param lens_transmission: Lens transmission coefficient (0-1).
        :param lens_segments_h: Number of horizontal lens segments (facets).
        :param ambient_temp_c: Ambient temperature in Celsius.
        :param thermal_time_constant_s: Pyroelectric element thermal time constant in seconds.
        :param pyro_responsivity: Pyroelectric responsivity scaling factor.
        :param noise_amplitude: Thermal/electronic noise amplitude.
        :param target_delta_t: Target temperature difference for threshold calibration in Celsius.
        :param target_distance: Target distance for threshold calibration in meters.
        :param target_emissivity: Target emissivity for threshold calibration.
        :param target_velocity_mps: Target velocity for threshold calibration in m/s.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The PIR sensor instance.
        """

        if config is None:
            config = PirSensorConfig(
                update_rate_hz=update_rate_hz,
                max_range=max_range,
                total_horiz_fov_deg=total_horiz_fov_deg,
                sensor_side_fov_deg=sensor_side_fov_deg,
                sensor_center_fov_deg=sensor_center_fov_deg,
                sensor_rays_horiz=sensor_rays_horiz,
                sensor_rays_vert=sensor_rays_vert,
                min_vertical_angle_center=min_vertical_angle_center,
                max_vertical_angle_center=max_vertical_angle_center,
                min_vertical_angle_side=min_vertical_angle_side,
                max_vertical_angle_side=max_vertical_angle_side,
                gain_center=gain_center,
                gain_sides=gain_sides,
                hp_corner_hz=hp_corner_hz,
                lp_corner_hz=lp_corner_hz,
                threshold=threshold,
                threshold_scale=threshold_scale,
                blind_time_s=blind_time_s,
                pulse_counter=pulse_counter,
                window_time_s=window_time_s,
                count_mode=count_mode,
                lens_transmission=lens_transmission,
                lens_segments_h=lens_segments_h,
                ambient_temp_c=ambient_temp_c,
                thermal_time_constant_s=thermal_time_constant_s,
                pyro_responsivity=pyro_responsivity,
                noise_amplitude=noise_amplitude,
                target_delta_t=target_delta_t,
                target_distance=target_distance,
                target_emissivity=target_emissivity,
                target_velocity_mps=target_velocity_mps,
            )

        return PirSensor.add(
            path=path,
            config=config,
            world_pose=Pose.from_any(world_pose) if world_pose is not None else None,
            local_pose=Pose.from_any(local_pose) if local_pose is not None else None,
        )

    def get_pir_sensor(self, path: str) -> PirSensor:
        """
        Get existing PIR sensor from the scene.

        :param path: USD path for the PIR sensor.
        :return: The PIR sensor instance.
        """

        return PirSensor(path)

    def set_collision(self, path: str, mesh_approximation: MeshApproximation | None = None) -> None:
        """
        Apply collision API to a prim.

        :param path: USD path to the prim.
        :param mesh_approximation: Optional mesh approximation method for collision geometry.
        """

        set_collision(path, mesh_approximation)

    def remove_collision(self, path: str) -> None:
        """
        Remove collision API from a prim.

        :param path: USD path to the prim.
        """

        remove_collision(path)

    def has_collision(self, path: str) -> bool:
        """
        Check if a prim has collision API applied.

        :param path: USD path to the prim.
        :return: True if collision API is applied.
        """

        return has_collision(path)

    def get_mesh_approximation(self, path: str) -> MeshApproximation | None:
        """
        Get mesh collision approximation from a prim.

        :param path: USD path to the prim.
        :return: Mesh approximation method, or None if not set.
        """

        return get_mesh_approximation(path)

    def set_pir_material(self, path: str, emissivity: float = 0.9, temperature_c: float | None = None) -> None:
        """
        Set PIR-specific thermal properties on a prim.

        These properties define how the prim appears to PIR sensors:
        - emissivity: How well the surface emits infrared radiation (0-1)
        - temperature_c: Surface temperature in Celsius

        Example:
            scene.set_pir_material("/World/person", emissivity=0.98, temperature_c=37.0)

        :param path: USD path of the prim to configure.
        :param emissivity: Material emissivity (0-1, default 0.9).
        :param temperature_c: Surface temperature in Celsius (optional).
        """

        set_pir_material(path, emissivity, temperature_c)

    def set_nonvisual_material(self, path: str, base: str, coating: str = "none", attribute: str = "none") -> int:
        """
        Set non-visual material properties on all Material prims in a subtree.

        These properties define how objects appear to RTX sensors (LiDAR and Radar).

        Valid base materials:
            Metals: aluminum, steel, oxidized_steel, iron, oxidized_iron, silver, brass,
                    bronze, oxidized_bronze_patina, tin
            Polymers: plastic, fiberglass, carbon_fiber, vinyl, plexiglass, pvc, nylon, polyester
            Glass: clear_glass, frosted_glass, one_way_mirror, mirror, ceramic_glass
            Other: asphalt, concrete, leaf_grass, dead_leaf_grass, rubber, wood, bark,
                   cardboard, paper, fabric, skin, fur_hair, leather, marble, brick,
                   stone, gravel, dirt, mud, water, salt_water, snow, ice, calibration_lambertion
            Default: none

        Valid coatings: none, paint, clearcoat, paint_clearcoat

        Valid attributes: none, emissive, retroreflective, single_sided, visually_transparent

        Example:
            # Make a person visible to radar/lidar with skin material
            scene.set_nonvisual_material("/World/person", base="skin")

            # Make a car with aluminum body and paint coating
            scene.set_nonvisual_material("/World/car", base="aluminum", coating="paint")

        :param path: USD path of the root prim to configure.
        :param base: Base material type.
        :param coating: Coating type.
        :param attribute: Material attribute.
        :return: Number of Material prims modified.
        """

        return self._session.query_sim_rpc(
            endpoint="material/set_nonvisual",
            payload={"path": path, "base": base, "coating": coating, "attribute": attribute},
            response_type=int,
        )

    def _step_physics(self, dt_us: int) -> None:
        """
        Step physics by dt_us.

        :param dt_us: Amount of time to step in microseconds.
        """

        if dt_us > 0:
            self._session.query_sim_rpc(
                endpoint="step",
                payload={"dt_us": dt_us},
            )
