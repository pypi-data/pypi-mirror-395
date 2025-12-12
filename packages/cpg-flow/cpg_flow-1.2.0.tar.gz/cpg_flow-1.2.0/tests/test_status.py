"""
Test workflow status reporter.
"""

from pathlib import Path
from typing import Any

import pytest
from pytest_mock import MockFixture

from cpg_flow.inputs import get_multicohort
from cpg_flow.stage import (
    SequencingGroupStage,
    StageInput,
    StageOutput,
    stage,
)
from cpg_flow.targets import MultiCohort, SequencingGroup
from cpg_flow.workflow import WorkflowError, run_workflow
from cpg_utils import Path as CPGPath
from cpg_utils import to_path
from cpg_utils.config import dataset_path
from cpg_utils.hail_batch import get_batch, reset_batch

from tests import set_config

TOML = """
[workflow]
dataset_gcp_project = 'fewgenomes'
access_level = 'test'
dataset = 'fewgenomes'
driver_image = '<stub>'
sequencing_type = 'genome'
status_reporter = 'metamist'

check_inputs = false
check_intermediates = false
check_expected_outputs = false
path_scheme = 'local'

[storage.default]
default = '{directory}'

[storage.fewgenomes]
default = '{directory}'

[hail]
billing_project = 'fewgenomes'
delete_scratch_on_exit = false
backend = 'local'
dry_run = true

[images]
cpg_flow = "stub"
"""


def _common(mocker, tmp_path):
    conf = TOML.format(directory=tmp_path)

    set_config(
        conf,
        tmp_path / 'config.toml',
        merge_with=[
            Path(to_path(__file__).parent.parent / 'src' / 'cpg_flow' / 'defaults.toml'),
        ],
    )

    def mock_create_analysis(_, project, analysis) -> int:
        print(f'Analysis model in project {project}: {analysis}')
        return 1  # metamist "analysis" entry ID

    mocker.patch('metamist.apis.AnalysisApi.create_analysis', mock_create_analysis)

    def mock_create_cohort(*_) -> MultiCohort:
        m = MultiCohort()
        c = m.create_cohort(id='COH123', name='fewgenomes')
        ds = m.create_dataset('my_dataset')

        def add_sg(id, external_id):
            return ds.add_sequencing_group(
                id,
                external_id=external_id,
                sequencing_type='genome',
                sequencing_technology='short-read',
                sequencing_platform='illumina',
            )

        c.add_sequencing_group_object(add_sg('CPGAA', external_id='SAMPLE1'))
        c.add_sequencing_group_object(add_sg('CPGBB', external_id='SAMPLE2'))
        return m

    mocker.patch('cpg_flow.inputs.create_multicohort', mock_create_cohort)


def test_status_reporter(mocker: MockFixture, tmp_path):
    _common(mocker, tmp_path)

    @stage(analysis_type='qc')
    class MyQcStage1(SequencingGroupStage):
        """
        Just a sequencing-group-level stage.
        """

        @staticmethod
        def expected_outputs(sequencing_group: SequencingGroup) -> CPGPath:
            return to_path(dataset_path(f'{sequencing_group.id}.tsv'))

        def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
            j = get_batch().new_job('Echo', self.get_job_attrs(sequencing_group) | dict(tool='echo'))
            j.command(f'echo {sequencing_group.id}_done >> {j.output}')
            get_batch().write_output(j.output, str(self.expected_outputs(sequencing_group)))
            print(f'Writing to {self.expected_outputs(sequencing_group)}')
            return self.make_outputs(sequencing_group, self.expected_outputs(sequencing_group), jobs=j)

    @stage(analysis_type='qc', analysis_keys=['bed'])
    class MyQcStage2(SequencingGroupStage):
        """
        Just a sequencing-group-level stage.
        """

        @staticmethod
        def expected_outputs(sequencing_group: SequencingGroup) -> dict:
            return {
                'bed': to_path(dataset_path(f'{sequencing_group.id}.bed')),
                'tsv': to_path(dataset_path(f'{sequencing_group.id}.tsv')),
            }

        def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
            j = get_batch().new_job('Echo', self.get_job_attrs(sequencing_group) | dict(tool='echo'))
            j.command(f'echo {sequencing_group.id}_done >> {j.output}')
            get_batch().write_output(j.output, str(self.expected_outputs(sequencing_group)['bed']))
            print(f'Writing to {self.expected_outputs(sequencing_group)["bed"]}')
            return self.make_outputs(sequencing_group, self.expected_outputs(sequencing_group), jobs=j)

    reset_batch()
    run_workflow(name='test-status-reporter', stages=[MyQcStage1, MyQcStage2])

    print(get_batch().job_by_tool['metamist'])
    assert 'metamist' in get_batch().job_by_tool, get_batch().job_by_tool
    # 2 jobs per sequencing group (2 analysis outputs)
    assert get_batch().job_by_tool['metamist']['job_n'] == len(get_multicohort().get_sequencing_groups()) * 2


def _update_meta(output_path: str) -> dict[str, Any]:
    with to_path(output_path).open() as f:
        return {'result': f.read().strip()}


def test_status_reporter_with_custom_updater(mocker: MockFixture, tmp_path):
    _common(mocker, tmp_path)

    @stage(analysis_type='qc', update_analysis_meta=_update_meta)
    class MyQcStage(SequencingGroupStage):
        @staticmethod
        def expected_outputs(sequencing_group: SequencingGroup) -> CPGPath:
            return to_path(dataset_path(f'{sequencing_group.id}.tsv'))

        def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
            j = get_batch().new_job('Echo', self.get_job_attrs(sequencing_group) | {'tool': 'echo'})
            j.command(f'echo 42 >> {j.output}')
            get_batch().write_output(j.output, str(self.expected_outputs(sequencing_group)))
            return self.make_outputs(sequencing_group, self.expected_outputs(sequencing_group), jobs=j)

    run_workflow(name='test-status-reporter-with-custom-updater', stages=[MyQcStage])

    assert 'metamist' in get_batch().job_by_tool, get_batch().job_by_tool


def test_status_reporter_fails(mocker: MockFixture, tmp_path):
    _common(mocker, tmp_path)

    @stage(analysis_type='qc')
    class MyQcStage(SequencingGroupStage):
        """
        Just a sequencing-group-level stage.
        """

        @staticmethod
        def expected_outputs(sequencing_group: SequencingGroup) -> dict:
            return {
                'bed': dataset_path(f'{sequencing_group.id}.bed'),
                'tsv': dataset_path(f'{sequencing_group.id}.tsv'),
            }

        def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
            j = get_batch().new_job('Echo', self.get_job_attrs(sequencing_group) | dict(tool='echo'))
            j.command(f'echo {sequencing_group.id}_done >> {j.output}')
            get_batch().write_output(j.output, str(self.expected_outputs(sequencing_group)['bed']))
            print(f'Writing to {self.expected_outputs(sequencing_group)["bed"]}')
            return self.make_outputs(sequencing_group, self.expected_outputs(sequencing_group), jobs=j)

    with pytest.raises(WorkflowError):
        run_workflow(name='test-status-reporter-fails', stages=[MyQcStage])
