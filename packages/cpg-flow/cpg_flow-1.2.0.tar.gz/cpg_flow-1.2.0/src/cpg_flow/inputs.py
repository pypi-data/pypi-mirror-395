"""
Metamist wrapper to get input sequencing groups.
"""

from functools import cache

from loguru import logger

from cpg_flow.filetypes import CramPath, GvcfPath
from cpg_flow.metamist import (
    AnalysisType,
    Assay,
    MetamistError,
    get_cohort_sgs,
    get_metamist,
    parse_reads,
)
from cpg_flow.targets import Dataset, MultiCohort, PedigreeInfo, SequencingGroup, Sex
from cpg_flow.utils import exists
from cpg_utils.config import config_retrieve, update_dict


def add_sg_to_dataset(dataset: Dataset, sg_data: dict) -> SequencingGroup:
    """
    Adds a sequencing group to a dataset.

    Args:
        dataset (Dataset): Dataset to insert the SequencingGroup into
        sg_data (dict): data from the metamist API

    Returns:
        The SequencingGroup object
    """
    # TODO: The update_dict calls are a bit of a hack, we should be able to do this in a cleaner way
    # scavenge all the metadata from the SG dict (SG/Sample/Participant)
    metadata = sg_data.get('meta', {})
    update_dict(metadata, sg_data['sample']['participant'].get('meta', {}))

    # phenotypes are managed badly here, need a cleaner way to get them into the SG
    update_dict(
        metadata,
        {'phenotypes': sg_data['sample']['participant'].get('phenotypes', {})},
    )

    # create a SequencingGroup object from its component parts
    sequencing_group = dataset.add_sequencing_group(
        id=str(sg_data['id']),
        external_id=str(sg_data['sample']['externalId']),
        participant_id=sg_data['sample']['participant'].get('externalId'),
        meta=metadata,
        sequencing_type=sg_data['type'],
        sequencing_technology=sg_data['technology'],
        sequencing_platform=sg_data['platform'],
    )

    if reported_sex := sg_data['sample']['participant'].get('reportedSex'):
        sequencing_group.pedigree.sex = Sex.parse(reported_sex)

    # parse the assays and related dict content
    if config_retrieve(['workflow', 'populate_assays'], None):
        _populate_assays(sequencing_group, sg_data)

    return sequencing_group


# NOTE: This function could be considered for merging with
# create_multicohort in future since we only ever create effectively a
# single multicohort object in the workflow.
# For now, we keep them separate to keep code clean and readable.
def get_multicohort() -> MultiCohort:
    """
    Return the cohort or multicohort object based on the workflow configuration.
    """
    input_datasets = config_retrieve(['workflow', 'input_datasets'], None)

    # pull the list of cohort IDs from the config
    custom_cohort_ids = config_retrieve(['workflow', 'input_cohorts'], None)

    if input_datasets:
        raise ValueError('Argument input_datasets is deprecated, use input_cohorts instead')

    if isinstance(custom_cohort_ids, list) and len(custom_cohort_ids) <= 0:
        raise ValueError('No custom_cohort_ids found in the config')

    # NOTE: When configuring sgs in the config is deprecated, this will be removed.
    if custom_cohort_ids and not isinstance(custom_cohort_ids, list):
        raise ValueError('Argument input_cohorts must be a list')

    # After the check for no cusotom_cohort_ids in the config convert
    # to a tuple for the cache decorator
    custom_cohort_ids = tuple() if not custom_cohort_ids else tuple(custom_cohort_ids)

    return create_multicohort(custom_cohort_ids)


# This will cache the result of create_multicohort given an identical
# custom_cohort_ids list. This is useful when we want to reuse the
# multicohort object in multiple places without having to recreate it.
# This reduces the overall number of calls to the Metamist API
@cache
def create_multicohort(custom_cohort_ids: tuple[str]) -> MultiCohort:
    """
    Add cohorts in the multicohort.
    """
    # get a unique set of cohort IDs
    custom_cohort_ids_unique = sorted(set(custom_cohort_ids))
    custom_cohort_ids_removed = sorted(set(custom_cohort_ids) - set(custom_cohort_ids_unique))

    # if any cohort id duplicates were removed we log them
    if len(custom_cohort_ids_unique) != len(custom_cohort_ids):
        logger.warning(
            f'Removed {len(custom_cohort_ids_removed)} non-unique cohort IDs',
        )
        duplicated_cohort_ids = ', '.join(custom_cohort_ids_removed)
        logger.warning(f'Non-unique cohort IDs: {duplicated_cohort_ids}')

    multicohort = MultiCohort()

    # for each Cohort ID
    for cohort_id in custom_cohort_ids_unique:
        # get the dictionary representation of all SGs in this cohort
        # dataset_id is sequencing_group_dict['sample']['project']['name']
        cohort_sg_dict = get_cohort_sgs(cohort_id)
        cohort_name = cohort_sg_dict.get('name', cohort_id)
        cohort_dataset = cohort_sg_dict.get('dataset', None)
        cohort_sgs = cohort_sg_dict.get('sequencing_groups', [])

        if len(cohort_sgs) == 0:
            raise MetamistError(f'Cohort {cohort_id} has no sequencing groups')

        # create a new Cohort object
        cohort = multicohort.create_cohort(
            id=cohort_id,
            name=cohort_name,
            dataset=cohort_dataset,
        )

        # first populate these SGs into their Datasets
        # required so that the SG objects can be referenced in the collective Datasets
        # SG.dataset.prefix is meaningful, to correctly store outputs in the project location
        for entry in cohort_sgs:
            sg_dataset = entry['sample']['project']['name']
            dataset = multicohort.create_dataset(sg_dataset.removesuffix('-test'))

            sequencing_group = add_sg_to_dataset(dataset, entry)

            # also add the same sequencing group to the cohort
            cohort.add_sequencing_group_object(sequencing_group)

    # we've populated all the sequencing groups in the cohorts and datasets
    # all SequencingGroup objects should be populated uniquely (pointers to instances, so updating Analysis entries
    # for each SG should update both the Dataset's version and the Cohort's version)

    # only go to metamist once per dataset to get analysis entries
    for dataset in multicohort.get_datasets():
        _populate_analysis(dataset)
        if config_retrieve(['workflow', 'read_pedigree'], True):
            _populate_pedigree(dataset)

    return multicohort


def _combine_assay_meta(assays: list[Assay]) -> dict:
    """
    Combine assay meta from multiple assays
    """
    assays_meta: dict = {}
    for assay in assays:
        for key, value in assay.meta.items():
            if key == 'reads':
                assays_meta.setdefault(key, []).append(value)
            else:
                assays_meta[key] = value
    return assays_meta


def _populate_assays(
    sequencing_group: SequencingGroup,
    entry: dict,
    check_existence: bool = False,
) -> None:
    """
    Populate assay inputs for a sequencing group
    """
    assays: list[Assay] = []

    for assay in entry.get('assays', []):
        entry_assay = Assay.parse(assay, sequencing_group.id, run_parse_reads=False)
        assays.append(entry_assay)

    sequencing_group.assays = tuple(assays)

    if len(assays) > 1:
        entry_assay_meta = _combine_assay_meta(assays)
    else:
        entry_assay_meta = assays[0].meta
        if _reads := entry_assay_meta.get('reads'):
            entry_assay_meta['reads'] = [_reads]

    if entry_assay_meta.get('reads'):
        alignment_input = parse_reads(
            sequencing_group_id=sequencing_group.id,
            assay_meta=entry_assay_meta,
            check_existence=check_existence,
        )
        sequencing_group.alignment_input = alignment_input
    else:
        logger.warning(
            f'No reads found for sequencing group {sequencing_group.id} of type {entry["type"]}',
        )


def _populate_analysis(dataset: Dataset) -> None:
    """
    Populate Analysis entries.
    """
    gvcf_by_sgid = get_metamist().get_analyses_by_sgid(
        analysis_type=AnalysisType.GVCF,
        dataset=dataset.name,
    )
    cram_by_sgid = get_metamist().get_analyses_by_sgid(
        analysis_type=AnalysisType.CRAM,
        dataset=dataset.name,
    )

    for sequencing_group in dataset.get_sequencing_groups():
        if (analysis := gvcf_by_sgid.get(sequencing_group.id)) and analysis.output:
            # assert file exists
            assert exists(analysis.output), (
                'gvcf file does not exist',
                analysis.output,
            )
            sequencing_group.gvcf = GvcfPath(path=analysis.output)
        elif exists(sequencing_group.make_gvcf_path()):
            logger.warning(
                f'We found a gvcf file in the expected location {sequencing_group.make_gvcf_path()},'
                'but it is not logged in metamist. Skipping. You may want to update the metadata and try again. ',
            )
        if (analysis := cram_by_sgid.get(sequencing_group.id)) and analysis.output:
            # assert file exists
            assert exists(analysis.output), (
                'cram file does not exist',
                analysis.output,
            )
            crai_path = analysis.output.with_suffix('.cram.crai')
            if not exists(crai_path):
                crai_path = None
            sequencing_group.cram = CramPath(analysis.output, crai_path)

        elif exists(sequencing_group.make_cram_path()):
            logger.warning(
                f'We found a cram file in the expected location {sequencing_group.make_cram_path()},'
                'but it is not logged in metamist. Skipping. You may want to update the metadata and try again. ',
            )


def _populate_pedigree(dataset: Dataset) -> None:
    """
    Populate pedigree data for sequencing groups.
    """

    sg_by_participant_id = {}
    for sg in dataset.get_sequencing_groups():
        sg_by_participant_id[sg.participant_id] = sg

    logger.info(f'Reading pedigree for dataset {dataset}')
    ped_entries = get_metamist().get_ped_entries(dataset=dataset.name)
    ped_entry_by_participant_id = {}
    for ped_entry in ped_entries:
        part_id = str(ped_entry['individual_id'])
        ped_entry_by_participant_id[part_id] = ped_entry

    sgids_wo_ped = []
    for sequencing_group in dataset.get_sequencing_groups():
        if sequencing_group.participant_id not in ped_entry_by_participant_id:
            sgids_wo_ped.append(sequencing_group.id)
            continue

        ped_entry = ped_entry_by_participant_id[sequencing_group.participant_id]
        maternal_sg = sg_by_participant_id.get(str(ped_entry['maternal_id']))
        paternal_sg = sg_by_participant_id.get(str(ped_entry['paternal_id']))
        sequencing_group.pedigree = PedigreeInfo(
            sequencing_group=sequencing_group,
            fam_id=ped_entry['family_id'],
            mom=maternal_sg,
            dad=paternal_sg,
            sex=Sex.parse(str(ped_entry['sex'])),
            phenotype=ped_entry['affected'] or '0',
        )
    if sgids_wo_ped:
        logger.warning(
            f'No pedigree data found for {len(sgids_wo_ped)}/{len(dataset.get_sequencing_groups())} sequencing groups',
        )
