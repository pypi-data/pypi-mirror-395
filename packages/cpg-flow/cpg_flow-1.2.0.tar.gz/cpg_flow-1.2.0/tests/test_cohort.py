"""
Test reading inputs into a Cohort object.
"""

import json
import logging
import re

import pytest
from pytest_mock import MockFixture

from cpg_flow.metamist import MetamistError
from cpg_flow.targets import MultiCohort

from tests import set_config

LOGGER = logging.getLogger(__name__)


# region CONFIG MOCKS


def _cohort_config(tmp_path, cohort_ids: list[str] | None = None, input_datasets: list[str] | None = None) -> str:
    cohort_ids_string, input_datasets_string = '', ''

    if cohort_ids is not None:
        cohort_ids = [f"'{cohort_id}'" for cohort_id in cohort_ids]
        cohort_ids_string = 'input_cohorts = [' + ', '.join(cohort_ids) + ']'

    if input_datasets is not None:
        input_datasets = [f"'{dataset}'" for dataset in input_datasets]
        input_datasets_string = 'input_datasets = [' + ', '.join(input_datasets) + ']'

    conf = f"""
    [workflow]
    dataset_gcp_project = 'fewgenomes'
    access_level = 'test'
    dataset = 'fewgenomes'
    sequencing_type = 'genome'
    {input_datasets_string if input_datasets is not None else ''}
    {cohort_ids_string if cohort_ids is not None else ''}

    check_inputs = false
    check_intermediates = false
    check_expected_outputs = false
    path_scheme = 'local'

    populate_assays = true

    [storage.default]
    default = '{tmp_path}'

    [storage.fewgenomes]
    default = '{tmp_path}'

    [large_cohort]
    training_pop = 'Superpopulation name'

    [hail]
    billing_project = 'fewgenomes'
    delete_scratch_on_exit = false
    backend = 'local'

    [references.broad]
    ref_fasta = 'stub'
    """

    return conf


def _custom_cohort_config(tmp_path) -> str:
    conf = f"""
    [workflow]
    dataset = 'projecta'
    input_cohorts = ['COH5']

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


# endregion CONFIG MOCKS

# region DATA MOCKS


def load_mock_data(file_path: str) -> dict:
    with open(file_path) as file:
        return json.load(file)


def mock_get_analysis_by_sgs(*args, **kwargs) -> dict:
    return {}


def mock_get_pedigree_empty(*args, **kwargs):
    return []


def mock_get_pedigree(*args, **kwargs):  # pylint: disable=unused-argument
    return load_mock_data('tests/assets/test_cohort/pedigree.json')


def mock_get_cohort_sgs(cohort_id: str, *args, **kwargs) -> dict:
    cohorts = {
        'COH1': load_mock_data('tests/assets/test_cohort/COH1.json'),
        'COH2': load_mock_data('tests/assets/test_cohort/COH2.json'),
        'COH3': load_mock_data('tests/assets/test_cohort/COH3.json'),
        'COH4': load_mock_data('tests/assets/test_cohort/COH4.json'),
        'COH5': load_mock_data('tests/assets/test_cohort/COH5.json'),
    }

    if cohort_id not in cohorts:
        raise MetamistError(f"Error fetching cohort: The provided cohort ID was not valid: '{cohort_id}'")

    return cohorts[cohort_id]


# endregion DATA MOCKS


def test_no_input_cohorts(mocker: MockFixture, tmp_path, caplog):
    """
    Testing if no input cohorts are provided in the config under input_cohorts
    The code should error out with a helpful message and return None
    """
    # This config will have no 'input_cohorts' argument
    set_config(_cohort_config(tmp_path, cohort_ids=[]), tmp_path / 'config.toml')

    # Assert the value error is raised
    from cpg_flow.inputs import get_multicohort

    expected_error = 'No custom_cohort_ids found in the config'
    with pytest.raises(ValueError, match=re.escape(expected_error)):
        get_multicohort()


def test_input_cohorts_dont_exist(mocker: MockFixture, tmp_path, caplog):
    # This config will 'input_cohorts = [COH09876543]' but the cohort doesn't exist
    missing_cohort_id = 'COH09876543'
    set_config(_cohort_config(tmp_path, cohort_ids=[missing_cohort_id]), tmp_path / 'config.toml')

    mocker.patch('cpg_flow.inputs.get_cohort_sgs', mock_get_cohort_sgs)

    # Assert the value error is raised
    from cpg_flow.inputs import get_multicohort

    expected_error = f"Error fetching cohort: The provided cohort ID was not valid: '{missing_cohort_id}'"
    with pytest.raises(MetamistError, match=re.escape(expected_error)):
        get_multicohort()


def test_input_datasets_deprecated(mocker: MockFixture, tmp_path, caplog):
    # Assert the value error is raised
    from cpg_flow.inputs import get_multicohort

    # This config will 'input_datasets = [DATASET098765432]' which is deprecated
    set_config(_cohort_config(tmp_path, input_datasets=['DATASET098765']), tmp_path / 'config.toml')

    expected_error = 'Argument input_datasets is deprecated, use input_cohorts instead'
    with pytest.raises(ValueError, match=re.escape(expected_error)):
        get_multicohort()


def test_cohort(mocker: MockFixture, tmp_path, caplog):
    """
    Testing creating a Cohort object from metamist mocks.
    """
    set_config(_cohort_config(tmp_path, ['COH1']), tmp_path / 'config.toml')

    mocker.patch('cpg_flow.utils.exists_not_cached', lambda *args: False)

    mocker.patch('cpg_flow.metamist.Metamist.get_ped_entries', mock_get_pedigree)

    mocker.patch('cpg_flow.metamist.Metamist.get_sg_entries', mock_get_cohort_sgs('COH1'))
    mocker.patch('cpg_flow.metamist.Metamist.get_analyses_by_sgid', mock_get_analysis_by_sgs)

    mocker.patch('cpg_flow.inputs.get_cohort_sgs', mock_get_cohort_sgs)

    caplog.set_level(logging.WARNING)

    from cpg_flow.inputs import get_multicohort
    from cpg_flow.targets import SequencingGroup, Sex

    multicohort = get_multicohort()

    assert multicohort
    assert isinstance(multicohort, MultiCohort)

    # Testing Cohort Information
    assert len(multicohort.get_sequencing_groups()) == 2
    assert multicohort.get_sequencing_group_ids() == ['CPGLCL17', 'CPGLCL25']

    for sg in multicohort.get_sequencing_groups():
        assert sg.dataset.name == 'fewgenomes'
        assert not sg.forced
        assert sg.cram is None
        assert sg.gvcf is None

    # Test SequenceGroup Population
    test_sg = multicohort.get_sequencing_groups()[0]
    test_sg2 = multicohort.get_sequencing_groups()[1]
    assert test_sg.id == 'CPGLCL17'
    assert test_sg.external_id == 'NA12340'
    assert test_sg.participant_id == '8'
    assert test_sg.meta == {'sg_meta': 'is_fun', 'participant_meta': 'is_here', 'phenotypes': {}}

    # Test Assay Population
    assert test_sg.assays
    assert test_sg.assays[0].sequencing_group_id == 'CPGLCL17'
    assert test_sg.assays[0].id == '1'
    assert test_sg.assays[0].meta['fluid_x_tube_id'] == '220405_FS28'

    assert test_sg.participant_id == '8'
    # TODO/NOTE: The sex in the pedigree will overwrite the sex in the
    # sequencing group. We should add a check and a test.
    # Also test for unknown reported sex with no ped information.

    assert test_sg.pedigree.sex == Sex.MALE
    assert test_sg2.pedigree.sex == Sex.FEMALE

    assert test_sg.pedigree.mom is None
    assert isinstance(test_sg.pedigree.dad, SequencingGroup)
    assert test_sg.pedigree.dad.participant_id == '14'

    # Test _sequencing_group_by_id attribute
    assert multicohort.get_datasets()[0]._sequencing_group_by_id.keys() == {
        'CPGLCL17',
        'CPGLCL25',
    }
    assert multicohort.get_datasets()[0]._sequencing_group_by_id['CPGLCL17'].id == 'CPGLCL17'
    assert multicohort.get_datasets()[0]._sequencing_group_by_id['CPGLCL25'].id == 'CPGLCL25'


def test_missing_reads(mocker: MockFixture, tmp_path):
    """
    Testing creating a Cohort object from metamist mocks.
    """
    set_config(_cohort_config(tmp_path, ['COH2']), tmp_path / 'config.toml')

    # mock file not existing
    mocker.patch('cpg_flow.utils.exists_not_cached', lambda *args: False)

    mocker.patch('cpg_flow.metamist.Metamist.get_ped_entries', mock_get_pedigree)

    mocker.patch(
        'cpg_flow.metamist.Metamist.get_sg_entries',
        mock_get_cohort_sgs('COH1'),
    )
    mocker.patch('cpg_flow.metamist.Metamist.get_analyses_by_sgid', mock_get_analysis_by_sgs)

    mocker.patch('cpg_flow.inputs.get_cohort_sgs', mock_get_cohort_sgs)

    # from cpg_flow.filetypes import BamPath
    from cpg_flow.inputs import get_multicohort
    from cpg_flow.targets import Sex

    cohort = get_multicohort()

    assert cohort

    # Testing Cohort Information
    assert len(cohort.get_sequencing_groups()) == 2
    assert cohort.get_sequencing_group_ids() == ['CPGLCL17', 'CPGLCL25']

    for sg in cohort.get_sequencing_groups():
        assert sg.dataset.name == 'fewgenomes'
        assert not sg.forced
        assert sg.cram is None
        assert sg.gvcf is None

    # Test SequenceGroup Population
    test_sg = cohort.get_sequencing_groups()[0]
    test_sg2 = cohort.get_sequencing_groups()[1]
    assert test_sg.id == 'CPGLCL17'
    assert test_sg.external_id == 'NA12340'
    assert test_sg.participant_id == '8'
    assert test_sg.meta == {'sg_meta': 'is_fun', 'participant_meta': 'is_here', 'phenotypes': {}}

    # Test Assay Population
    assert test_sg.assays
    assert test_sg.assays[0].sequencing_group_id == 'CPGLCL17'
    assert test_sg.assays[0].id == '1'
    assert test_sg.assays[0].meta['fluid_x_tube_id'] == '220405_FS28'

    assert test_sg.participant_id == '8'
    assert test_sg.pedigree.sex == Sex.MALE
    assert test_sg2.pedigree.sex == Sex.FEMALE

    # Test _sequencing_group_by_id attribute
    assert cohort.get_datasets()[0]._sequencing_group_by_id.keys() == {
        'CPGLCL17',
        'CPGLCL25',
    }
    assert cohort.get_datasets()[0]._sequencing_group_by_id['CPGLCL17'].id == 'CPGLCL17'
    assert cohort.get_datasets()[0]._sequencing_group_by_id['CPGLCL25'].id == 'CPGLCL25'

    # Test reads
    # assert test_sg.alignment_input_by_seq_type['genome'][0].r1 == CloudPath(
    #     'gs://cpg-fewgenomes-main/HG3FMDSX3_2_220405_FS28_Homo-sapiens_AACGAGGCCG-ATCCAGGTAT_R_220208_BINKAN1_FEWGENOMES_M001_R1.fastq.gz'
    # )
    # TODO: what should this result be?
    assert test_sg2.alignment_input is None


def test_mixed_reads(mocker: MockFixture, tmp_path, caplog):
    """
    Testing creating a Cohort object from metamist mocks.
    """

    caplog.set_level(logging.WARNING)
    set_config(_cohort_config(tmp_path, ['COH3']), tmp_path / 'config.toml')

    mocker.patch('cpg_flow.utils.exists_not_cached', lambda *args: True)

    mocker.patch('cpg_flow.metamist.Metamist.get_ped_entries', mock_get_pedigree)

    mocker.patch(
        'cpg_flow.metamist.Metamist.get_sg_entries',
        mock_get_cohort_sgs('COH3'),
    )
    mocker.patch('cpg_flow.metamist.Metamist.get_analyses_by_sgid', mock_get_analysis_by_sgs)

    mocker.patch('cpg_flow.inputs.get_cohort_sgs', mock_get_cohort_sgs)

    from cpg_flow.inputs import get_multicohort

    cohort = get_multicohort()

    # Testing Cohort Information
    assert len(cohort.get_sequencing_groups()) == 3
    assert cohort.get_sequencing_group_ids() == ['CPGccc', 'CPGbbb', 'CPGaaa']

    # test_genome = cohort.get_sequencing_groups()[0]
    test_none = cohort.get_sequencing_groups()[1]
    # test_exome = cohort.get_sequencing_groups()[2]

    # Test reads
    # TODO: This code returns error: Value of type "AlignmentInput" is not indexable
    # assert test_genome.alignment_input_by_seq_type['genome'][0].r1 == CloudPath(
    #     'gs://cpg-fewgenomes-main/HG3FMDSX3_2_220405_FS28_Homo-sapiens_AACGAGGCCG-ATCCAGGTAT_R_220208_BINKAN1_FEWGENOMES_M001_R1.fastq.gz'
    # )
    # assert test_exome.alignment_input_by_seq_type['exome'][0].r1 == CloudPath(
    #     'gs://cpg-fewgenomes-main/exomeexample_r1.fastq.gz'
    # )

    # TODO: check expected output
    assert test_none.alignment_input is None
    assert re.search(
        r'WARNING\s+cpg_flow\.inputs:inputs\.py:\d+\s+No reads found for sequencing group CPGbbb of type genome',
        caplog.text,
    )


def test_unknown_data(mocker: MockFixture, tmp_path, caplog):
    mocker.patch('cpg_flow.utils.exists_not_cached', lambda *args: True)

    caplog.set_level(logging.WARNING)
    set_config(_cohort_config(tmp_path, ['COH4']), tmp_path / 'config.toml')

    mocker.patch('cpg_flow.metamist.Metamist.get_ped_entries', mock_get_pedigree_empty)

    mocker.patch(
        'cpg_flow.metamist.Metamist.get_sg_entries',
        mock_get_cohort_sgs('COH3'),
    )
    mocker.patch('cpg_flow.metamist.Metamist.get_analyses_by_sgid', mock_get_analysis_by_sgs)

    mocker.patch('cpg_flow.inputs.get_cohort_sgs', mock_get_cohort_sgs)

    from cpg_flow.inputs import get_multicohort
    from cpg_flow.targets import Sex

    cohort = get_multicohort()

    test_female = cohort.get_sequencing_groups()[0]

    test_unknown = cohort.get_sequencing_groups()[1]

    assert test_female.pedigree.sex == Sex.FEMALE
    assert test_unknown.pedigree.sex == Sex.UNKNOWN


def test_custom_cohort(mocker: MockFixture, tmp_path, monkeypatch):
    """
    Testing creating a Cohort object from metamist mocks.
    """
    set_config(_custom_cohort_config(tmp_path), tmp_path / 'config.toml')

    mocker.patch('cpg_flow.utils.exists_not_cached', lambda *args: False)

    mocker.patch('cpg_flow.metamist.Metamist.get_ped_entries', mock_get_pedigree)
    mocker.patch('cpg_flow.metamist.Metamist.get_analyses_by_sgid', mock_get_analysis_by_sgs)

    def mock_query(query, variables):
        # Mocking the return value of the query function
        data = mock_get_cohort_sgs('COH5')
        return {
            'cohorts': [
                {
                    'name': data.get('name'),
                    'status': data.get('status'),
                    'project': {'dataset': data.get('dataset')},
                    'sequencingGroups': data.get('sequencing_groups'),
                },
            ],
        }

    monkeypatch.setattr('cpg_flow.metamist.query', mock_query)

    from cpg_flow.inputs import get_multicohort

    multicohort = get_multicohort()

    assert multicohort
    assert isinstance(multicohort, MultiCohort)

    # Testing Cohort Information
    assert len(multicohort.get_sequencing_groups()) == 2
    assert sorted(multicohort.get_sequencing_group_ids()) == ['CPGAAAA', 'CPGXXXX']

    # Test the projects they belong to
    ds_map = {'CPGAAAA': 'projectb', 'CPGXXXX': 'projecta'}
    for sg in multicohort.get_sequencing_groups():
        assert sg.dataset.name == ds_map[sg.id]
