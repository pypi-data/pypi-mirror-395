"""Building model construction and simulation orchestration utilities.

.. module:: batem.core.building

This module provides the high-level orchestration logic required to build a
BATEM building model from contextual data, generate thermal networks, configure
HVAC controllers, and run coupled simulations. It binds together solar,
thermal, control, and model-making subsystems to offer a cohesive workflow.

The dataclasses defined here use reStructuredText field lists so that automated
documentation can surface every parameter accepted by the simulation pipeline.

:Author: stephane.ploix@grenoble-inp.fr
:License: GNU General Public License v3.0
"""
from abc import ABC, abstractmethod
from datetime import datetime
from batem.core.data import DataProvider, Bindings
from batem.core.control import HeatingPeriod, CoolingPeriod, OccupancyProfile, SignalGenerator, TemperatureController, Simulation, TemperatureSetpointPort, HVACcontinuousModePort, LongAbsencePeriod
from batem.core.model import ModelMaker
from batem.core.components import Side
from batem.core.library import SIDE_TYPES, SLOPES
from batem.core.solar import SolarModel, SolarSystem, Collector, SideMask, Mask
from batem.core.statemodel import StateModel
from pyvista.core.pointset import PolyData
from dataclasses import dataclass, field
from pyvista.plotting.plotter import Plotter
from math import sqrt, sin, cos, radians, atan2, degrees, isnan
import pyvista as pv
import matplotlib.pyplot as plt
import numpy as np
import types
pv.set_jupyter_backend('html')


@dataclass
class WindowData:
    side: str
    surface: float
    rotation_angle_deg: float


@dataclass
class FloorData:
    length: float
    width: float
    elevation: float
    windows_data: list[WindowData]


@dataclass
class SideMaskData:
    x_center: float
    y_center: float
    width: float
    height: float
    elevation: float
    exposure_deg: float
    slope_deg: float
    normal_rotation_angle_deg: float


@dataclass
class ContextData:
    """Metadata describing the geographic and climatic context for a simulation.

    :param latitude_north_deg: Site latitude in decimal degrees (positive north).
    :param longitude_east_deg: Site longitude in decimal degrees (positive east).
    :param starting_stringdate: Inclusive start date for the simulation window.
    :param ending_stringdate: Exclusive end date for the simulation window.
    :param location: Human-readable site name used in reports.
    :param albedo: Ground albedo coefficient in the ``[0, 1]`` range.
    :param pollution: Atmospheric pollution factor used for solar attenuation.
    :param number_of_levels: Number of distinct vertical atmospheric layers to
        load in the weather data set.
    :param ground_temperature: Average ground temperature in degrees Celsius.
    :param side_masks: Optional list of distant masks describing surrounding
        obstacles.
    :ivar side_masks: Always stored as a list for downstream iteration.
    """
    latitude_north_deg: float
    longitude_east_deg: float
    starting_stringdate: str
    ending_stringdate: str
    location: str
    albedo: float
    pollution: float
    number_of_levels: int
    ground_temperature: float
    side_masks: list[SideMaskData] = field(default_factory=list)


@dataclass
class BuildingData:
    """Physical and operational parameters defining a BATEM building model.

    This dataclass stores the geometry, material compositions, HVAC capacities,
    and occupant-related assumptions used when generating thermal networks and
    control systems.

    :param length: Building length along the X-axis in metres.
    :param width: Building width along the Y-axis in metres.
    :param n_floors: Number of occupied floors (excluding the basement zone).
    :param floor_height: Storey height in metres for regular floors.
    :param base_elevation: Basement height in metres.
    :param z_rotation_angle_deg: Clockwise rotation of the building footprint.
    :param glazing_ratio: Ratio of window surface to façade surface for each
        orientation.
    :param glazing_solar_factor: Solar heat gain coefficient applied to glazing.
    :param compositions: Mapping of envelope component names to layer tuples
        ``(material_name, thickness_m)``.
    :param max_heating_power: Maximum heating power available per zone in watts.
    :param max_cooling_power: Maximum cooling power available per zone in watts.
    :param occupant_consumption: Latent/convective gains per occupant in watts.
    :param body_PCO2: CO₂ production per occupant in litres per hour.
    :param density_occupants_per_100m2: Occupant density used for gain profiles.
    :param regular_air_renewal_rate_vol_per_hour: Baseline ventilation rate used
        for nominal operation (volumes per hour).
    :param super_air_renewal_rate_vol_per_hour: Ventilation rate applied during
        forced ventilation or free-cooling strategies (volumes per hour).
    :param initial_temperature: Initial temperature (°C) for all thermal states.
    :param low_heating_setpoint: Setback heating setpoint in degrees Celsius.
    :param normal_heating_setpoint: Comfort heating setpoint in degrees Celsius.
    :param high_heating_setpoint: Boost heating setpoint in degrees Celsius.
    :param state_model_order_max: Optional upper bound for model reduction.
    :param periodic_depth_seconds: Maximum penetration depth for periodic inputs.
    :param combinations: dictionary with keys 'wall', 'intermediate_floor', 'roof', 'glazing', 'ground_floor', 'basement_floor' and values are lists of tuples of materials and thicknesses
    :param intermediate_floor: dict[str, tuple[tuple[str, float], ...]]
    """
    length: float
    width: float
    n_floors: int
    floor_height: float
    base_elevation: float
    z_rotation_angle_deg: float
    glazing_ratio: float
    glazing_solar_factor: float
    compositions: dict[str, tuple[tuple[str, float], ...]]
    max_heating_power: float
    max_cooling_power: float
    occupant_consumption: float
    body_PCO2: float
    density_occupants_per_100m2: float
    initial_temperature: float
    low_heating_setpoint: float
    normal_heating_setpoint: float
    normal_cooling_setpoint: float
    regular_air_renewal_rate_vol_per_hour: float
    super_air_renewal_rate_vol_per_hour: float = None  # if not None, window-based free-cooling (air conditioning is disabled) when outdoor temperature is higher than indoor temperature and HVAC setpoint but takes much more computation time be cause of a non-linear system of equations
    long_absence_period: tuple[str, str] = ('1/8', '15/8')
    heating_period: tuple[str, str] = ('1/11', '1/5')
    cooling_period: tuple[str, str] = ('1/6', '30/9')
    state_model_order_max: int | None = None
    periodic_depth_seconds: int = 3600
    wall: Side = field(init=False)
    intermediate_floor: Side = field(init=False)
    roof: Side = field(init=False)
    glazing: Side = field(init=False)
    ground_floor: Side = field(init=False)
    basement_floor: Side = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization method to validate and initialize building components.
        Validates that all required compositions are present and initializes the building components.

        :param self: The instance of the class.
        :raises ValueError: Raised if required compositions are missing.
        """
        required_components: tuple[str, ...] = ('wall', 'intermediate_floor', 'roof', 'glazing', 'ground_floor', 'basement_floor')
        missing_keys: list[str] = [key for key in required_components if key not in self.compositions]
        if missing_keys:
            raise ValueError(f"Missing compositions for: {', '.join(missing_keys)}")

        self.wall = Side(*self.compositions['wall'])
        self.intermediate_floor = Side(*self.compositions['intermediate_floor'])
        self.roof = Side(*self.compositions['roof'])
        self.glazing = Side(*self.compositions['glazing'])
        self.ground_floor = Side(*self.compositions['ground_floor'])
        self.basement_floor = Side(*self.compositions['basement_floor'])


class FloorZoneView:

    @staticmethod
    def _normalize(angle: float) -> float:
        return (angle + 180) % 360 - 180

    def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float, zmin: float, zmax: float, glazing_ratio: float, rotation_angle_deg: float = 0.0) -> None:
        self.xmin: float = xmin
        self.xmax: float = xmax
        self.ymin: float = ymin
        self.ymax: float = ymax
        self.zmin: float = zmin
        self.zmax: float = zmax
        self._rotation_angle_deg: float = rotation_angle_deg
        self.glazing_ratio: float = glazing_ratio

        floor_length: float = xmax - xmin
        floor_width: float = ymax - ymin
        floor_height: float = zmax - zmin
        self._elevation: float = (zmin + zmax) / 2
        self._north_south_surface: float = floor_length * floor_height
        self._east_west_surface: float = floor_width * floor_height

    @property
    def floor_center(self) -> tuple:
        return (0, 0, (self.zmin + self.zmax) / 2)

    def make(self) -> pv.PolyData:
        main_box: PolyData = pv.Box(bounds=(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax))
        if self.glazing_ratio == 0:
            return main_box
        # Create window holes on each side
        window_boxes: list = []

        floor_length: float = self.xmax - self.xmin
        floor_width: float = self.ymax - self.ymin
        floor_height: float = self.zmax - self.zmin
        elevation: float = (self.zmin + self.zmax) / 2
        window_height: float = (self.zmax - self.zmin) * sqrt(self.glazing_ratio)

        north_south_window_width: float = floor_length * sqrt(self.glazing_ratio)
        east_west_window_width: float = floor_width * sqrt(self.glazing_ratio)
        north_south_window_center_x: float = (self.xmin + self.xmax) / 2
        east_west_window_center_y: float = (self.ymin + self.ymax) / 2

        self._elevation: float = elevation
        self._north_south_surface: float = floor_length * floor_height
        self._east_west_surface: float = floor_width * floor_height

        # Use a large padding so cutter boxes pass fully through the floor
        pad: float = max(floor_length, floor_width, floor_height) * 5.0
        # North and South windows (single passing-through box)
        window_box_ns = pv.Box(bounds=(north_south_window_center_x - north_south_window_width/2, north_south_window_center_x + north_south_window_width/2, self.ymin - pad, self.ymax + pad, elevation - window_height/2, elevation + window_height/2))
        window_boxes.append(window_box_ns)

        # East and West windows (single passing-through box)
        window_box_ew = pv.Box(bounds=(self.xmin - pad, self.xmax + pad, east_west_window_center_y - east_west_window_width/2, east_west_window_center_y + east_west_window_width/2, elevation - window_height/2, elevation + window_height/2))
        window_boxes.append(window_box_ew)
        # Use clip_box with invert=True (faster and more stable than boolean CSG)
        # Define cutter bounds explicitly to avoid passing meshes into VTK CSG
        ns_bounds = (
            north_south_window_center_x - north_south_window_width/2,
            north_south_window_center_x + north_south_window_width/2,
            self.ymin - pad,
            self.ymax + pad,
            elevation - window_height/2,
            elevation + window_height/2,
        )
        ew_bounds: tuple[float, float, float, float, float, float] = (
            self.xmin - pad,
            self.xmax + pad,
            east_west_window_center_y - east_west_window_width/2,
            east_west_window_center_y + east_west_window_width/2,
            elevation - window_height/2,
            elevation + window_height/2,
        )
        try:
            result: PolyData = main_box.clip_box(ns_bounds, invert=True)
            result: PolyData = result.clip_box(ew_bounds, invert=True)
            return result
        except Exception as e:
            print(f"Clipping operation failed: {e}")
            return main_box

    @property
    def elevation(self) -> float:
        return self._elevation

    @property
    def primary_window_surface(self) -> float:
        return self._north_south_surface * sqrt(self.glazing_ratio)

    @property
    def secondary_window_surface(self) -> float:
        return self._east_west_surface * sqrt(self.glazing_ratio)

    @property
    def windows_data(self) -> list[WindowData]:
        return [
            WindowData(side="ref", surface=self.primary_window_surface, rotation_angle_deg=FloorZoneView._normalize(self._rotation_angle_deg)),
            WindowData(side="right", surface=self.secondary_window_surface, rotation_angle_deg=FloorZoneView._normalize(self._rotation_angle_deg+90)),
            WindowData(side="opposite", surface=self.primary_window_surface, rotation_angle_deg=FloorZoneView._normalize(self._rotation_angle_deg+180)),
            WindowData(side="left", surface=self.primary_window_surface, rotation_angle_deg=FloorZoneView._normalize(self._rotation_angle_deg-90)),
        ]


class BuildingView:

    def __init__(self, length=10.0, width=8.0, n_floors=5, floor_height=2.7, base_elevation=0, glazing_ratio=0.4) -> None:
        self._building_data: list[FloorData] = []
        self.rotation_angle_deg: float = None
        self.building_color: str = "lightgray"
        self.base_color: str = "darkgray"
        self.edge_color: str = "black"
        self.length: float = length
        self.width: float = width
        self.n_floors: int = n_floors
        self.floor_height: float = floor_height
        self.base_elevation: float = base_elevation
        self.glazing_ratio: float = glazing_ratio
        self.xmin: float = -length/2
        self.xmax: float = length/2
        self.ymin: float = -width/2
        self.ymax: float = width/2
        self.total_height: float = base_elevation + n_floors * floor_height
        self.center_elevation: float = self.total_height / 2
        self.zmin = 0
        self.zmax: float = self.total_height
        self.z_floors: list[float] = [base_elevation + i * floor_height for i in range(n_floors)] + [self.total_height]
        self.floors: list[FloorZoneView] = [FloorZoneView(xmin=self.xmin, xmax=self.xmax, ymin=self.ymin, ymax=self.ymax, zmin=0, zmax=base_elevation, glazing_ratio=0)]
        self.slabs: list[pv.PolyData] = []
        for i in range(n_floors):
            self.floors.append(FloorZoneView(xmin=self.xmin, xmax=self.xmax, ymin=self.ymin, ymax=self.ymax, zmin=self.z_floors[i], zmax=self.z_floors[i+1], glazing_ratio=glazing_ratio))
            self.slabs.append(pv.Box(bounds=(self.xmin, self.xmax, self.ymin, self.ymax, self.z_floors[i], self.z_floors[i]+self.total_height/20)))

    def make(self, rotation_angle_deg: float = 0) -> list[FloorData]:
        # rotation_angle_deg follows convention: 0°=South, 90°=East, -90°=West, 180°=North
        self.rotation_angle_deg = rotation_angle_deg
        building_data: list[FloorData] = []
        for floor in self.floors:
            floor._rotation_angle_deg = rotation_angle_deg
            windows_data: list[WindowData] = []
            for window in floor.windows_data:
                windows_data.append(WindowData(side=window.side, surface=window.surface, rotation_angle_deg=window.rotation_angle_deg))
                # floor_data.windows_data.append(window_data)
            floor_data: FloorData = FloorData(length=self.length, width=self.width, elevation=floor.elevation, windows_data=floor.windows_data)
            building_data.append(floor_data)
        self._building_data = building_data
        return self._building_data

    def draw(self, plotter: pv.Plotter) -> None:
        if self.rotation_angle_deg is None:
            self.rotation_angle_deg = 0.0

        base_box: PolyData = self.floors[0].make().rotate_z(self.rotation_angle_deg, inplace=False)
        # Upper floors have windows
        upper_boxes: list[PolyData] = []
        for floor in self.floors[1:]:
            floor._rotation_angle_deg = self.rotation_angle_deg
            upper_boxes.append(floor.make().rotate_z(self.rotation_angle_deg, inplace=False))

        merged_upper: PolyData | None = None
        if upper_boxes:
            merged_upper = upper_boxes[0].copy()
            for ub in upper_boxes[1:]:
                merged_upper = merged_upper.merge(ub)

        # Slabs
        slab_boxes: list[PolyData] = [slab.rotate_z(self.rotation_angle_deg, inplace=False) for slab in self.slabs]

        for slab in slab_boxes:  # type: ignore[index]
            plotter.add_mesh(slab, color=self.building_color, opacity=0.2, show_edges=False)
        plotter.add_mesh(base_box, color=self.base_color, smooth_shading=True, metallic=0.1, roughness=0.6, show_edges=True, edge_color="black", line_width=1.5)  # type: ignore[arg-type]
        if merged_upper is not None:
            plotter.add_mesh(merged_upper, color=self.building_color, smooth_shading=True, metallic=0.1, roughness=0.6, show_edges=True, edge_color=self.edge_color, line_width=1.5)  # type: ignore[arg-type]

        building_data: list[FloorData] = []
        for floor in self.floors:
            windows_data: list[WindowData] = []
            for window in floor.windows_data:
                windows_data.append(WindowData(side=window.side, surface=window.surface, rotation_angle_deg=window.rotation_angle_deg))
            floor_data: FloorData = FloorData(length=self.length, width=self.width, elevation=floor.elevation, windows_data=floor.windows_data)
            building_data.append(floor_data)
        self._building_data = building_data

    @property
    def building_data(self) -> list[FloorData]:
        return self._building_data


class SideMaskView:

    def __init__(self, side_mask_data: SideMaskData) -> None:
        self.color: str = "red"
        self.opacity: float = 0.35
        # World coordinates: +X=South, +Y=East (as requested)
        self.x_center: float = side_mask_data.x_center
        self.y_center: float = side_mask_data.y_center
        self.z_center: float = side_mask_data.elevation + side_mask_data.height / 2
        self.center_ref: tuple[float, float, float] = (side_mask_data.x_center, side_mask_data.y_center, self.z_center)
        self.width: float = side_mask_data.width
        self.height: float = side_mask_data.height
        self.elevation: float = side_mask_data.elevation
        self.exposure_deg: float = side_mask_data.exposure_deg
        self.slope_deg: float = side_mask_data.slope_deg
        self.normal_rotation_deg: float = side_mask_data.normal_rotation_angle_deg

        self.azimuth_deg: float = degrees(atan2(self.y_center, self.x_center))
        self.altitude_deg: float = degrees(atan2(self.elevation, sqrt(self.x_center**2 + self.y_center**2)))
        self.distance_m: float = sqrt(self.x_center**2 + self.y_center**2)

        slope_rad: float = radians(self.slope_deg)
        # Convention: +X is South, +Y is East; 0°=South(+X), 90°=East(+Y), -90°=West(-Y), 180°=North(-X)
        exposure_rad: float = radians(side_mask_data.exposure_deg)

        # Normal mapping in world XY directly: (cos(theta), sin(theta))
        nx: float = cos(exposure_rad) * sin(slope_rad)
        ny: float = sin(exposure_rad) * sin(slope_rad)
        nz: float = -cos(slope_rad)
        self.normal: tuple[float, float, float] = (nx, ny, nz)

    def make(self) -> SideMaskData:
        return SideMaskData(x_center=self.x_center, y_center=self.y_center, width=self.width, height=self.height, elevation=self.elevation, exposure_deg=self.exposure_deg, slope_deg=self.slope_deg, normal_rotation_angle_deg=self.normal_rotation_deg)

    def draw(self, plotter: pv.Plotter) -> None:
        plane: pv.Plane = pv.Plane(center=self.center_ref, direction=self.normal, i_size=self.height, j_size=self.width)
        if abs(self.normal_rotation_deg) > 1e-9:
            plane.rotate_vector(vector=self.normal, angle=self.normal_rotation_deg, point=self.center_ref, inplace=True)
        tail: list[float] = self.center_ref
        head: list[float] = (self.center_ref[0] + 3.0 * self.normal[0], self.center_ref[1] + 3.0 * self.normal[1], self.center_ref[2] + 3.0 * self.normal[2])
        arrow: pv.Arrow = pv.Arrow(start=tail, direction=[head[i] - tail[i] for i in range(3)], tip_length=0.2, tip_radius=0.15, shaft_radius=0.05)

        plotter.add_mesh(plane, color=self.color, opacity=self.opacity, smooth_shading=True)
        plotter.add_mesh(arrow, color="black")


class Context:

    def __init__(self, context_data: ContextData) -> None:
        self.context_data: ContextData = context_data
        self.distant_masks: list[SideMask] = list()
        self.side_mask_views: list[SideMaskView] = list()
        for side_mask in context_data.side_masks:
            self.distant_masks.append(SideMask(side_mask.x_center, side_mask.y_center, side_mask.width, side_mask.height, side_mask.exposure_deg, side_mask.slope_deg, side_mask.elevation, side_mask.normal_rotation_angle_deg))
            side_mask_view: SideMaskView = SideMaskView(side_mask)
            side_mask_view.make()
            self.side_mask_views.append(side_mask_view)

        bindings: Bindings = Bindings()
        bindings('TZ:outdoor', 'weather_temperature')

        self.dp: DataProvider = DataProvider(location=context_data.location, latitude_north_deg=context_data.latitude_north_deg, longitude_east_deg=context_data.longitude_east_deg, starting_stringdate=context_data.starting_stringdate, ending_stringdate=context_data.ending_stringdate, bindings=bindings, albedo=context_data.albedo, pollution=context_data.pollution, number_of_levels=context_data.number_of_levels)
        self.solar_model: SolarModel = SolarModel(self.dp.weather_data, distant_masks=self.distant_masks)


class Zone(ABC):

    def __init__(self, floor_number: int, building_data: BuildingData, solar_model: SolarModel) -> None:
        self.floor_number: int = floor_number
        self.name: str = f"floor{floor_number}"
        self.length: float = building_data.length
        self.width: float = building_data.width
        self.floor_height: float = building_data.floor_height
        self.floor_surface: float = self.length * self.width
        self.base_elevation: float = building_data.base_elevation
        self.glazing_ratio: float = building_data.glazing_ratio
        self.z_rotation_angle_deg: float = building_data.z_rotation_angle_deg
        self.building_data: BuildingData = building_data
        self.solar_model: SolarModel = solar_model
        self.solar_system: SolarSystem = SolarSystem(solar_model)
        self.n_floors: int = building_data.n_floors

    @abstractmethod
    def make(self, model_maker: ModelMaker, dp: DataProvider) -> None:
        pass

    @abstractmethod
    def window_masks(self) -> dict[str, Mask]:
        """Return window masks dictionary."""
        pass


class BasementZone(Zone):

    def __init__(self, floor_number: int, building_data: BuildingData, solar_model: SolarModel) -> None:
        super().__init__(floor_number, building_data, solar_model)
        self.volume: float = self.length * self.width * self.base_elevation
        self.mid_elevation: float = self.building_data.base_elevation/2
        self.wall_surface: float = 2 * (self.length + self.width) * self.base_elevation

    def window_masks(self) -> dict[str, Mask]:
        return dict()

    def make(self, model_maker: ModelMaker, dp: DataProvider) -> None:
        model_maker.make_side(self.building_data.basement_floor(self.name, 'ground', SIDE_TYPES.FLOOR, self.floor_surface))
        model_maker.make_side(self.building_data.wall(self.name, 'outdoor', SIDE_TYPES.WALL, self.wall_surface))
        model_maker.make_side(self.building_data.ground_floor(self.name, 'floor1', SIDE_TYPES.FLOOR, self.floor_surface))


class RegularZone(Zone):

    def __init__(self, floor_number: int, building_data: BuildingData, solar_model: SolarModel) -> None:
        super().__init__(floor_number, building_data, solar_model)
        self.volume: float = self.length * self.width * self.floor_height
        self.mid_elevation: float = self.base_elevation + self.floor_height * (floor_number - 1 / 2)
        self.glazing_surface: float = self.glazing_ratio * self.length * self.floor_height
        self.wall_surface: float = 2 * (self.length + self.width) * self.floor_height - self.glazing_surface
        self.window_angles_deg: list[float] = [self.z_rotation_angle_deg, 90+self.z_rotation_angle_deg, 180+self.z_rotation_angle_deg, -90+self.z_rotation_angle_deg]
        self.window_surfaces: list[float] = [self.glazing_ratio * self.length * self.floor_height, self.glazing_ratio * self.width * self.floor_height, self.glazing_ratio * self.length * self.floor_height, self.glazing_ratio * self.width * self.floor_height]
        self._window_masks: dict[str, Mask] = dict()
        self.zone_window_collectors: list[Collector] = []
        self.windows_names: list[str] = ['ref', 'right', 'opposite', 'left']

    def window_masks(self) -> dict[str, Mask]:
        return self._window_masks

    def make(self, model_maker: ModelMaker, dp: DataProvider) -> None:
        # n_floors is the number of regular floors, so the top floor number equals n_floors
        if self.floor_number == self.n_floors:
            model_maker.make_side(self.building_data.roof(self.name, 'outdoor', SIDE_TYPES.CEILING, self.volume))
        else:
            model_maker.make_side(self.building_data.intermediate_floor(self.name, f'floor{self.floor_number+1}', SIDE_TYPES.FLOOR, self.floor_surface))
        model_maker.make_side(self.building_data.wall(self.name, 'outdoor', SIDE_TYPES.WALL, self.wall_surface))
        model_maker.make_side(self.building_data.glazing(self.name, 'outdoor', SIDE_TYPES.GLAZING, self.glazing_surface))
        regular_rate = self.building_data.regular_air_renewal_rate_vol_per_hour
        super_rate = self.building_data.super_air_renewal_rate_vol_per_hour
        if regular_rate is not None:
            nominal_airflow = regular_rate * self.volume / 3600
        elif super_rate is not None:
            nominal_airflow = super_rate * self.volume / 3600
        else:
            nominal_airflow = 0.0
        model_maker.connect_airflow(self.name, 'outdoor', nominal_value=nominal_airflow)

        for window_name, window_angle, window_surface in zip(self.windows_names, self.window_angles_deg, self.window_surfaces):
            window_collector: Collector = Collector(self.solar_system, f'{window_name}', surface_m2=window_surface, exposure_deg=window_angle, slope_deg=SLOPES.VERTICAL.value, solar_factor=self.building_data.glazing_solar_factor, observer_elevation_m=self.mid_elevation)
            self.zone_window_collectors.append(window_collector)
            self._window_masks[window_name] = window_collector.mask


class Building:
    """High-level orchestrator for generating and simulating a BATEM building.

    The class assembles the context, solar model, thermal network, HVAC
    controllers, and simulation engine required to execute a full-year building
    simulation.

    :param context_data: Geographic and climatic context description.
    :param building_data: Physical parameters and HVAC capacities.
    :ivar context: Instantiated :class:`Context` wrapping weather and bindings.
    :ivar dp: Shared :class:`~batem.core.data.DataProvider` used across modules.
    :ivar simulation: Configured :class:`~batem.core.control.Simulation` object.
    :ivar floors: List of :class:`Zone` instances representing each building
        level.
    """

    def __init__(self, context_data: ContextData, building_data: BuildingData) -> None:
        self.context: Context = Context(context_data)
        self.context_data: ContextData = context_data
        self.dp: DataProvider = self.context.dp
        self.building_data: BuildingData = building_data
        self.building_view: BuildingView = BuildingView(length=building_data.length, width=building_data.width, n_floors=building_data.n_floors, floor_height=building_data.floor_height, base_elevation=building_data.base_elevation, glazing_ratio=building_data.glazing_ratio)
        self.building_view.make(rotation_angle_deg=building_data.z_rotation_angle_deg)
        self.dp.add_param('CCO2:outdoor', 400)
        self.dp.add_param('TZ:ground', context_data.ground_temperature)

        solar_model: SolarModel = self.context.solar_model

        floors: list[Zone] = [BasementZone(0, building_data, solar_model)]
        zone_name_volumes: dict[str, float] = {floors[0].name: floors[0].volume}
        # n_floors represents the number of regular floors (excluding basement)
        # So we create floors 1 through n_floors
        for floor_number in range(1, building_data.n_floors + 1):
            floors.append(RegularZone(floor_number, building_data, solar_model))
            zone_name_volumes[floors[floor_number].name] = floors[floor_number].volume
        zone_name_volumes['outdoor'] = None
        zone_name_volumes['ground'] = None
        self.zone_names: list[str] = [floor.name for floor in floors]
        self.floors: list[Zone] = floors
        self._zone_outdoor_regular_airflows: dict[str, float] = {}
        self._zone_outdoor_super_airflows: dict[str, float] = {}
        airflow_defaults: dict[str, float] = {}
        airflow_bounds: dict[str, float] = {}
        airflow_names: list[str] = []
        for floor in floors:
            volume: float | None = getattr(floor, 'volume', None)
            if volume is None:
                continue
            airflow_name = f'Q:{floor.name}-outdoor'
            base_value: float | None = None
            bound_upper: float = 0.0
            if self.building_data.regular_air_renewal_rate_vol_per_hour is not None:
                regular_airflow: float = (self.building_data.regular_air_renewal_rate_vol_per_hour * volume) / 3600.0
                self._zone_outdoor_regular_airflows[floor.name] = regular_airflow
                base_value = regular_airflow
                bound_upper = max(bound_upper, regular_airflow)
            if self.building_data.super_air_renewal_rate_vol_per_hour is not None:
                super_airflow: float = (self.building_data.super_air_renewal_rate_vol_per_hour * volume) / 3600.0
                self._zone_outdoor_super_airflows[floor.name] = super_airflow
                if base_value is None:
                    base_value = super_airflow
                bound_upper = max(bound_upper, super_airflow)
            if base_value is None:
                base_value = 0.0
            bound_upper = max(bound_upper, base_value)
            airflow_defaults[airflow_name] = base_value
            airflow_bounds[airflow_name] = bound_upper
            airflow_names.append(airflow_name)
        if airflow_names:
            self.dp.add_data_names_in_fingerprint(*airflow_names)
            for airflow_name, default_value in airflow_defaults.items():
                values = [default_value for _ in self.dp.ks]
                if airflow_name in self.dp:
                    self.dp.add_var(airflow_name, values, force=True)
                else:
                    self.dp.add_var(airflow_name, values)
                bound_upper = airflow_bounds.get(airflow_name, default_value)
                if bound_upper <= 0.0:
                    bound_upper = 1e-6
                if hasattr(self.dp, 'independent_variable_set'):
                    self.dp.independent_variable_set.variable_bounds[airflow_name] = (0.0, bound_upper)

        # #### STATE MODEL MAKER AND SURFACES ####
        model_maker: ModelMaker = ModelMaker(data_provider=self.dp, periodic_depth_seconds=building_data.periodic_depth_seconds, state_model_order_max=building_data.state_model_order_max, **zone_name_volumes)

        max_occupancy: float = building_data.density_occupants_per_100m2 * (building_data.length * building_data.width) / 100

        siggen: SignalGenerator = SignalGenerator(self.dp, OccupancyProfile(weekday_profile={0: max_occupancy, 7: max_occupancy*.95, 8: max_occupancy*.7, 9: max_occupancy*.3, 12: max_occupancy*.5, 17: max_occupancy*.7, 18: max_occupancy*.8, 19: max_occupancy*.9, 20: max_occupancy}, weekend_profile={0: max_occupancy}))
        siggen.add_hvac_period(HeatingPeriod(building_data.heating_period[0], building_data.heating_period[1], weekday_profile={0: building_data.low_heating_setpoint, 7: building_data.normal_heating_setpoint}, weekend_profile={00: building_data.low_heating_setpoint, 7: building_data.normal_heating_setpoint}))
        siggen.add_hvac_period(CoolingPeriod(building_data.cooling_period[0], building_data.cooling_period[1], weekday_profile={0: None, 10: building_data.normal_cooling_setpoint, 18: None}, weekend_profile={0: None, 10: building_data.normal_cooling_setpoint, 18: None}))
        if building_data.long_absence_period is not None:
            siggen.add_long_absence_period(LongAbsencePeriod(building_data.long_absence_period[0], building_data.long_absence_period[1]))
        else:
            siggen.add_long_absence_period(LongAbsencePeriod(building_data.long_absence_period[0], building_data.long_absence_period[1]))
        # Create per-floor signals
        controllers: dict[str, TemperatureController] = {}

        for floor in floors:
            floor.make(model_maker, self.dp)
            # Occupancy profile and HVAC seasons
            if floor.floor_number == 0:
                # Basement: generate signals but no HVAC controller
                siggen.generate(floor.name)
            else:
                # Regular floors: generate signals (SETPOINT, MODE, OCCUPANCY, PRESENCE)
                siggen.generate(floor.name)
                # Get solar gain (returns None if no collectors)
                solar_gain = floor.solar_system.powers_W(gather_collectors=True)
                # Handle case where there are no collectors (solar_gain is None)
                if solar_gain is None:
                    solar_gain = [0.0 for _ in self.dp.ks]
                self.dp.add_var(f'GAIN_SOLAR:{floor.name}', solar_gain)
                # Add solar to gains
                zone_occupancy: list[float | None] = self.dp.series(f'OCCUPANCY:{floor.name}')

                # Handle None values in occupancy (convert None to 0 for gain calculation)
                # OCCUPANCY contains the actual number of occupants (0 to max_occupancy), not a ratio
                occupancy_gain: list[float] = [(building_data.occupant_consumption) * (_ if _ is not None else 0.0) for _ in zone_occupancy]
                self.dp.add_var(f'GAIN_OCCUPANCY:{floor.name}', occupancy_gain)
                self.dp.add_var(f'GAIN:{floor.name}', [occupancy_gain[k] + solar_gain[k] for k in self.dp.ks])
                self.dp.add_var(f'PCO2:{floor.name}', (siggen.filter(zone_occupancy, lambda x: x * building_data.body_PCO2 if x is not None else 0)))

        model_maker.zones_to_simulate({floor.name: floor.volume for floor in floors})
        # Nominal state model - must be created before TemperatureControllers
        model_maker.nominal
        if self.building_data.initial_temperature is not None:
            self._initialize_state_models(model_maker, self.building_data.initial_temperature)

        # Create HVAC controllers after nominal state model is ready
        for floor in floors:
            if floor.floor_number > 0:
                hvac_port: HVACcontinuousModePort = HVACcontinuousModePort(data_provider=self.dp, zone_name=floor.name, max_heating_power=building_data.max_heating_power, max_cooling_power=building_data.max_cooling_power)
                temperature_setpoint_port: TemperatureSetpointPort = TemperatureSetpointPort(data_provider=self.dp, zone_name=floor.name, heating_levels=[16, 19, 20, 21, 22, 23, 24], cooling_levels=[24, 25, 26, 27, 28])
                controllers[floor.name] = TemperatureController(hvac_heat_port=hvac_port, temperature_setpoint_port=temperature_setpoint_port, model_maker=model_maker)

        self.simulation: Simulation = Simulation(model_maker)
        for floor in floors:
            if floor.floor_number > 0:
                self.simulation.add_temperature_controller(zone_name=floor.name, temperature_controller=controllers[floor.name])

    def _initialize_state_models(self, model_maker: ModelMaker, temperature: float) -> None:
        def _set_uniform_initial_state(state_model: StateModel, temp: float) -> StateModel:
            if state_model is None or state_model.n_states == 0:
                return state_model
            target_state: np.ndarray = np.full((state_model.n_states, 1), float(temp))
            state_model.set_state(target_state)
            return state_model

        if hasattr(model_maker, "state_models_cache"):
            model_maker.state_models_cache = {
                key: _set_uniform_initial_state(sm, temperature) for key, sm in model_maker.state_models_cache.items()
            }

        nominal_model: StateModel | None = getattr(model_maker, "nominal_state_model", None)
        if nominal_model is not None:
            _set_uniform_initial_state(nominal_model, temperature)

        original_make_k = model_maker.make_k

        def make_k_with_initial_state(self, *args, **kwargs):
            state_model: StateModel = original_make_k(*args, **kwargs)
            return _set_uniform_initial_state(state_model, temperature)

        model_maker.make_k = types.MethodType(make_k_with_initial_state, model_maker)

    def _cooling_lockout_rule(self, simulation: Simulation, k: int, heater_power: float) -> float:
        """Promote ventilation when cooling mode and free-cooling conditions are met.

        The rule restores the nominal outdoor airflow at the beginning of each timestep,
        then checks whether the HVAC is in cooling mode (``MODE = -1``) and whether
        passive free-cooling criteria are satisfied (occupancy present, zone warmer
        than the set-point, outdoor air sufficiently cool, and window ventilation
        enabled). When the criteria hold the outdoor airflow time series is overwritten
        for both the current index ``k`` and the following index ``k+1`` to ensure the
        state-model fingerprint registers the change. The function finally returns a
        heater power request of ``0`` to maintain cooling lockout.

        :param simulation: Running :class:`~batem.core.control.Simulation` instance.
        :param k: Current time-step index.
        :param heater_power: Heater power that would have been applied without the rule.
        :returns: Either the original ``heater_power`` or ``0.0`` when free-cooling is triggered.
        """
        zone_info: dict[str, callable] | None = getattr(simulation, '_active_zone_info', None)
        if not zone_info:
            return heater_power

        zone_name: str | None = zone_info.get('zone_name')
        if zone_name is None:
            return heater_power

        if hasattr(simulation, 'sim_variable_map'):
            sim_var_map: dict[str, str] = simulation.sim_variable_map
        else:
            sim_var_map = {}
        dp: DataProvider = simulation.dp

        def _set_outdoor_airflow(target_value: float | None) -> None:
            if target_value is None:
                return
            airflow_name = f'Q:{zone_name}-outdoor'
            targets = {airflow_name, sim_var_map.get(airflow_name, airflow_name)}
            for target in targets:
                for index in (k, k + 1 if (k + 1) < len(dp) else None):
                    if index is None:
                        continue
                    try:
                        dp(target, index, target_value)
                    except Exception:
                        continue

        _set_outdoor_airflow(self._zone_outdoor_regular_airflows.get(zone_name))

        def sample(base_name: str, index: int = k):
            var_name: str = sim_var_map.get(base_name, base_name)
            try:
                return dp(var_name, index)
            except Exception:
                return None

        mode_raw = sample(f'MODE:{zone_name}')
        try:
            mode_value = float(mode_raw) if mode_raw is not None else None
        except (TypeError, ValueError):
            mode_value = None

        occupancy_raw = sample(f'OCCUPANCY:{zone_name}')
        try:
            occupancy_value = float(occupancy_raw) if occupancy_raw is not None else 0.0
        except (TypeError, ValueError):
            occupancy_value = 0.0
        if occupancy_value <= 0.0:
            return heater_power

        default_cooling_setpoint: float | None = getattr(self.building_data, 'cooling_lockout_default_setpoint', 24.0)

        def _to_float(value) -> float | None:
            try:
                as_float = float(value)
            except (TypeError, ValueError):
                return None
            return as_float if not isnan(as_float) else None

        setpoint_raw = sample(f'SETPOINT:{zone_name}')
        setpoint_value: float | None = _to_float(setpoint_raw)
        if setpoint_value is None:
            setpoint_value = default_cooling_setpoint
        if setpoint_value is None:
            return heater_power

        outdoor_raw = dp('weather_temperature', k)
        try:
            outdoor_temp = float(outdoor_raw)
        except (TypeError, ValueError):
            outdoor_temp = None
        if outdoor_temp is None:
            return heater_power

        if hasattr(simulation, '_precontrol_output_map'):
            pre_outputs: dict[str, float] = simulation._precontrol_output_map
        else:
            pre_outputs = {}
        tz_value = pre_outputs.get(f'TZ:{zone_name}')
        if tz_value is None:
            tz_value = pre_outputs.get(f'TZ_OP:{zone_name}')
        if tz_value is None:
            return heater_power
        try:
            zone_temp = float(tz_value)
        except (TypeError, ValueError):
            return heater_power

        free_cooling_delta_temp: float = getattr(self.building_data, 'free_cooling_temperature_delta', 1.0)
        free_cooling_margin: float = getattr(self.building_data, 'free_cooling_setpoint_margin', 0.0)
        window_cooling_enabled: bool = self.building_data.super_air_renewal_rate_vol_per_hour is not None

        if not (window_cooling_enabled and mode_value == -1.0):
            return heater_power

        if zone_temp <= setpoint_value:
            return heater_power
        if outdoor_temp > setpoint_value - free_cooling_margin:
            return heater_power
        if (zone_temp - outdoor_temp) < free_cooling_delta_temp:
            return heater_power

        _set_outdoor_airflow(self._zone_outdoor_super_airflows.get(zone_name))
        return 0.0

    def simulate(self, suffix: str = 'sim') -> DataProvider:
        # #### RUN ####
        self.simulation.run(suffix=suffix, control_rule=self._cooling_lockout_rule)

        # #### PRINT/SHOW RESULTS ####
        print(self.simulation)
        print(self.simulation.control_ports)
        return self.dp

    def draw(self, window_size: tuple[int, int] = (1024, 768)) -> None:
        plotter: Plotter = pv.Plotter(window_size=window_size)
        plotter.set_background("white")
        plotter.clear()
        if self.building_view is not None:
            self.building_view.draw(plotter)
        ground: PolyData = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=60, j_size=60)
        plotter.add_mesh(ground, color="#DDDDDD", opacity=1)
        if self.context.side_mask_views is not None:
            for side_mask_view in self.context.side_mask_views:
                side_mask_view.draw(plotter)
        plotter.add_axes(line_width=2)
        plotter.show_bounds(grid="front", location="outer", all_edges=True, xtitle="X (North -> South)", ytitle="Y (West -> East)", ztitle="Z (Up)")
        plotter.enable_eye_dome_lighting()
        plotter.camera_position = [(25, -35, 25), (0, 0, 5), (0, 0, 1)]
        plotter.show(auto_close=False)

    def plot_heliodon(self, floor_number: int) -> plt.Axes:
        """Plot heliodon charts with horizon mask and collector-specific side masks for each floor.

        Generates one heliodon chart per floor showing the complete mask (horizon + distant + collector)
        for the South-facing window, demonstrating how solar access changes with floor elevation.

        :param floor_number: Floor number to plot (1-based index)
        :type floor_number: int (from 0 ground floor to n_floors - 1 to top floor)
        :param year: Year for heliodon plot (defaults to first year in weather data)
        :type collector_name: str (name of the collector to plot)
        :type collector_name: str (name of the collector to plot)
        :type year: int, optional
        """
        # Get year from weather data if not provided

        first_date: datetime = self.dp.weather_data.datetimes[0]
        year: int = first_date.year
        floor: Zone = self.floors[floor_number]
        window_masks_dict: dict[str, Mask] = floor.window_masks()
        if len(window_masks_dict) == 0:
            # Skip floors with no windows (e.g., basement)
            return None
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'Heliodon for {floor.name}, Elevation: {floor.mid_elevation:.1f}m', fontsize=12)
        axes_flat = axes.flatten()  # Flatten 2D array to 1D for easier indexing
        for i, (window_name, window_mask) in enumerate(window_masks_dict.items()):
            if i >= len(axes_flat):
                break  # Safety check: don't exceed available subplots
            self.context.solar_model.plot_heliodon(name=f'Window {window_name}', year=year, observer_elevation_m=floor.mid_elevation, mask=window_mask, axes=axes_flat[i])
            axes_flat[i].set_title(f'Window {window_name}')
            axes_flat[i].set_xlabel('Azimuth in degrees (0° = South, +90° =West)')
        plt.tight_layout()
        return axes
