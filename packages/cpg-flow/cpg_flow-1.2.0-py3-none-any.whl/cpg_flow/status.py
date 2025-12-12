"""
Metamist wrapper to report analysis progress.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable

from hailtop.batch import Batch
from hailtop.batch.job import Job

from cpg_flow.metamist import AnalysisStatus, get_metamist
from cpg_flow.targets import Target
from cpg_flow.targets.cohort import Cohort
from cpg_flow.targets.multicohort import MultiCohort
from cpg_utils import to_path
from cpg_utils.config import get_config


def complete_analysis_job(  # noqa: PLR0917
    output: str,
    analysis_type: str,
    cohort_ids: list[str],
    sg_ids: list[str],
    project_name: str,
    meta: dict,
    update_analysis_meta: Callable | None = None,
    tolerate_missing: bool = False,
):
    """
    a job to be called within the batch as a pythonJob
    this will register the analysis outputs from a Stage

    Args:
        output (str): path to the output file
        analysis_type (str): metamist analysis type
        sg_ids (list[str]): all CPG IDs relevant to this target
        project_name (str): project/dataset name
        meta (dict): any metadata to add
        update_analysis_meta (Callable | None): function to update analysis meta
        tolerate_missing (bool): if True, allow missing output
    """

    assert isinstance(output, str)
    output_cloudpath = to_path(output)

    if update_analysis_meta is not None:
        meta |= update_analysis_meta(output)

    # if SG IDs are listed in the meta, remove them
    # these are already captured in the sg_ids list
    meta.pop('sequencing_groups', None)

    # if the meta has a remove_sgids key, we need to remove those from the list
    # this occurs when samples are soft-filtered from joint-calls in a way that
    # doesn't percolate through to the dataset/cohorts
    # removal here prevents results being registered for samples that were omitted
    if 'remove_sgids' in meta and to_path(meta['remove_sgids']).exists():
        with to_path(meta['remove_sgids']).open() as f:
            exclusion_ids = set(f.read().splitlines())
            print(f'removing {len(exclusion_ids)} samples from analysis')
            print(f'samples for removal: {", ".join(exclusion_ids)}')
            sg_ids = [sg for sg in sg_ids if sg not in exclusion_ids]

    # we know that es indexes are registered names, not files/dirs
    # skip all relevant checks for this output type
    if analysis_type != 'es-index':
        if not output_cloudpath.exists():
            if tolerate_missing:
                print(f"Output {output} doesn't exist, allowing silent return")
                return
            raise ValueError(f"Output {output} doesn't exist")

        # add file size to meta
        if not output_cloudpath.is_dir():
            meta |= {'size': output_cloudpath.stat().st_size}

    a_id = get_metamist().create_analysis(
        output=output,
        type_=analysis_type,
        status=AnalysisStatus('completed'),
        cohort_ids=cohort_ids,
        sequencing_group_ids=sg_ids,
        dataset=project_name,
        meta=meta,
    )
    if a_id is None:
        msg = f'Creation of Analysis failed (type={analysis_type}, output={output}) in {project_name}'
        print(msg)
        raise ConnectionError(msg)
    print(
        f'Created Analysis(id={a_id}, type={analysis_type}, output={output}) in {project_name}',
    )


class StatusReporterError(Exception):
    """
    Error thrown by StatusReporter.
    """


class StatusReporter(ABC):
    """
    Status reporter
    """

    @abstractmethod
    def create_analysis(  # noqa: PLR0917
        self,
        b: Batch,
        output: str,
        analysis_type: str,
        target: Target,
        jobs: list[Job] | None = None,
        job_attr: dict | None = None,
        meta: dict | None = None,
        update_analysis_meta: Callable | None = None,
        tolerate_missing_output: bool = False,
        project_name: str | None = None,
    ):
        """
        Record analysis entry.
        """


class MetamistStatusReporter(StatusReporter):
    """
    Job status reporter. Works through creating metamist Analysis entries.
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def create_analysis(  # noqa: PLR0917
        b: Batch,
        output: str,
        analysis_type: str,
        target: Target,
        jobs: list[Job] | None = None,
        job_attr: dict | None = None,
        meta: dict | None = None,
        update_analysis_meta: Callable | None = None,
        tolerate_missing_output: bool = False,
        project_name: str | None = None,
    ):
        """
        Create completed analysis job
        """

        # no jobs means no output, so no need to create analysis
        if not jobs:
            return

        if meta is None:
            meta = {}

        # find all relevant SG IDs
        # Currently this implementation will only return sg ids or cohort ids
        # The other list of ids will be empty
        # It is unclear if metamist would accept both list of ids and succeed
        cohort_ids = []
        sequencing_group_ids = []
        if target is None:
            raise ValueError('Target is required to create analysis')
        if isinstance(target, MultiCohort):
            cohort_ids = target.get_cohort_ids()
        elif isinstance(target, Cohort):
            cohort_ids = [target.get_cohort_id()]
        else:
            sequencing_group_ids = target.get_sequencing_group_ids()

        py_job = b.new_python_job(
            f'Register analysis output {output}',
            job_attr or {} | {'tool': 'metamist'},
        )
        py_job.image(get_config()['workflow']['driver_image'])
        py_job.call(
            complete_analysis_job,
            str(output),
            analysis_type,
            cohort_ids,
            sequencing_group_ids,
            project_name,
            meta,
            update_analysis_meta,
            tolerate_missing_output,
        )

        py_job.depends_on(*jobs)
