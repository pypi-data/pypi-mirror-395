"""
Code to display the prod pipelines graph
Heavily inspired by:
https://towardsdatascience.com/visualize-hierarchical-data-using-plotly-and-datapane-7e5abe2686e1
"""

import os
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from itertools import groupby

import networkx as nx
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Helpful Types
EdgeList = tuple[float, float, float, float]


@dataclass
class GraphEdge:
    u: float
    v: float
    data: dict | None = None


@dataclass
class Edge:
    x0: float
    y0: float
    x1: float
    y1: float


@dataclass
class Point:
    x: float
    y: float


class GraphPlot:
    def __init__(self, G: nx.DiGraph, **kwargs):
        # Data
        self.G = deepcopy(G)

        script_location = os.path.dirname(os.path.abspath(__file__))
        self.stages_folder = os.path.abspath(f'{script_location}/stages/')

        # Text and sizes
        self.title = 'Workflow Graph'
        self.title_fontsize = 24
        self.node_text_position = 'top center'
        self.node_text_fontsize = 14
        self.node_size = 5
        self.node_border_weight = 5
        self.arrow_size = self.node_border_weight * 2
        self.edge_weight = 1

        # Layout
        self.partite_key = 'layer'
        self.partite_across_key = 'layer_order'
        self.align = 'horizontal'
        self.layout_scale = 10
        self.show_legend = False
        self.curve = 0.5

        # Colors
        self.colorscale = 'Blugrn'
        self.node_color_key = self.partite_key
        self.grey_color = 'rgba(153, 153, 153, 0.5)'
        self.dark_emphasis_color = '#0c1f27'
        self.arrow_opacity = 0.8

        # Convert any kwargs into attributes
        self.__dict__.update(kwargs)

        # Graph transforms
        # Add name as attribute
        nx.set_node_attributes(self.G, {n: n for n in self.G.nodes}, name='name')

        # Reverse all edges
        self.G = G.reverse()

        # Recalculate the depths using the topological order
        self._recalculate_depth(new_key=self.partite_key)

        # Calculate the depth_order and position
        self._calculate_depth_order(layer_key=self.partite_key, new_key=self.partite_across_key)

    def __add__(self, other) -> go.Figure:
        assert type(self) is type(other)

        fig = make_subplots(rows=1, cols=2, column_titles=[self.title, other.title])

        for trace in self.create_traces():
            fig.add_trace(trace, row=1, col=1)

        for trace in other.create_traces():
            fig.add_trace(trace, row=1, col=2)

        # Set the overall layout using this objects layout
        # Make sure the updates are to both subplot axes
        layout = self._get_layout()
        layout.update(
            annotations=self.get_annotations(xref='x1', yref='y1') + other.get_annotations(xref='x2', yref='y2'),
        )
        fig.update_layout(layout)
        fig.update_layout(title='')
        fig.update_yaxes(layout.yaxis)
        fig.update_xaxes(layout.xaxis)

        return fig

    def _get_layout(self) -> go.Layout:
        return go.Layout(
            title=self.title,
            titlefont_size=self.title_fontsize,
            showlegend=self.show_legend,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleanchor='y'),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, autorange='reversed'),
            coloraxis=dict(reversescale=False),
        )

    def display_graph(self):
        fig = self.create_figure()
        fig.show()

    def create_traces(self) -> list[go.Scatter]:
        # Add weight and depth attributes to the nodes
        for node in self.G.nodes:
            self.G.nodes[node]['weight'] = 1

        # Make edge traces
        dark_edge_traces = self._create_edge_traces(self._non_skipped_edge, self.dark_emphasis_color)
        light_edge_traces = self._create_edge_traces(lambda x: not self._non_skipped_edge(x), self.grey_color)

        # Make node trace
        node_trace = self._create_node_trace()

        return [*dark_edge_traces, *light_edge_traces, node_trace]

    def create_figure(self):
        traces = self.create_traces()
        fig = go.FigureWidget(
            data=traces,
            layout=self._get_layout(),
        )
        fig.layout['annotations'] = self.get_annotations()

        return fig

    def _get_node_positions(self):
        positions = map(lambda n: self.G.nodes[n]['pos'], self.G.nodes)
        node_x, node_y = list(map(list, zip(*positions, strict=False)))
        return node_x, node_y

    def _get_edge_positions(self, filter_fun: Callable):
        # Add position info to the edges
        edges: dict[str, list[float | None]] = {'x': [], 'y': []}
        midpoints: dict[str, list[float | None]] = {'x': [], 'y': []}
        edge_names = []
        mid_angles = []  # This will store the perpendicular angles at each midpoint

        for edge in list(filter(filter_fun, self.G.edges())):
            edge = GraphEdge(*edge)
            u = Point(*self.G.nodes[edge.u]['pos'])
            v = Point(*self.G.nodes[edge.v]['pos'])

            # Compute straight edge
            points_x, points_y = self._straight_edge(u, v)

            # Get all the nodes in the graph that aren't n1 and n2 and get their position
            node_positions = np.array(
                [self.G.nodes[n]['pos'] for n in self.G.nodes if n not in set([edge.u, edge.v])],
            )

            # I only want to curve the edge if the straight line passes over a node
            closest_node_distance = self._closest_node_distance(u, v, node_positions)
            self.G.edges[edge.u, edge.v]['closest_node_distance'] = closest_node_distance

            if closest_node_distance < self.node_size:
                # If the straight line passes over a node, compute the curved edge
                points_x, points_y = self._curved_edge(
                    u,
                    v,
                    offset=self.curve,
                    curve_left=self.G.nodes[edge.v]['curve_left'],
                )

            # Add the edge to the list
            edges['x'].extend(list(points_x) + [None])
            edges['y'].extend(list(points_y) + [None])

            # Add hover text at the midpoint
            mid_idx = len(points_x) // 2
            midpoints['x'].append(points_x[mid_idx])  # Curved midpoint X
            midpoints['y'].append(points_y[mid_idx])  # Curved midpoint Y

            # Get the midpoint perpendicular vector angle
            mid_angles.append(self._get_midpoint_angle(points_x, points_y, mid_idx))

            edge_names.append(f'{edge.u} ⮕ {edge.v}')

        return edges['x'], edges['y'], edge_names, midpoints['x'], midpoints['y'], mid_angles

    @staticmethod
    def _get_midpoint_angle(points_x, points_y, mid_idx):
        # Calculate the direction vector at midpoint (tangent to curve)
        direction_vector = np.array(
            [
                points_x[mid_idx + 1] - points_x[mid_idx - 1],
                points_y[mid_idx + 1] - points_y[mid_idx - 1],
            ]
        )
        length = np.linalg.norm(direction_vector)

        # Avoid division by zero
        if length == 0:
            perp_vector = Point(1, 0)  # Default perpendicular vector if no direction
        else:
            direction_vector /= length
            # Perpendicular vector: Rotate 90 degrees (counter-clockwise)
            perp_vector = Point(-direction_vector[1], direction_vector[0])

        # Calculate the angle of the perpendicular vector (in degrees)
        angle = np.arctan2(perp_vector.y, perp_vector.x) * (180 / np.pi)

        # Normalize the angle to be within 0 to 360 degrees
        if angle < 0:
            angle += 360  # Adjust to make angles positive

        return angle

    @staticmethod
    def _closest_node_distance(p1: Point, p2: Point, node_positions):
        """
        Computes the shortest distance from the line defined by points (p1.x, p1.y) to (p2.x, p2.y)
        to the closest node in the node_positions.
        """
        # If there are no node positions, return inf
        if len(node_positions) == 0:
            return np.inf

        # Calculate the direction vector of the line
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        # Calculate the length of the line segment
        length = np.sqrt(dx**2 + dy**2)

        # Normalize the direction vector
        direction_vector = np.array([dx, dy]) / length

        # Vector from the start of the line to each node
        vec_to_nodes = node_positions - np.array([p1.x, p1.y])

        # Project each node onto the direction vector
        projection_length = np.dot(vec_to_nodes, direction_vector)

        # Clamp the projection length to the range [0, length] to stay within the line segment
        projection_length = np.clip(projection_length, 0, length)

        # Calculate the closest point on the line segment to each node
        closest_point = np.outer(projection_length, direction_vector) + np.array([p1.x, p1.y])

        # Calculate the distance from each node to the closest point on the line segment
        distance_to_line = np.linalg.norm(node_positions - closest_point, axis=1)

        # Return the minimum distance to the line for each node
        min_distance = np.min(distance_to_line)

        return min_distance

    def _create_edge_traces(self, filter_fun: Callable, color: str) -> list[go.Scatter]:
        # Begin plotting
        edge_x, edge_y, edge_names, mid_x, mid_y, mid_angles = self._get_edge_positions(filter_fun)

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            mode='lines',
            line=dict(width=self.edge_weight, color=color),
            hoverinfo='none',
            marker=dict(
                color=color,
            ),
        )

        # Add hover text
        # Scatter trace for edge hover text (at midpoints), using perpendicular vectors to orient markers
        edge_hover_trace = go.Scatter(
            x=mid_x,
            y=mid_y,
            mode='markers+text',
            marker=dict(
                size=self.arrow_size,
                symbol='arrow-up',  # This makes the marker an arrow
                color=color,
                angle=mid_angles,  # Rotate the arrow based on the perpendicular angle
                angleref='up',
            ),
            hovertext=edge_names,  # Hover text
            hoverinfo='text',
            textposition='top center',  # Position text near the marker if visible
        )

        return [edge_trace, edge_hover_trace]

    @staticmethod
    def _straight_edge(p1: Point, p2: Point, num_points=100):
        """
        Computes a straight path for an edge.

        Parameters:
        - x0, y0: Start coordinates of the edge.
        - x1, y1: End coordinates of the edge.
        - num_points: Number of points to define the straight path.

        Returns:
        - Straight coordinates as lists of x and y values.
        """
        # Compute 100 points along the line
        t_values = np.linspace(0, 1, num_points)
        straight_x = (1 - t_values) * p1.x + t_values * p2.x
        straight_y = (1 - t_values) * p1.y + t_values * p2.y

        return np.array([p1.x, *straight_x, p2.x]), np.array([p1.y, *straight_y, p2.y])

    @staticmethod
    def _curved_edge(p1: Point, p2: Point, offset=0.5, num_points=100, curve_left=True):
        """
        Computes a curved path for an edge by introducing a midpoint offset proportional to the edge length.
        The direction of the curve can be controlled with the `curve_up` boolean.

        Parameters:
        - p1.x, p1.y: Start coordinates of the edge.
        - p2.x, p2.y: End coordinates of the edge.
        - offset_multiplier: Multiplier to scale the offset based on edge length.
        - num_points: Number of points to define the curve.
        - curve_up: Boolean to determine if the curve is upward or downw ard.

        Returns:
        - Curved coordinates as lists of x and y values.
        """

        # Compute edge length
        dx, dy = p2.x - p1.x, p2.y - p1.y
        length = np.sqrt(dx**2 + dy**2)
        if length == 0:  # Avoid division by zero
            return [p1.x, p2.x], [p1.y, p2.y]

        # Midpoint of the edge
        mid_x = (p1.x + p2.x) / 2
        mid_y = (p1.y + p2.y) / 2

        # Direction of the edge (unit vector)
        perp_dx = -dy / length
        perp_dy = dx / length

        # Offset proportional to the edge length
        offset = length * offset

        # Adjust offset direction based on curve_up boolean
        if not curve_left:
            perp_dx = -perp_dx
            perp_dy = -perp_dy

        # Compute the control point for the quadratic Bezier curve
        control_x = mid_x + perp_dx * offset
        control_y = mid_y + perp_dy * offset

        # Generate Bezier curve points
        t_values = np.linspace(0, 1, num_points)
        curve_x = (1 - t_values) ** 2 * p1.x + 2 * (1 - t_values) * t_values * control_x + t_values**2 * p2.x
        curve_y = (1 - t_values) ** 2 * p1.y + 2 * (1 - t_values) * t_values * control_y + t_values**2 * p2.y

        # Return the full curved path
        return np.array([p1.x, *curve_x, p2.x]), np.array([p1.y, *curve_y, p2.y])

    def _create_node_trace(self) -> go.Scatter:
        # Now get the node and edge positions
        node_x, node_y = self._get_node_positions()
        max_dim = max(*node_x, *node_y)

        # Get node depths and meta
        node_name, node_hovertext, node_color = self._get_node_data()

        layer_min, layer_max = self._get_layer_range()
        marker = dict(
            showscale=True,
            colorscale=self.colorscale,
            reversescale=False,
            color=[],
            opacity=1,
            size=[self.node_size] * len(node_x),
            sizeref=1.0 * max_dim / 100.0,
            line=dict(color=self._get_border_colors(), width=self.node_border_weight),
            colorbar=dict(
                thickness=15,
                title='Workflow Depth',
                xanchor='left',
                titleside='right',
                tickmode='array',
                tickvals=list(range(-layer_min, -layer_max - 1, -1)),
                ticktext=list(range(layer_min, layer_max + 1, 1)),
            ),
        )

        # Create the node trace
        marker['color'] = node_color
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            textposition=self.node_text_position,
            textfont_size=self.node_text_fontsize,
            hoverinfo='text',
            marker=marker,
            text=node_name,
            hovertext=node_hovertext,
        )

        return node_trace

    def _get_node_data(self):
        node_color = list(
            map(
                lambda n: self._get_node_color(n[0], -n[1][self.node_color_key])[0],
                self.G.nodes.items(),
            ),
        )
        node_name = [n for n in self.G.nodes]

        def special_labels(n):
            _, label = self._get_node_color(n)
            return label + '<br>' if label else ''

        node_hovertext = list(
            map(
                lambda n: (
                    special_labels(n[0]) + 'Stage: ' + str(n[0]) + '<br>' + 'Stage Order: ' + str(n[1].get('order', ''))
                ),
                self.G.nodes.items(),
            ),
        )
        return node_name, node_hovertext, node_color

    def _get_node_color(self, n: str, default: str | int | None = None):
        if self.G.nodes[n]['skip_stages']:
            return '#5A5A5A', 'Skip stage'
        elif self.G.nodes[n]['only_stages']:
            return '#5053f8', 'Only run this stage'
        elif self.G.nodes[n]['first_stages']:
            return '#28A745', 'First stage'
        elif self.G.nodes[n]['last_stages']:
            return '#e93e2e', 'Last stage'
        elif self.G.nodes[n]['skipped']:
            return self.grey_color, 'Skipped'
        else:
            return default, None

    def _get_border_color(self, n: str):
        if self.G.nodes[n]['skipped']:
            return self.grey_color
        else:
            return self.dark_emphasis_color

    def _non_skipped_edge(self, edge) -> bool:
        return not self.G.nodes[edge[0]]['skipped'] and not self.G.nodes[edge[1]]['skipped']

    def _non_skipped_node(self, node: str) -> bool:
        return not self.G.nodes[node]['skipped']

    def _get_edge_color(self, edge):
        return self.dark_emphasis_color if self._non_skipped_edge(edge) else self.grey_color

    def _get_node_colors(self):
        return [self._get_node_color(n)[0] for n in self.G.nodes]

    def _get_border_colors(self):
        return [self._get_border_color(n) for n in self.G.nodes]

    def _get_edge_colors(self):
        return [self._get_edge_color(e) for e in self.G.edges]

    def _recalculate_depth(self, new_key: str):
        for layer, nodes in enumerate(nx.topological_generations(self.G)):
            for node in nodes:
                self.G.nodes[node][new_key] = layer

    def _calculate_depth_order(self, layer_key: str, new_key: str):
        # Add position info to the graph nodes
        pos = nx.multipartite_layout(
            self.G,
            subset_key=layer_key,
            align=self.align,
            scale=self.layout_scale,
        )
        for n, p in pos.items():
            self.G.nodes[n]['pos'] = p

        # Get all the node meta, add the name as well so we can just pass around values
        nodes = dict(self.G.nodes.items())
        nodes = {n: dict(meta, name=n) for n, meta in nodes.items()}

        # Group by partite_key
        sorted_nodes = sorted(nodes.values(), key=lambda n: n[layer_key])
        by_depth = groupby(sorted_nodes, lambda x: x[layer_key])

        # Go through each layer group
        for _, group in by_depth:
            # Extract nodes and node positions (sorted)
            group_nodes = list(group)
            group_pos = sorted([n['pos'] for n in group_nodes], key=lambda p: p[0])

            # Do a layer sort
            nodes = self._node_layer_sort(group_nodes)

            # Iterate through all running jobs, then skipped
            # Set layer_order to its order index in that layer
            for depth_order, node in enumerate(nodes):
                idx = depth_order
                left = depth_order < (len(nodes) / 2)
                self.G.nodes[node['name']][new_key] = idx
                self.G.nodes[node['name']]['curve_left'] = left
                self.G.nodes[node['name']]['pos'] = group_pos[idx]

    def get_annotations(self, xref='x', yref='y'):
        def pts(edge, key) -> float:
            pts = {
                'p1.x': self.G.nodes[edge[0]]['pos'][0],
                'p1.y': self.G.nodes[edge[0]]['pos'][1],
                'p2.x': self.G.nodes[edge[1]]['pos'][0],
                'p2.y': self.G.nodes[edge[1]]['pos'][1],
            }

            if key not in pts:
                raise ValueError(f'Key {key} not found in pts dictionary. Available keys: {list(pts.keys())}')

            return pts[key]

        # Old arrows
        _ = [
            go.layout.Annotation(
                ax=(pts(edge, 'p1.x') * 7 + pts(edge, 'p2.x') * 1) / 8,
                ay=(pts(edge, 'p1.y') * 7 + pts(edge, 'p2.y') * 1) / 8,
                x=(pts(edge, 'p1.x') * 4 + pts(edge, 'p2.x') * 4) / 8,
                y=(pts(edge, 'p1.y') * 4 + pts(edge, 'p2.y') * 4) / 8,
                axref=xref,
                ayref=yref,
                xref=xref,
                yref=yref,
                showarrow=True,
                arrowhead=3,
                arrowsize=4,
                arrowwidth=self.edge_weight,
                arrowcolor=self._get_edge_color(edge),
                opacity=self.arrow_opacity,
            )
            for edge in self.G.edges
        ]

        # Legend
        legend = (
            '<span style="color: #5053f8;">■<span style="color: black;"> Only run this stage</span><br>'
            '<span style="color: #28A745;">■<span style="color: black;"> First stage</span><br>'
            '<span style="color: #e93e2e;">■<span style="color: black;"> Last stage</span><br>'
            '<span style="color: #A9A9A9;">■<span style="color: black;"> Skipped</span><br>'
        )

        return [
            {
                'text': legend,  # The text inside the box
                'xref': 'paper',  # x-axis reference type (paper space)
                'yref': 'paper',  # y-axis reference type (paper space)
                'x': 0.5,  # x-coordinate (center)
                'y': 0.5,  # y-coordinate (center)
                'showarrow': False,  # Hide the arrow
                'font': {'size': 16},  # Font size and style
                'align': 'center',  # Align text to center
                'bgcolor': 'rgba(255, 255, 255, 0.5)',  # Background color with transparency
                'bordercolor': 'rgba(0,0,0,0)',  # Border color with no border
                'borderwidth': 2,  # Border width
            },
        ]

    def _node_layer_sort(self, nodes):
        layer_num_parity = bool(nodes[0][self.partite_key] % 2)

        degree = self.G.out_degree([n['name'] for n in nodes])
        if isinstance(degree, int):
            raise ValueError('Degree is an int, not a dict. This should not happen.')
        else:
            degree = dict(degree)
        deg_order = sorted(nodes, key=lambda n: degree.get(n['name'], 0), reverse=layer_num_parity)

        # Set largest degree towards the middle
        return deg_order[len(deg_order) % 2 :: 2] + deg_order[::-2]

    def _get_layer_range(self):
        nodes = set(filter(self._non_skipped_node, self.G.nodes))
        layer = nx.get_node_attributes(self.G, self.partite_key)
        layer = set([val for node, val in layer.items() if node in nodes])
        return min(layer), max(layer)
