"""
Test reading inputs into a Cohort object.
"""

import json
import logging

from pytest_mock import MockFixture

from cpg_flow.inputs import MultiCohort

from tests import set_config

LOGGER = logging.getLogger(__name__)


def _multicohort_config(tmp_path, cohort_ids=['COH123', 'COH456']) -> str:
    conf = f"""
    [workflow]
    dataset = 'projecta'
    input_cohorts = [{', '.join([f"'{x}'" for x in cohort_ids])}]

    path_scheme = 'local'

    [storage.default]
    default = '{tmp_path}'

    [storage.projecta]
    default = '{tmp_path}'

    [storage.projectb]
    default = '{tmp_path}'

    [references.broad]
    ref_fasta = 'stub'
    """

    return conf


def load_mock_data(file_path: str) -> dict:
    with open(file_path) as file:
        return json.load(file)


def mock_get_cohorts(cohort_id: str, *args, **kwargs) -> dict:
    return {
        'COH123': load_mock_data('tests/assets/test_multicohort/COH123.json'),
        'COH456': load_mock_data('tests/assets/test_multicohort/COH456.json'),
    }[cohort_id]


def mock_get_test_project_cohorts(cohort_id: str, *args, **kwargs) -> dict:
    return {
        'COH1': load_mock_data('tests/assets/test_multicohort/COH1.json'),
        'COH2': load_mock_data('tests/assets/test_multicohort/COH2.json'),
    }[cohort_id]


def mock_get_overlapping_cohorts(cohort_id: str, *args, **kwargs) -> dict:
    data = load_mock_data('tests/assets/test_multicohort/COH123.json')

    name = data['name']
    sgs = data['sequencing_groups']

    return {
        'COHAAA': {'name': name, 'sequencing_groups': sgs},
        'COHBBB': {'name': name + ' duplicate', 'sequencing_groups': sgs},
    }[cohort_id]


def mock_get_analysis_by_sgs(*args, **kwargs) -> dict:
    return {}


def mock_get_pedigree(*args, **kwargs):  # pylint: disable=unused-argument
    return load_mock_data('tests/assets/test_multicohort/pedigree.json')


def test_multicohort(mocker: MockFixture, tmp_path):
    """
    Testing creating a Cohort object from metamist mocks.
    """
    set_config(_multicohort_config(tmp_path), tmp_path / 'config.toml')

    mocker.patch('cpg_flow.utils.exists_not_cached', lambda *args: False)

    mocker.patch('cpg_flow.metamist.Metamist.get_ped_entries', mock_get_pedigree)
    mocker.patch('cpg_flow.metamist.Metamist.get_analyses_by_sgid', mock_get_analysis_by_sgs)
    # don't patch the method location, patch where it's imported/called
    mocker.patch('cpg_flow.inputs.get_cohort_sgs', mock_get_cohorts)

    from cpg_flow.inputs import get_multicohort

    multicohort = get_multicohort()

    assert multicohort
    assert isinstance(multicohort, MultiCohort)

    # Testing Cohort Information
    cohorts = multicohort.get_cohorts()
    assert len(cohorts) == 2
    assert cohorts[0].name == 'Cohort #123'
    assert cohorts[1].name == 'Cohort #456'

    assert len(multicohort.get_sequencing_groups()) == 4
    assert sorted(multicohort.get_sequencing_group_ids()) == [
        'CPGAAAA',
        'CPGCCCCCC',
        'CPGDDDDDD',
        'CPGXXXX',
    ]

    # Test the projects they belong to
    assert multicohort.get_sequencing_groups()[0].dataset.name == 'projecta'
    assert multicohort.get_sequencing_groups()[1].dataset.name == 'projecta'
    assert multicohort.get_sequencing_groups()[2].dataset.name == 'projectb'
    assert multicohort.get_sequencing_groups()[3].dataset.name == 'projectb'

    test_sg_a = multicohort.get_sequencing_groups()[0]
    test_sg_b = multicohort.get_sequencing_groups()[2]

    # Test SequenceGroup Population
    assert test_sg_a.id == 'CPGXXXX'
    assert test_sg_a.external_id == 'NA12340'
    assert test_sg_a.participant_id == '8'
    assert test_sg_a.meta == {'sg_meta': 'is_fun', 'participant_meta': 'is_here', 'phenotypes': {}}

    assert test_sg_b.id == 'CPGCCCCCC'
    assert test_sg_b.external_id == 'NA111111'
    assert test_sg_b.participant_id == '10'
    assert test_sg_b.meta == {'sg_meta': 'is_awesome', 'participant_meta': 'is_here', 'phenotypes': {}}


def test_overlapping_multicohort(mocker: MockFixture, tmp_path):
    """
    Testing multicohorts where different cohorts have sgs from the same dataset.
    """
    set_config(_multicohort_config(tmp_path, ['COHAAA', 'COHBBB']), tmp_path / 'config.toml')

    mocker.patch('cpg_flow.utils.exists_not_cached', lambda *args: False)

    mocker.patch('cpg_flow.metamist.Metamist.get_ped_entries', mock_get_pedigree)
    mocker.patch('cpg_flow.metamist.Metamist.get_analyses_by_sgid', mock_get_analysis_by_sgs)
    mocker.patch('cpg_flow.inputs.get_cohort_sgs', mock_get_overlapping_cohorts)

    from cpg_flow.inputs import get_multicohort

    multicohort = get_multicohort()

    assert multicohort
    assert isinstance(multicohort, MultiCohort)

    # Testing Cohort Information
    assert len(multicohort.get_sequencing_groups()) == 2
    assert multicohort.get_sequencing_group_ids() == ['CPGXXXX', 'CPGAAAA']

    # Test the projects they belong to
    assert multicohort.get_sequencing_groups()[0].dataset.name == 'projecta'
    assert multicohort.get_sequencing_groups()[1].dataset.name == 'projecta'

    test_sg_a = multicohort.get_sequencing_groups()[0]

    # Test SequenceGroup Population

    # Validate Cohort Names
    cohorts = multicohort.get_cohorts()
    assert len(cohorts) == 2
    assert cohorts[0].name == 'Cohort #123'
    assert cohorts[1].name == 'Cohort #123 duplicate'

    assert test_sg_a.id == 'CPGXXXX'
    assert test_sg_a.external_id == 'NA12340'
    assert test_sg_a.participant_id == '8'
    assert test_sg_a.meta == {'sg_meta': 'is_fun', 'participant_meta': 'is_here', 'phenotypes': {}}

    for cohort in multicohort.get_cohorts():
        assert len(cohort.get_sequencing_group_ids()) == 2


def test_multicohort_dataset_config(mocker: MockFixture, tmp_path):
    """
    This test is to ensure that the dataset name is stripped of the '-test' suffix.
    """
    set_config(_multicohort_config(tmp_path, ['COH1', 'COH2']), tmp_path / 'config.toml')

    mocker.patch('cpg_flow.utils.exists_not_cached', lambda *args: False)

    mocker.patch('cpg_flow.metamist.Metamist.get_ped_entries', mock_get_pedigree)
    mocker.patch('cpg_flow.metamist.Metamist.get_analyses_by_sgid', mock_get_analysis_by_sgs)
    # mockup the cohort data with '-test' suffix
    mocker.patch('cpg_flow.inputs.get_cohort_sgs', mock_get_test_project_cohorts)

    from cpg_flow.inputs import get_multicohort

    multicohort = get_multicohort()

    assert multicohort
    assert isinstance(multicohort, MultiCohort)

    # Testing Cohort Information
    cohorts = multicohort.get_cohorts()
    assert len(cohorts) == 2
    assert cohorts[0].name == 'Cohort #1'
    assert cohorts[1].name == 'Cohort #2'

    assert len(multicohort.get_sequencing_groups()) == 4
    assert sorted(multicohort.get_sequencing_group_ids()) == ['CPGAAAA', 'CPGCCCCCC', 'CPGDDDDDD', 'CPGXXXX']

    # Test the projects they belong to
    # Datasets name should be without '-test' suffix
    assert multicohort.get_sequencing_groups()[0].dataset.name == 'projecta'
    assert multicohort.get_sequencing_groups()[1].dataset.name == 'projecta'
    assert multicohort.get_sequencing_groups()[2].dataset.name == 'projectb'
    assert multicohort.get_sequencing_groups()[3].dataset.name == 'projectb'
