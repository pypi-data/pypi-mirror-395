import folium
import math
import networkx as nx
import pandas as pd
from datetime import datetime
from folium.plugins import AntPath, PolyLineTextPath
from geopy.distance import geodesic
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Tuple


class RouteMapPlotterSettings(BaseModel):
    """Configuration for the RouteMapPlotter."""
    use_antpath: bool = Field(True)
    zoom_start: int = Field(14)
    forward_color: str = Field("blue")
    return_color: str = Field("red")
    return_offset_m: float = Field(2.5)
    antpath_delay: int = Field(800)
    antpath_weight: int = Field(5)
    antpath_dash_array: List[int] = Field(default=[10, 20])
    antpath_pulse_color: str = Field("white")
    marker_origin_color: str = Field("green")
    marker_end_color: str = Field("red")
    furthest_marker_color: str = Field("orange")
    arrow_color: str = Field("black")
    marker_radius: int = Field(6)
    default_tile: str = Field("OpenStreetMap")
    arrow_spacing: int = Field(75)
    date_field: str = Field("date_time")
    action_field: str = Field("action")
    colour_field: str = Field("color")
    icon_field: str = Field("icon")
    shape_field: str = Field("shape")
    tooltip_field: str = Field("tooltip")
    lat_col: str = Field("latitude")
    lon_col: str = Field("longitude")


class RouteDataPoint(BaseModel):
    latitude: float
    longitude: float
    date_time: datetime
    origin_node: int
    dest_node: int
    path_nodes: List[int]
    action: Optional[str] = None


class RouteMapPlotter:
    """
    Plots GPS routes and events using Folium, leveraging per-action styling
    (folium_color, folium_icon, folium_shape) if provided by the DataFrame.
    """

    def __init__(self, graph: nx.Graph, settings: Optional[RouteMapPlotterSettings] = None):
        if not isinstance(graph, nx.Graph) or not graph.nodes:
            raise ValueError("A valid NetworkX graph with nodes is required.")
        self.graph = graph
        self.settings = settings or RouteMapPlotterSettings()
        self.tile_layers = {
            "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        }

    # ---------- HELPER METHODS ----------

    def _compute_distance_time_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy().sort_values(self.settings.date_field).reset_index(drop=True)
        df[self.settings.date_field] = pd.to_datetime(df[self.settings.date_field])
        df["prev_lat"] = df[self.settings.lat_col].shift(1)
        df["prev_lon"] = df[self.settings.lon_col].shift(1)
        df["prev_time"] = df[self.settings.date_field].shift(1)

        valid_points = df["prev_lat"].notna()
        df.loc[valid_points, "distance_to_prev"] = df[valid_points].apply(
            lambda r: geodesic((r["prev_lat"], r["prev_lon"]),
                               (r["latitude"], r["longitude"])).meters, axis=1
        )
        df["time_elapsed"] = df[self.settings.date_field] - df["prev_time"]
        df["cumulative_time"] = df["time_elapsed"].cumsum()
        df.fillna({"distance_to_prev": 0.0, "time_elapsed": pd.Timedelta(0)}, inplace=True)
        return df.drop(columns=["prev_lat", "prev_lon", "prev_time"])

    def _format_timedelta(self, td: pd.Timedelta) -> str:
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _get_midpoint(self, df: pd.DataFrame) -> Tuple[float, float]:
        all_nodes = [node for path in df["path_nodes"] if path for node in path]
        if not all_nodes:
            return (df[self.settings.lat_col].mean(), df[self.settings.lon_col].mean())
        avg_lat = sum(self.graph.nodes[n]["y"] for n in all_nodes) / len(all_nodes)
        avg_lon = sum(self.graph.nodes[n]["x"] for n in all_nodes) / len(all_nodes)
        return (avg_lat, avg_lon)

    def _offset_coordinates(self, coords: List[Tuple[float, float]], offset_m: float) -> List[Tuple[float, float]]:
        if len(coords) < 2 or offset_m == 0:
            return coords
        offset_coords = []
        for i, (lat, lon) in enumerate(coords):
            if i == 0:
                p_prev, p_next = coords[i], coords[i + 1]
            elif i == len(coords) - 1:
                p_prev, p_next = coords[i - 1], coords[i]
            else:
                p_prev, p_next = coords[i - 1], coords[i + 1]
            normal_angle = math.atan2(p_next[0] - p_prev[0], p_next[1] - p_prev[1]) + math.pi / 2
            offset_lat = offset_m / 111111
            offset_lon = offset_m / (111111 * math.cos(math.radians(lat)))
            new_lat = lat + offset_lat * math.sin(normal_angle)
            new_lon = lon + offset_lon * math.cos(normal_angle)
            offset_coords.append((new_lat, new_lon))
        return offset_coords

    def _find_furthest_point(self, df: pd.DataFrame) -> Tuple[Optional[int], Optional[int], Optional[pd.Series]]:
        if df["origin_node"].isnull().all():
            return None, None, None
        start_node = df["origin_node"].iloc[0]
        start_lat, start_lon = self.graph.nodes[start_node]["y"], self.graph.nodes[start_node]["x"]
        max_dist, furthest_node, furthest_idx, furthest_row = -1, None, None, None
        for idx, row in df.iterrows():
            if not row["path_nodes"]:
                continue
            for n in row["path_nodes"]:
                lat, lon = self.graph.nodes[n]["y"], self.graph.nodes[n]["x"]
                dist = geodesic((start_lat, start_lon), (lat, lon)).meters
                if dist > max_dist:
                    max_dist, furthest_node, furthest_idx, furthest_row = dist, n, idx, row
        return furthest_node, furthest_idx, furthest_row

    def _plot_path(self, m: folium.Map, coords: List[Tuple[float, float]], color: str):
        if self.settings.use_antpath:
            AntPath(
                locations=coords,
                color=color,
                weight=self.settings.antpath_weight,
                delay=self.settings.antpath_delay,
                dash_array=self.settings.antpath_dash_array,
                pulse_color=self.settings.antpath_pulse_color,
                opacity=0.8,
            ).add_to(m)
        else:
            polyline = folium.PolyLine(coords, color=color, weight=4, opacity=0.6).add_to(m)
            PolyLineTextPath(
                polyline, "▶", repeat=True, offset=8, spacing=self.settings.arrow_spacing,
                attributes={"fill": self.settings.arrow_color, "font-weight": "bold"}
            ).add_to(m)

    def _add_flag_marker(self, m: folium.Map, lat: float, lon: float, color: str, tooltip: str):
        icon = folium.Icon(color=color, icon="flag", prefix="fa")
        folium.Marker(location=(lat, lon), icon=icon, tooltip=tooltip).add_to(m)

    # ---------- DYNAMIC POINT MARKER SUPPORT ----------

    def _add_point_markers(self, m: folium.Map, df: pd.DataFrame):
        """
        Adds dynamic point markers using DataFrame columns:
        folium_color, folium_icon, folium_shape, tooltip, action.

        Also labels each FeatureGroup with the action name and its record count.
        """
        # Compute action counts
        action_counts = (
            df[self.settings.action_field]
            .fillna("Unknown")
            .value_counts()
            .to_dict()
        )

        # Create a feature group per action, including the count in the layer name
        action_groups = {
            action: folium.FeatureGroup(name=f"{action} ({count})")
            for action, count in action_counts.items()
        }
        action_groups["Other"] = folium.FeatureGroup(name="Other (0)")

        # Iterate and render points
        for _, row in df.iterrows():
            action = row.get(self.settings.action_field, "Unknown")
            color = row.get(self.settings.colour_field, "gray")
            icon_name = row.get(self.settings.icon_field, "circle")
            shape = row.get(self.settings.shape_field, "circle")
            tooltip = row.get(self.settings.tooltip_field, "")

            lat, lon = row[self.settings.lat_col], row[self.settings.lon_col]
            target_layer = action_groups.get(action, action_groups["Other"])

            # Marker style dispatch
            if shape == "circle":
                folium.CircleMarker(
                    location=(lat, lon),
                    radius=self.settings.marker_radius,
                    color=color,
                    fill=True,
                    fill_opacity=0.9,
                    tooltip=tooltip,
                ).add_to(target_layer)

            elif shape == "square":
                folium.RegularPolygonMarker(
                    location=(lat, lon),
                    number_of_sides=4,
                    radius=self.settings.marker_radius,
                    color=color,
                    fill=True,
                    fill_opacity=0.9,
                    tooltip=tooltip,
                ).add_to(target_layer)

            elif shape == "triangle":
                folium.RegularPolygonMarker(
                    location=(lat, lon),
                    number_of_sides=3,
                    radius=self.settings.marker_radius + 1,
                    color=color,
                    fill=True,
                    fill_opacity=0.9,
                    tooltip=tooltip,
                ).add_to(target_layer)

            elif shape == "diamond":
                folium.RegularPolygonMarker(
                    location=(lat, lon),
                    number_of_sides=4,
                    radius=self.settings.marker_radius + 1,
                    rotation=45,
                    color=color,
                    fill=True,
                    fill_opacity=0.9,
                    tooltip=tooltip,
                ).add_to(target_layer)

            else:
                folium.Marker(
                    location=(lat, lon),
                    icon=folium.Icon(color=color, icon=icon_name, prefix="fa"),
                    tooltip=tooltip,
                ).add_to(target_layer)

        # Add all layers to the map
        for layer in action_groups.values():
            layer.add_to(m)

    # ---------- MAIN PLOT ----------

    def plot(self, df: pd.DataFrame) -> folium.Map:
        try:
            df_dict = df.iloc[0].to_dict()
            df_dict[self.settings.date_field] = pd.to_datetime(df_dict[self.settings.date_field])
            RouteDataPoint.model_validate(df_dict)
        except Exception as e:
            raise ValueError(f"DataFrame schema validation failed: {e}")

        processed_df = self._compute_distance_time_metrics(df)
        midpoint = self._get_midpoint(processed_df)
        m = folium.Map(location=midpoint, zoom_start=self.settings.zoom_start, tiles=self.settings.default_tile)

        for name, url in self.tile_layers.items():
            if name != self.settings.default_tile:
                folium.TileLayer(tiles=url, name=name, attr=name).add_to(m)

        furthest_node, furthest_idx, furthest_row = self._find_furthest_point(processed_df)
        if furthest_idx is not None:
            for idx, row in processed_df.iterrows():
                if not row["path_nodes"]:
                    continue
                coords = [(self.graph.nodes[n]["y"], self.graph.nodes[n]["x"]) for n in row["path_nodes"]]
                is_forward = idx <= furthest_idx
                color = self.settings.forward_color if is_forward else self.settings.return_color
                coords = coords if is_forward else self._offset_coordinates(coords, self.settings.return_offset_m)
                self._plot_path(m, coords, color)

        start_node = processed_df["origin_node"].iloc[0]
        self._add_flag_marker(m, self.graph.nodes[start_node]["y"], self.graph.nodes[start_node]["x"],
                              self.settings.marker_origin_color, "Start")

        end_node = processed_df["dest_node"].iloc[-1]
        self._add_flag_marker(m, self.graph.nodes[end_node]["y"], self.graph.nodes[end_node]["x"],
                              self.settings.marker_end_color, "End")

        if furthest_node:
            self._add_flag_marker(m, self.graph.nodes[furthest_node]["y"], self.graph.nodes[furthest_node]["x"],
                                  self.settings.furthest_marker_color, "Furthest Point")

        self._add_point_markers(m, processed_df)
        folium.LayerControl(collapsed=False).add_to(m)
        return m