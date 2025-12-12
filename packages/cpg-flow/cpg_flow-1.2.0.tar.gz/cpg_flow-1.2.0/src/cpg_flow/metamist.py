"""
Helpers to communicate with the metamist database.
"""

import pprint
import traceback
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from gql.transport.exceptions import TransportServerError
from loguru import logger
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from cpg_flow.filetypes import AlignmentInput, BamPath, CramPath, FastqOraPair, FastqPair, FastqPairs
from cpg_flow.utils import exists
from cpg_utils import Path, to_path
from cpg_utils.config import config_retrieve, get_config
from metamist import models
from metamist.apis import AnalysisApi
from metamist.exceptions import ApiException, ServiceException
from metamist.graphql import gql, query

GET_SEQUENCING_GROUPS_QUERY = gql(
    """
        query SGQuery($metamist_proj: String!, $only_sgs: [String!]!, $skip_sgs: [String!]!, $sequencing_type: String!){
            project(name: $metamist_proj) {
                sequencingGroups(id: { in_: $only_sgs, nin: $skip_sgs}, type:  {eq: $sequencing_type}) {
                    id
                    meta
                    platform
                    technology
                    type
                    sample {
                        externalId
                        participant {
                            id
                            externalId
                            phenotypes
                            reportedSex
                            meta
                        }
                    }
                    assays {
                        id
                        meta
                        type
                    }
                }
            }
        }
        """,
)

GET_SEQUENCING_GROUPS_BY_COHORT_QUERY = gql(
    """
    query SGByCohortQuery($cohort_id: String!) {
        cohorts(id: {eq: $cohort_id}) {
            name
            status
            project {
                dataset
            }
            sequencingGroups {
                id
                meta
                platform
                technology
                type
                sample {
                    project {
                        name
                    }
                    externalId
                    participant {
                        id
                        externalId
                        phenotypes
                        reportedSex
                        meta
                    }
                }
                assays {
                    id
                    meta
                    type
                }
            }
        }
    }
    """,
)


GET_ANALYSES_QUERY = gql(
    """
        query AnalysesQuery($metamist_proj: String!, $analysis_type: String!, $analysis_status: AnalysisStatus!) {
            project(name: $metamist_proj) {
                analyses (active: {eq: true}, type: {eq: $analysis_type}, status: {eq: $analysis_status}) {
                    id
                    type
                    meta
                    output
                    status
                    sequencingGroups {
                        id
                    }
                }
            }
        }
        """,
)

GET_PEDIGREE_QUERY = gql(
    """
        query PedigreeQuery($metamist_proj: String!){
            project(name: $metamist_proj) {
                pedigree(replaceWithFamilyExternalIds: false)
            }
        }
    """,
)

SUPPORTED_READ_TYPES = {'bam', 'cram', 'fastq', 'fastq_ora'}

_metamist: Optional['Metamist'] = None


def get_metamist() -> 'Metamist':
    """Return the cohort object"""
    global _metamist
    if not _metamist:
        _metamist = Metamist()
    return _metamist


class MetamistError(Exception):
    """
    Error while interacting with Metamist.
    """


class AnalysisStatus(Enum):
    """
    Corresponds to metamist Analysis statuses:
    https://github.com/populationgenomics/sample-metadata/blob/dev/models/enums/analysis.py#L14-L21
    """

    QUEUED = 'queued'
    IN_PROGRESS = 'in-progress'
    FAILED = 'failed'
    COMPLETED = 'completed'
    UNKNOWN = 'unknown'

    @staticmethod
    def parse(name: str) -> 'AnalysisStatus':
        """
        Parse str and create a AnalysisStatus object
        """
        return {v.value: v for v in AnalysisStatus}[name.lower()]


class AnalysisType(Enum):
    """
    Corresponds to metamist Analysis types:
    https://github.com/populationgenomics/sample-metadata/blob/dev/models/enums
    /analysis.py#L4-L11

    Re-defined in a separate module to decouple from the main metamist module,
    so decorators can use `@stage(analysis_type=AnalysisType.QC)` without importing
    the metamist package.
    """

    QC = 'qc'
    JOINT_CALLING = 'joint-calling'
    GVCF = 'gvcf'
    CRAM = 'cram'
    MITO_CRAM = 'mito-cram'
    CUSTOM = 'custom'
    ES_INDEX = 'es-index'
    COMBINER = 'combiner'

    @staticmethod
    def parse(val: str) -> 'AnalysisType':
        """
        Parse str and create a AnalysisStatus object
        """
        d = {v.value: v for v in AnalysisType}
        if val not in d:
            raise MetamistError(
                f'Unrecognised analysis type {val}. Available: {list(d.keys())}',
            )
        return d[val.lower()]


@dataclass
class Analysis:
    """
    Metamist DB Analysis entry.

    See the metamist package for more details:
    https://github.com/populationgenomics/sample-metadata
    """

    id: int
    type: AnalysisType
    status: AnalysisStatus
    sequencing_group_ids: set[str]
    output: Path | None
    meta: dict

    @staticmethod
    def parse(data: dict) -> 'Analysis':
        """
        Parse data to create an Analysis object.
        """
        req_keys = ['id', 'type', 'status']
        if any(k not in data for k in req_keys):
            for key in req_keys:
                if key not in data:
                    logger.error(f'"Analysis" data does not have {key}: {data}')
            raise ValueError(f'Cannot parse metamist Sequence {data}')

        output = data.get('output')
        if output:
            output = to_path(output)

        a = Analysis(
            id=int(data['id']),
            type=AnalysisType.parse(data['type']),
            status=AnalysisStatus.parse(data['status']),
            sequencing_group_ids=set([s['id'] for s in data['sequencingGroups']]),
            output=output,
            meta=data.get('meta') or {},
        )
        return a


class Metamist:
    """
    Communication with metamist.
    """

    def __init__(self) -> None:
        self.default_dataset: str = get_config()['workflow']['dataset']
        self.aapi = AnalysisApi()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=3, min=8, max=30),
        retry=retry_if_exception_type(ServiceException),
        reraise=True,
    )
    def make_retry_aapi_call(self, api_func: Callable, **kwargv: Any):  # noqa: PLR6301
        """
        Make a generic API call to self.aapi with retries.
        Retry only if ServiceException is thrown

        TODO: How many retries?
        e.g. try 3 times, wait 2^3: 8, 16, 24 seconds
        """
        try:
            return api_func(**kwargv)
        except ServiceException:
            # raise here so the retry occurs
            logger.warning(
                f'Retrying {api_func} ...',
            )
            raise

    def make_aapi_call(self, api_func: Callable, **kwargv: Any):
        """
        Make a generic API call to self.aapi.
        This is a wrapper around retry of API call to handle exceptions and logger.
        """
        try:
            return self.make_retry_aapi_call(api_func, **kwargv)
        except (ServiceException, ApiException) as e:
            # Metamist API failed even after retries
            # log the error and continue
            traceback.print_exc()
            logger.error(
                f'Error: {e} Call {api_func} failed with payload:\n{kwargv!s}',
            )
        # TODO: discuss should we catch all here as well?
        # except Exception as e:
        #     # Other exceptions?

        return None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=3, min=8, max=30),
        retry=retry_if_exception_type(TransportServerError),
        reraise=True,
    )
    def get_sg_entries(self, dataset_name: str) -> list[dict]:
        """
        Retrieve sequencing group entries for a dataset, in the context of access level
        and filtering options.
        """
        metamist_proj = self.get_metamist_proj(dataset_name)
        logger.info(f'Getting sequencing groups for dataset {metamist_proj}')

        skip_sgs = get_config()['workflow'].get('skip_sgs', [])
        only_sgs = get_config()['workflow'].get('only_sgs', [])
        sequencing_type = get_config()['workflow'].get('sequencing_type')

        if only_sgs and skip_sgs:
            raise MetamistError('Cannot specify both only_sgs and skip_sgs in config')

        sequencing_group_entries = query(
            GET_SEQUENCING_GROUPS_QUERY,
            variables={
                'metamist_proj': metamist_proj,
                'only_sgs': only_sgs,
                'skip_sgs': skip_sgs,
                'sequencing_type': sequencing_type,
            },
        )

        return sequencing_group_entries['project']['sequencingGroups']

    def update_analysis(self, analysis: Analysis, status: AnalysisStatus):
        """
        Update "status" of an Analysis entry.
        """
        self.make_aapi_call(
            self.aapi.update_analysis,
            analysis_id=analysis.id,
            analysis_update_model=models.AnalysisUpdateModel(
                status=models.AnalysisStatus(status.value),
            ),
        )
        # Keeping this as is for compatibility with the existing code
        # However this should only be set after the API call is successful
        analysis.status = status

    # TODO: Refactor based on correct usage
    def get_analyses_by_sgid(
        self,
        analysis_type: AnalysisType,
        analysis_status: AnalysisStatus = AnalysisStatus.COMPLETED,
        dataset: str | None = None,
    ) -> dict[str, Analysis]:
        """
        Query the DB to find the last completed analysis for the type, sequencing group ids,
        and sequencing type, one Analysis object per sequencing group. Assumes the analysis
        is defined for a single sequencing group (that is, analysis_type=cram|gvcf|qc).
        """
        metamist_proj = self.get_metamist_proj(dataset)

        analyses = query(
            GET_ANALYSES_QUERY,
            variables={
                'metamist_proj': metamist_proj,
                'analysis_type': analysis_type.value,
                'analysis_status': analysis_status.name,
            },
        )

        analysis_per_sid: dict[str, Analysis] = dict()

        for analysis in analyses['project']['analyses']:
            a = Analysis.parse(analysis)
            if not a:
                continue

            assert a.status == analysis_status, analysis
            assert a.type == analysis_type, analysis
            if len(a.sequencing_group_ids) < 1:
                logger.warning(f'Analysis has no sequencing group ids. {analysis}')
                continue

            assert len(a.sequencing_group_ids) == 1, analysis
            analysis_per_sid[list(a.sequencing_group_ids)[0]] = a

        logger.info(
            f'Querying {analysis_type} analysis entries for {metamist_proj}: found {len(analysis_per_sid)}',
        )
        return analysis_per_sid

    def create_analysis(  # noqa: PLR0917
        self,
        output: Path | str,
        type_: str | AnalysisType,
        status: str | AnalysisStatus,
        cohort_ids: list[str] | None = None,
        sequencing_group_ids: list[str] | None = None,
        dataset: str | None = None,
        meta: dict | None = None,
    ) -> int | None:
        """
        Tries to create an Analysis entry, returns its id if successful.
        """
        metamist_proj = self.get_metamist_proj(dataset)

        if isinstance(type_, AnalysisType):
            type_ = type_.value
        if isinstance(status, AnalysisStatus):
            status = status.value

        if not cohort_ids:
            cohort_ids = []

        if not sequencing_group_ids:
            sequencing_group_ids = []

        am = models.Analysis(
            type=type_,
            status=models.AnalysisStatus(status),
            output=str(output),
            cohort_ids=list(cohort_ids),
            sequencing_group_ids=list(sequencing_group_ids),
            meta=meta or {},
        )
        aid = self.make_aapi_call(
            self.aapi.create_analysis,
            project=metamist_proj,
            analysis=am,
        )
        if aid is None:
            logger.error(
                f'Failed to create Analysis(type={type_}, status={status}, output={output!s}) in {metamist_proj}',
            )
            return None
        logger.info(
            f'Created Analysis(id={aid}, type={type_}, status={status}, output={output!s}) in {metamist_proj}',
        )
        return aid

    def get_ped_entries(self, dataset: str | None = None) -> list[dict[str, str]]:
        """
        Retrieve PED lines for a specified SM project, with external participant IDs.
        """
        metamist_proj = self.get_metamist_proj(dataset)
        entries = query(GET_PEDIGREE_QUERY, variables={'metamist_proj': metamist_proj})

        pedigree_entries = entries['project']['pedigree']

        return pedigree_entries

    def get_metamist_proj(self, dataset: str | None = None) -> str:
        """
        Return the Metamist project name, appending '-test' if the access level is 'test'.
        """
        metamist_proj = dataset or self.default_dataset
        if config_retrieve(['workflow', 'access_level']) == 'test' and not metamist_proj.endswith('-test'):
            metamist_proj += '-test'

        return metamist_proj


@dataclass
class Assay:
    """
    Metamist "Assay" entry.

    See metamist for more details:
    https://github.com/populationgenomics/sample-metadata
    """

    id: str
    sequencing_group_id: str
    meta: dict
    assay_type: str
    alignment_input: AlignmentInput | None = None

    @staticmethod
    def parse(
        data: dict,
        sg_id: str,
        check_existence: bool = False,
        run_parse_reads: bool = True,
    ) -> 'Assay':
        """
        Create from a dictionary.
        """

        assay_keys = ['id', 'type', 'meta']
        missing_keys = [key for key in assay_keys if data.get(key) is None]

        if missing_keys:
            raise ValueError(
                f'Cannot parse metamist Sequence {data}. Missing keys: {missing_keys}',
            )

        assay_type = str(data['type'])
        assert assay_type, data
        mm_seq = Assay(
            id=str(data['id']),
            sequencing_group_id=sg_id,
            meta=data['meta'],
            assay_type=assay_type,
        )
        if run_parse_reads:
            mm_seq.alignment_input = parse_reads(
                sequencing_group_id=sg_id,
                assay_meta=data['meta'],
                check_existence=check_existence,
            )
        return mm_seq


def get_cohort_sgs(cohort_id: str) -> dict:
    """
    Retrieve sequencing group entries for a single cohort.
    """
    logger.info(f'Getting sequencing groups for cohort {cohort_id}')
    entries = query(GET_SEQUENCING_GROUPS_BY_COHORT_QUERY, {'cohort_id': cohort_id})

    # Create dictionary keying sequencing groups by project and including cohort name
    # {
    #     "sequencing_groups": {
    #         project_id: [sequencing_group_1, sequencing_group_2, ...],
    #         ...
    #     },
    #     "name": "CohortName"
    #     "dataset": "DatasetName"
    # }

    if len(entries['cohorts']) != 1:
        raise MetamistError('We only support one cohort at a time currently')

    if entries.get('data') is None and 'errors' in entries:
        message = entries['errors'][0]['message']
        raise MetamistError(f'Error fetching cohort: {message}')

    cohort_status = entries['cohorts'][0]['status']
    if cohort_status.lower() != 'active':  # support upper and lower formats during migration
        raise MetamistError(
            f'Cohort {cohort_id} is {cohort_status}. Only active cohorts are allowed. Please check the input cohort list.'
        )

    cohort_name = entries['cohorts'][0]['name']
    cohort_dataset = entries['cohorts'][0]['project']['dataset']
    sequencing_groups = entries['cohorts'][0]['sequencingGroups']

    return {
        'name': cohort_name,
        'dataset': cohort_dataset,
        'sequencing_groups': sequencing_groups,
    }


def parse_reads(
    sequencing_group_id: str,
    assay_meta: dict,
    check_existence: bool,
) -> AlignmentInput:
    """
    Parse a AlignmentInput object from the meta dictionary.
    `check_existence`: check if fastq/crams exist on buckets.
    Default value is pulled from self.metamist and can be overridden.
    """
    reads_data = assay_meta.get('reads')
    reads_type = assay_meta.get('reads_type')
    reference_assembly = assay_meta.get('reference_assembly', {}).get('location')

    if not reads_data:
        raise MetamistError(f'{sequencing_group_id}: no "meta/reads" field in meta')

    if not reads_type:
        raise MetamistError(
            f'{sequencing_group_id}: no "meta/reads_type" field in meta',
        )

    if reads_type in {'bam', 'cram'} and len(reads_data) > 1:
        raise MetamistError(
            f'{sequencing_group_id}: supporting only single bam/cram input',
        )

    if reads_type not in SUPPORTED_READ_TYPES:
        raise MetamistError(
            f'{sequencing_group_id}: ERROR: "reads_type" is expected to be one of {sorted(SUPPORTED_READ_TYPES)}',
        )

    if reads_type in {'bam', 'cram'}:
        return find_cram_or_bam(
            reads_data,
            sequencing_group_id,
            check_existence,
            reference_assembly,
            access_level=config_retrieve(['workflow', 'access_level']),
        )

    # special handling case for FQ.ora files, these require a reference for decompression
    elif reads_type == 'fastq_ora':
        if (ora_reference := assay_meta.get('ora_reference')) is None or (
            reference_location := ora_reference.get('location')
        ) is None:
            raise MetamistError(f'"meta.ora_reference.location" is mandatory for {reads_type} assays: \n{assay_meta}')
        return find_fastqs(reads_data, sequencing_group_id, check_existence, read_reference=reference_location)

    else:
        return find_fastqs(reads_data, sequencing_group_id, check_existence)


def find_fastqs(
    reads_data: list[dict],
    sequencing_group_id: str,
    check_existence: bool,
    read_reference: str | None = None,
) -> FastqPairs:
    """
    Generates FastqPairs objects. This method handles component FastqPair objects or ORA or FQ type.
    Objects are assumed to be ORA if we are generating FastqPairs and passing a reference for decompression.
    """
    fastq_pairs = FastqPairs()

    for lane_pair in reads_data:
        if len(lane_pair) != 2:
            raise ValueError(
                f'Sequence data for sequencing group {sequencing_group_id} is incorrectly '
                f'formatted. Expecting 2 entries per lane (R1 and R2 fastqs), '
                f'but got {len(lane_pair)}. '
                f'Read data: {pprint.pformat(lane_pair)}',
            )
        r1_file = lane_pair[0]['location']
        r2_file = lane_pair[1]['location']

        if check_existence and not exists(r1_file):
            raise MetamistError(
                f'{sequencing_group_id}: ERROR: read 1 file does not exist: {r1_file}',
            )
        if check_existence and not exists(r2_file):
            raise MetamistError(
                f'{sequencing_group_id}: ERROR: read 2 file does not exist: {r2_file}',
            )

        if read_reference is not None:
            fastq_pairs.append(
                FastqOraPair(
                    to_path(r1_file),
                    to_path(r2_file),
                    read_reference,
                ),
            )
        else:
            fastq_pairs.append(
                FastqPair(
                    to_path(r1_file),
                    to_path(r2_file),
                ),
            )

    return fastq_pairs


def update_location(location: str, access_level: str | None) -> str:
    if access_level == 'test':
        return location.replace('-main-upload/', '-test-upload/')
    return location


def find_cram_or_bam(
    reads_data: list[dict],
    sequencing_group_id: str,
    check_existence: bool,
    reference_assembly: Path | None = None,
    access_level: str | None = None,
) -> AlignmentInput:
    CRAM_EXT = '.cram'
    BAM_EXT = '.bam'
    CRAM_INDEX_EXT = '.crai'
    BAM_INDEX_EXT = '.bai'

    assert len(reads_data) == 1, f'{sequencing_group_id}: expected only one entry for bam/cram, got {len(reads_data)}'
    file = reads_data[0]
    location = update_location(file['location'], access_level)

    if not (location.endswith(CRAM_EXT) or location.endswith(BAM_EXT)):
        raise MetamistError(
            f'{sequencing_group_id}: ERROR: expected the file to have an extension .cram or .bam, got: {location}',
        )

    if check_existence and not exists(location):
        raise MetamistError(
            f'{sequencing_group_id}: ERROR: index file does not exist: {location}',
        )

    # Index:
    index_location = None
    if file.get('secondaryFiles'):
        index_location = update_location(file['secondaryFiles'][0]['location'], access_level)

        if (location.endswith(CRAM_EXT) and not index_location.endswith(CRAM_INDEX_EXT)) or (
            location.endswith(BAM_EXT) and not index_location.endswith(BAM_INDEX_EXT)
        ):
            raise MetamistError(
                f'{sequencing_group_id}: ERROR: expected the index file to have an extension '
                f'.crai or .bai, got: {index_location}',
            )

        if check_existence and not exists(index_location):
            raise MetamistError(
                f'{sequencing_group_id}: ERROR: index file does not exist: {index_location}',
            )

    if location.endswith(CRAM_EXT):
        return CramPath(
            location,
            index_path=index_location,
            reference_assembly=reference_assembly,
        )

    assert location.endswith(BAM_EXT)
    return BamPath(location, index_path=index_location)
