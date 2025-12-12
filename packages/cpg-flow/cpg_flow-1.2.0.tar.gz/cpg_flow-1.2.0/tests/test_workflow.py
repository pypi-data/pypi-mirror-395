"""
Test building Workflow object.
"""

import pathlib
from collections.abc import Collection, Mapping, Sequence
from typing import Any, Final
from unittest import mock

import networkx as nx
import pytest

from cpg_flow.inputs import get_multicohort
from cpg_flow.stage import (
    CohortStage,
    SequencingGroupStage,
    StageInput,
    StageOutput,
    stage,
)
from cpg_flow.targets import Cohort, MultiCohort, SequencingGroup
from cpg_flow.workflow import _render_graph, path_walk, run_workflow
from cpg_utils.config import dataset_path
from cpg_utils.hail_batch import get_batch

from tests import set_config

TOML = """
[workflow]
dataset_gcp_project = 'fewgenomes'
access_level = 'test'
dataset = 'fewgenomes'
driver_image = 'test'
sequencing_type = 'genome'

check_inputs = false
check_intermediates = false
check_expected_outputs = false
path_scheme = 'local'

[storage.default]
default = "{directory}"

[storage.fewgenomes]
default = "{directory}"

[hail]
billing_project = 'fewgenomes'
delete_scratch_on_exit = false
backend = 'local'
"""


def mock_create_create_cohort(*_) -> MultiCohort:
    m = MultiCohort()
    c = m.create_cohort(id='COH123', name='fewgenomes')
    ds = m.create_dataset('my_dataset')

    def add_sg(id, external_id):
        return ds.add_sequencing_group(
            id=id,
            external_id=external_id,
            sequencing_type='genome',
            sequencing_technology='short-read',
            sequencing_platform='illumina',
        )

    c.add_sequencing_group_object(add_sg('CPGAA', external_id='SAMPLE1'))
    c.add_sequencing_group_object(add_sg('CPGBB', external_id='SAMPLE2'))
    return m


@mock.patch('cpg_flow.inputs.create_multicohort', mock_create_create_cohort)
def test_workflow(tmp_path: pathlib.Path):
    """
    Testing running a workflow from a mock cohort.
    """
    conf = TOML.format(directory=tmp_path)
    set_config(conf, tmp_path / 'config.toml')

    output_path = pathlib.Path(dataset_path('cohort.tsv'))

    multi_cohort = get_multicohort()

    assert len(multi_cohort.get_sequencing_groups()) == 2

    assert multi_cohort.alignment_inputs_hash is None
    mc_hash = multi_cohort.get_alignment_inputs_hash()
    assert multi_cohort.alignment_inputs_hash == mc_hash
    assert mc_hash == 'e3b0c44298fc1c149afbf4c8996fb92427ae41_2'

    assert multi_cohort.sg_hash is None
    mc_sg_hash = multi_cohort.get_sg_hash()
    assert multi_cohort.sg_hash == mc_sg_hash
    assert mc_sg_hash == '5ecfbcb86b94df30ddb6b9d4cfe3e3f49c31a3_2'

    @stage
    class MySequencingGroupStage(SequencingGroupStage):
        """
        Just a sequencing-group-level stage.
        """

        def expected_outputs(self, sequencing_group: SequencingGroup) -> pathlib.Path:
            return pathlib.Path(dataset_path(f'{sequencing_group.id}.tsv'))

        def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
            j = get_batch().new_job('SequencingGroup job', self.get_job_attrs(sequencing_group))
            j.command(f'echo {sequencing_group.id}_done >> {j.output}')
            get_batch().write_output(j.output, str(self.expected_outputs(sequencing_group)))
            print(f'Writing to {self.expected_outputs(sequencing_group)}')
            return self.make_outputs(sequencing_group, self.expected_outputs(sequencing_group))

    @stage(required_stages=MySequencingGroupStage)
    class MyCohortStage(CohortStage):
        """
        Just a cohort-level stage.
        """

        def expected_outputs(self, _: Cohort) -> pathlib.Path:
            return output_path

        def queue_jobs(self, cohort: Cohort, inputs: StageInput) -> StageOutput | None:
            path_by_sg = inputs.as_path_by_target(MySequencingGroupStage)
            assert len(path_by_sg) == len(cohort.get_sequencing_groups())
            j = get_batch().new_job('Cohort job', self.get_job_attrs(cohort))
            j.command(f'touch {j.output}')
            for _, sg_result_path in path_by_sg.items():
                input_file = get_batch().read_input(str(sg_result_path))
                j.command(f'cat {input_file} >> {j.output}')
            get_batch().write_output(j.output, str(self.expected_outputs(cohort)))
            print(f'Writing to {self.expected_outputs(cohort)}')
            return self.make_outputs(cohort, self.expected_outputs(cohort))

    run_workflow(name='test_workflow', stages=[MyCohortStage])

    print(f'Checking result in {output_path}:')
    with output_path.open() as f:
        result = f.read()
        assert result.split() == ['CPGAA_done', 'CPGBB_done'], result


def test_path_walk():
    """
    tests the recursive path walk to find all stage outputs
    the recursive method can unpack any nested structure
    end result is a set of all Paths
    Note: Strings in this dict are not turned into Paths
    """

    exp = {
        'a': pathlib.Path('this.txt'),
        'b': [pathlib.Path('that.txt'), {'c': pathlib.Path('the_other.txt')}],
        'd': 'string.txt',
    }
    act = path_walk(exp)
    assert act == {pathlib.Path('this.txt'), pathlib.Path('that.txt'), pathlib.Path('the_other.txt')}


@pytest.fixture()
def mock_render_constants(monkeypatch: pytest.MonkeyPatch):
    """Mocks the rendering constants used by _render_graph."""
    monkeypatch.setattr('cpg_flow.workflow._TARGET', '<TARGET>')
    monkeypatch.setattr('cpg_flow.workflow._ONLY', '<ONLY>')
    monkeypatch.setattr('cpg_flow.workflow._START', '<START>')
    monkeypatch.setattr('cpg_flow.workflow._END', '<END>')
    monkeypatch.setattr('cpg_flow.workflow._ARROW', ' -> ')
    # Don't care about presence of ANSI escapes
    monkeypatch.setattr('cpg_flow.workflow._BOLD', '')
    monkeypatch.setattr('cpg_flow.workflow._WHITE', '')
    monkeypatch.setattr('cpg_flow.workflow._BLUE', '')
    monkeypatch.setattr('cpg_flow.workflow._DARK', '')
    monkeypatch.setattr('cpg_flow.workflow._RESET', '')


def _create_graph_with_attrs(edges: Sequence[tuple[str, str]], skipped_nodes: Collection[str]) -> nx.DiGraph:
    graph = nx.DiGraph()
    # workflow uses a graph with node -> dependencies, but displays the reverse order.
    # It's easier to write the test inputs in the reverse order too.
    graph.add_edges_from((t, s) for (s, t) in edges)
    nx.set_node_attributes(graph, {n: n in skipped_nodes for n in graph.nodes}, 'skipped')
    for order, n in enumerate(reversed(list(nx.topological_sort(graph)))):
        graph.nodes[n]['order'] = order
    return graph


_COMPLEX_GRAPH: Final[tuple[tuple[str, str], ...]] = (
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'D'),
    ('A', 'D'),
    ('D', 'E'),
    ('D', 'F'),
)


class TestRenderGraph:
    @pytest.mark.parametrize(
        ['edges', 'skipped_nodes', 'expected'],
        [
            pytest.param([], {}, '', id='empty_graph'),
            pytest.param(
                [('A', 'B')],
                set(),
                'A[0] -> B[1]',
                id='one_edge',
            ),
            pytest.param(
                [('A', 'B')],
                {'A'},
                'A -> B[1]',
                id='one_edge_one_skipped_node',
            ),
            pytest.param(
                [('A', 'B'), ('B', 'C'), ('A', 'C')],
                set(),
                'A[0] -> {B,C};A -> B[1] -> C[2]',
                id='triangle',
            ),
            pytest.param(
                _COMPLEX_GRAPH,
                set(),
                'A[0] -> {B,D};A -> B[1] -> C[2] -> D[3] -> {E,F};      D -> E[5];      D -> F[4]',
                id='complex_graph',
            ),
        ],
    )
    def test_render_graph(
        self,
        edges: Sequence[tuple[str, str]],
        skipped_nodes: set[str],
        expected: str,
        mock_render_constants,
    ):
        graph = _create_graph_with_attrs(edges, skipped_nodes)
        result = ';'.join(_render_graph(graph))
        assert result == expected

    @pytest.mark.parametrize(
        ['edges', 'skipped_nodes', 'extra_args', 'expected'],
        [
            pytest.param(
                _COMPLEX_GRAPH,
                set(),
                dict(only_stages={'D'}),
                'A[0] -> {B,D};A -> B[1] -> C[2] -> <ONLY>D[3] -> {E,F};      D -> E[5];      D -> F[4]',
                id='complex_graph_only_nodes',
            ),
            pytest.param(
                _COMPLEX_GRAPH,
                set(),
                dict(target_stages={'E', 'F'}),
                'A[0] -> {B,D};A -> B[1] -> C[2] -> D[3] -> {E,F};      D -> E[5]<TARGET>;      D -> F[4]<TARGET>',
                id='complex_graph_only_nodes',
            ),
            pytest.param(
                _COMPLEX_GRAPH,
                set(),
                dict(first_stages={'A'}, last_stages={'E', 'F'}),
                '<START>A[0] -> {B,D};A -> B[1] -> C[2] -> D[3] -> {E,F};      D -> E<END>[5];      D -> F<END>[4]',
                id='complex_graph_only_nodes',
            ),
        ],
    )
    def test_render_graph_extra_args(
        self,
        edges: Sequence[tuple[str, str]],
        skipped_nodes: set[str],
        extra_args: Mapping[str, Any],
        expected: str,
        mock_render_constants,
    ):
        graph = _create_graph_with_attrs(edges, skipped_nodes)
        result = ';'.join(_render_graph(graph, **extra_args))
        assert result == expected
