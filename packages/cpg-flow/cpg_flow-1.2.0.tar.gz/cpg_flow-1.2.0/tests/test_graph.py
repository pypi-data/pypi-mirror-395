import networkx as nx
import pytest

from src.cpg_flow.show_workflow.graph import GraphPlot


@pytest.fixture
def sample_graph():
    """
    Create a sample directed graph for testing.
    """
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ('A', 'B'),
            ('B', 'C'),
            ('C', 'D'),
            ('A', 'E'),
            ('E', 'F'),
            ('F', 'D'),
        ],
    )
    all_nodes_false = dict.fromkeys(G.nodes, False)

    nx.set_node_attributes(G, all_nodes_false, 'skipped')
    nx.set_node_attributes(G, all_nodes_false, 'skip_stages')
    nx.set_node_attributes(G, all_nodes_false, 'only_stages')
    nx.set_node_attributes(G, all_nodes_false, 'first_stages')
    nx.set_node_attributes(G, all_nodes_false, 'last_stages')
    return G


def test_graphplot_initialization(sample_graph):
    """
    Test the initialization of the GraphPlot class.
    """
    graph_plot = GraphPlot(sample_graph)
    assert graph_plot.G is not None
    assert isinstance(graph_plot.G, nx.DiGraph)
    assert graph_plot.title == 'Workflow Graph'
    assert graph_plot.node_size == 5
    assert graph_plot.arrow_size == 10


def test_graphplot_recalculate_depth(sample_graph):
    """
    Test the depth recalculation logic.
    """
    graph_plot = GraphPlot(sample_graph)
    graph_plot._recalculate_depth(new_key='test_depth')
    for node, data in graph_plot.G.nodes(data=True):
        assert 'test_depth' in data
        assert isinstance(data['test_depth'], int)


def test_graphplot_calculate_depth_order(sample_graph):
    """
    Test the depth order calculation logic.
    """
    graph_plot = GraphPlot(sample_graph)
    graph_plot._calculate_depth_order(layer_key='layer', new_key='layer_order')
    for node, data in graph_plot.G.nodes(data=True):
        assert 'layer_order' in data
        assert isinstance(data['layer_order'], int)


def test_graphplot_create_traces(sample_graph):
    """
    Test the creation of traces for the graph.
    """
    graph_plot = GraphPlot(sample_graph)
    traces = graph_plot.create_traces()
    assert isinstance(traces, list)
    assert len(traces) > 0


def test_graphplot_create_figure(sample_graph):
    """
    Test the creation of a figure for the graph.
    """
    graph_plot = GraphPlot(sample_graph)
    figure = graph_plot.create_figure()
    assert figure is not None
    assert hasattr(figure, 'data')
    assert hasattr(figure, 'layout')


def test_graphplot_get_node_positions(sample_graph):
    """
    Test the retrieval of node positions.
    """
    graph_plot = GraphPlot(sample_graph)
    node_x, node_y = graph_plot._get_node_positions()
    assert len(node_x) == len(sample_graph.nodes)
    assert len(node_y) == len(sample_graph.nodes)


def test_graphplot_get_edge_positions(sample_graph):
    """
    Test the retrieval of edge positions.
    """
    graph_plot = GraphPlot(sample_graph)
    edge_x, edge_y, edge_names, mid_x, mid_y, mid_angles = graph_plot._get_edge_positions(filter_fun=lambda x: True)
    assert len(edge_x) > 0
    assert len(edge_y) > 0
    assert len(edge_names) == len(sample_graph.edges)
    assert len(mid_x) == len(sample_graph.edges)
    assert len(mid_y) == len(sample_graph.edges)
    assert len(mid_angles) == len(sample_graph.edges)


def test_graphplot_non_skipped_edge(sample_graph):
    """
    Test the logic for determining non-skipped edges.
    """
    graph_plot = GraphPlot(sample_graph)
    for edge in sample_graph.edges:
        assert graph_plot._non_skipped_edge(edge) is True


def test_graphplot_non_skipped_node(sample_graph):
    """
    Test the logic for determining non-skipped nodes.
    """
    graph_plot = GraphPlot(sample_graph)
    for node in sample_graph.nodes:
        assert graph_plot._non_skipped_node(node) is True
