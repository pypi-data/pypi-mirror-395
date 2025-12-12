"""
Provides a `Workflow` class and a `@stage` decorator that allow to define workflows
in a declarative fashion.

A `Stage` object is responsible for creating Hail Batch jobs and declaring outputs
(files or metamist analysis objects) that are expected to be produced. Each stage
acts on a `Target`, which can be of the following:

    * SequencingGroup - an individual Sequencing Group (e.g. the CRAM of a single sample)
    * Dataset - a stratification of SGs in this analysis by Metamist Project (e.g. all SGs in acute-care)
    * Cohort - a stratification of SGs in this analysis by Metamist CustomCohort
    * MultiCohort - a union of all SGs in this analysis by Metamist CustomCohort

A `Workflow` object plugs stages together by resolving dependencies between different levels accordingly. Stages are
defined in this package, and chained into Workflows by their inter-Stages dependencies. Workflow names are defined in
main.py, which provides a way to choose a workflow using a CLI argument.
"""

import functools
import os
from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from typing import Any, Generic, Optional, TypeVar, cast, overload

from loguru import logger

from hailtop.batch.job import Job

from cpg_flow.targets import Cohort, Dataset, MultiCohort, SequencingGroup, Target
from cpg_flow.utils import ExpectedResultT, exists
from cpg_flow.workflow import Action, WorkflowError, get_workflow, path_walk
from cpg_utils import Path, to_path
from cpg_utils.config import get_config
from cpg_utils.hail_batch import get_batch

StageDecorator = Callable[..., 'Stage']

# Type variable to use with Generic to make sure a Stage subclass always matches the
# corresponding Target subclass. We can't just use the Target superclass because
# it would violate the Liskov substitution principle (i.e. any Stage subclass would
# have to be able to work on any Target subclass).
TargetT = TypeVar('TargetT', bound=Target)


class StageInputNotFoundError(Exception):
    """
    Thrown when a stage requests input from another stage
    that doesn't exist.
    """


class StageTargetNotFoundError(Exception):
    """
    Thrown when a stage is attempting to get the Path of a target
    that doesn't exist.
    """


# noinspection PyShadowingNames
class StageOutput:
    """
    Represents a result of a specific stage, which was run on a specific target.
    Can be a file path, or a Hail Batch Resource. Optionally wrapped in a dict.
    """

    def __init__(
        self,
        *,
        target: Target,
        data: ExpectedResultT = None,
        jobs: Sequence[Job | None] | Job | None = None,
        meta: dict | None = None,
        reusable: bool = False,
        skipped: bool = False,
        error_msg: str | None = None,
        stage: Optional['Stage'] = None,
    ):
        # Converting str into Path objects.
        self.data: ExpectedResultT = None
        if isinstance(data, str):
            self.data = to_path(data)
        elif isinstance(data, dict):
            self.data = data

            # NOTE: prior Issue #110 we would convert strings to Paths
            # as suggested in an old prod pipes comment.
            # As per discussion in Issue #110, and PR #113 we are
            # reverting this change for now to fix the Cromwell issue.
        else:
            self.data = data

        self.stage = stage
        self.target = target

        if isinstance(jobs, Job):
            self.jobs = [jobs]
        elif jobs is None:
            self.jobs = []
        else:
            self.jobs = [j for j in jobs if j is not None]

        self.meta: dict = meta or {}
        self.reusable = reusable
        self.skipped = skipped
        self.error_msg = error_msg

    def __repr__(self) -> str:
        res = (
            f'StageOutput({self.data}'
            f' target={self.target}'
            f' stage={self.stage}'
            + (' [reusable]' if self.reusable else '')
            + (' [skipped]' if self.skipped else '')
            + (f' [error: {self.error_msg}]' if self.error_msg else '')
            + f' meta={self.meta}'
            + ')'
        )
        return res

    def _get(self, key=None) -> str | Path:
        if self.data is None:
            raise ValueError(f'{self.stage}: output data is not available')

        if key is not None:
            if not isinstance(self.data, dict):
                raise ValueError(
                    f'{self.stage}: {self.data} is not a dictionary, can\'t get "{key}"',
                )
            res = to_path(cast('dict', self.data)[key])
        elif isinstance(self.data, Path):
            res = self.data
        elif isinstance(self.data, str):
            res = to_path(self.data)
        else:
            raise ValueError(f'{self.stage}: {self.data} is not a string or dictionary, can\'t get "{key}"')

        return res

    def as_str(self, key=None) -> str:
        """
        Return the requested value as a simple string.
        The value here can be a String or PathLike, which will be returned as a String
        This is a type change, not a cast
        Args:
            key (str | None): used to extract the value when the result is a dictionary.
        Returns:
            string representation of the value
        """
        res = self._get(key)
        if not isinstance(res, (os.PathLike | str)):
            raise ValueError(f'{res} is not a str or valid Pathlike, will not convert.')
        return str(res)

    def as_path(self, key=None) -> Path:
        """
        Return the result as a Path object.
        This throws an exception when it can't cast.
        `key` is used to extract the value when the result is a dictionary.
        """
        res = self._get(key)
        if not isinstance(res, (os.PathLike | str)):
            raise ValueError(f'{res} is not a path object or a valid String, cannot return as Path.')
        return to_path(res)

    def as_dict(self) -> dict[str, Any]:
        """
        Cast the result to a dictionary, or throw an error if the cast failed.
        """
        if not isinstance(self.data, dict):
            raise ValueError(f'{self.data} is not a dictionary.')

        return self.data


# noinspection PyShadowingNames
class StageInput:
    """
    Represents an input for a stage run. It wraps the outputs of all required upstream
    stages for corresponding targets (e.g. all GVCFs from a GenotypeSample stage
    for a JointCalling stage, along with Hail Batch jobs).

    An object of this class is passed to the public `queue_jobs` method of a Stage,
    and can be used to query dependency files and jobs.
    """

    def __init__(self, stage: 'Stage'):
        self.stage = stage
        self._outputs_by_target_by_stage: dict[str, dict[str, StageOutput | None]] = {}

    def add_other_stage_output(self, output: StageOutput):
        """
        Add output from another stage run.
        """
        assert output.stage is not None, output
        if not output.target.active:
            return
        if not output.target.get_sequencing_groups():
            return
        if not output.data and not output.jobs:
            return
        stage_name = output.stage.name
        target_id = output.target.target_id
        if stage_name not in self._outputs_by_target_by_stage:
            self._outputs_by_target_by_stage[stage_name] = dict()
        self._outputs_by_target_by_stage[stage_name][target_id] = output
        logger.debug(f'Added output from stage_name:{stage_name} for target_id:{target_id} which was {output}')

    def _each(
        self,
        fun: Callable,
        stage: StageDecorator,
    ):
        if stage.__name__ not in [s.name for s in self.stage.required_stages]:
            raise WorkflowError(
                f'{self.stage.name}: getting inputs from stage {stage.__name__}, '
                f'but {stage.__name__} is not listed in required_stages. '
                f'Consider adding it into the decorator: '
                f'@stage(required_stages=[{stage.__name__}])',
            )

        if stage.__name__ not in self._outputs_by_target_by_stage:
            raise WorkflowError(
                f'No inputs from {stage.__name__} for {self.stage.name} found '
                + 'after skipping targets with missing inputs. '
                + (
                    'Check the logs if all sequencing groups were missing inputs from previous '
                    'stages, and consider changing `workflow/first_stage`'
                    if get_config()['workflow'].get('skip_sgs_with_missing_input')
                    else ''
                ),
            )

        return {
            trg: fun(result)
            for trg, result in self._outputs_by_target_by_stage.get(
                stage.__name__,
                {},
            ).items()
        }

    def as_path_by_target(
        self,
        stage: StageDecorator,
        key: str | None = None,
    ) -> dict[str, Path]:
        """
        Get a single file path result, indexed by target for a specific stage
        """
        return self._each(fun=(lambda r: r.as_path(key=key)), stage=stage)

    def as_dict_by_target(self, stage: StageDecorator) -> dict[str, dict[str, Path]]:
        """
        Get as a dict of files/resources for a specific stage, indexed by target
        """
        return self._each(fun=(lambda r: r.as_dict()), stage=stage)

    def as_path_dict_by_target(
        self,
        stage: StageDecorator,
    ) -> dict[str, dict[str, Path]]:
        """
        Get a dict of paths for a specific stage, and indexed by target
        """
        return self._each(fun=(lambda r: r.as_path_dict()), stage=stage)

    def _get(
        self,
        target: Target,
        stage: StageDecorator,
    ):
        if not self._outputs_by_target_by_stage.get(stage.__name__):
            logger.error(f'Available: {self._outputs_by_target_by_stage}, trying to find {stage.__name__}')
            raise StageInputNotFoundError(
                f'Not found output from stage {stage.__name__}, required for stage '
                f'{self.stage.name}. Is {stage.__name__} in the `required_stages`'
                f'decorator? Available: {self._outputs_by_target_by_stage}',
            )
        if not self._outputs_by_target_by_stage[stage.__name__].get(target.target_id):
            logger.error(
                f'Available: {self._outputs_by_target_by_stage[stage.__name__]}, trying to find {target.target_id}',
            )
            raise StageInputNotFoundError(
                f'Not found output for {target} from stage {stage.__name__}, required for stage {self.stage.name}',
            )
        return self._outputs_by_target_by_stage[stage.__name__][target.target_id]

    def as_path(
        self,
        target: Target,
        stage: StageDecorator,
        key: str | None = None,
    ) -> Path:
        """
        Represent as a path to a file, otherwise fail.
        `stage` can be callable, or a subclass of Stage
        """
        res = self._get(target=target, stage=stage)

        if not res:
            raise StageTargetNotFoundError(f'Target "{target}" not found for Stage "{stage}".')

        return res.as_path(key)

    def as_str(
        self,
        target: Target,
        stage: StageDecorator,
        key: str | None = None,
    ) -> str:
        """
        Represent as a simple string, otherwise fail.
        `stage` can be callable, or a subclass of Stage
        """
        res = self._get(target=target, stage=stage)

        if not res:
            raise StageTargetNotFoundError(f'Target "{target}" not found for Stage "{stage}".')

        return res.as_str(key)

    def as_dict(self, target: Target, stage: StageDecorator) -> dict[str, Any]:
        """
        Get a dict of paths for a specific target and stage
        """
        res = self._get(target=target, stage=stage)

        if not res:
            raise StageTargetNotFoundError(f'Target "{target}" not found for Stage "{stage}".')

        return res.as_dict()

    def get_jobs(self, target: Target) -> list[Job]:
        """
        Get list of jobs that the next stage would depend on.
        """
        all_jobs: list[Job] = []
        target_sequencing_groups = target.get_sequencing_group_ids()
        for stage_, outputs_by_target in self._outputs_by_target_by_stage.items():
            for target_, output in outputs_by_target.items():
                if output:
                    output_sequencing_groups = output.target.get_sequencing_group_ids()
                    sequencing_groups_intersect = set(target_sequencing_groups) & set(
                        output_sequencing_groups,
                    )
                    if sequencing_groups_intersect:
                        for j in output.jobs:
                            assert j, f'Stage: {stage_}, target: {target_}, output: {output}'
                        all_jobs.extend(output.jobs)
        return all_jobs


class Stage(ABC, Generic[TargetT]):
    """
    Abstract class for a workflow stage. Parametrised by specific Target subclass,
    i.e. SequencingGroupStage(Stage[SequencingGroup]) should only be able to work on SequencingGroup(Target).
    """

    def __init__(
        self,
        *,
        name: str,
        required_stages: list[StageDecorator] | StageDecorator | None = None,
        analysis_type: str | None = None,
        analysis_keys: list[str] | None = None,
        update_analysis_meta: Callable[[str], dict] | None = None,
        tolerate_missing_output: bool = False,
        skipped: bool = False,
        assume_outputs_exist: bool = False,
        forced: bool = False,
    ):
        self._name = name
        self.required_stages_classes: list[StageDecorator] = []
        if required_stages:
            if isinstance(required_stages, list):
                self.required_stages_classes.extend(required_stages)
            else:
                self.required_stages_classes.append(required_stages)

        # Dependencies. Populated in workflow.run(), after we know all stages.
        self.required_stages: list[Stage] = []

        self.status_reporter = get_workflow().status_reporter
        # If `analysis_type` is defined, it will be used to create/update Analysis
        # entries in Metamist.
        self.analysis_type = analysis_type
        # If `analysis_keys` are defined, it will be used to extract the value for
        # `Analysis.output` if the Stage.expected_outputs() returns a dict.
        self.analysis_keys = analysis_keys
        # if `update_analysis_meta` is defined, it is called on the `Analysis.output`
        # field, and result is merged into the `Analysis.meta` dictionary.
        self.update_analysis_meta = update_analysis_meta

        self.tolerate_missing_output = tolerate_missing_output

        # Populated with the return value of `add_to_the_workflow()`
        self.output_by_target: dict[str, StageOutput | None] = dict()

        self.skipped = skipped
        self.forced = forced or self.name in get_config()['workflow'].get(
            'force_stages',
            [],
        )
        self.assume_outputs_exist = assume_outputs_exist

    @property
    def tmp_prefix(self):
        return get_workflow().tmp_prefix / self.name

    @property
    def web_prefix(self) -> Path:
        return get_workflow().web_prefix / self.name

    @property
    def prefix(self) -> Path:
        return get_workflow().prefix / self.name

    @property
    def analysis_prefix(self) -> Path:
        return get_workflow().analysis_prefix / self.name

    def get_stage_cohort_prefix(
        self,
        cohort: Cohort,
        category: str | None = None,
    ) -> Path:
        """
        Takes a cohort as an argument, calls through to the Workflow cohort_prefix method
        Result in the form PROJECT_BUCKET / WORKFLOW_NAME / COHORT_ID / STAGE_NAME
        e.g. "gs://cpg-project-main/seqr_loader/COH123/MyStage"

        Args:
            cohort (Cohort): we pull the analysis dataset and name from this Cohort
            category (str | none): main, tmp, test, analysis, web

        Returns:
            Path
        """
        return get_workflow().cohort_prefix(cohort, category=category) / self.name

    def __str__(self):
        res = f'{self._name}'
        if self.skipped:
            res += ' [skipped]'
        if self.forced:
            res += ' [forced]'
        if self.assume_outputs_exist:
            res += ' [assume_outputs_exist]'
        if self.required_stages:
            res += f' <- [{", ".join([s.name for s in self.required_stages])}]'
        return res

    @property
    def name(self) -> str:
        """
        Stage name (unique and descriptive stage)
        """
        return self._name

    @abstractmethod
    def queue_jobs(self, target: TargetT, inputs: StageInput) -> StageOutput | None:
        """
        Adds Hail Batch jobs that process `target`.
        Assumes that all the household work is done: checking missing inputs
        from required stages, checking for possible reuse of existing outputs.
        """

    @abstractmethod
    def expected_outputs(self, target: TargetT) -> ExpectedResultT:
        """
        Get path(s) to files that the stage is expected to generate for a `target`.
        Used within in `queue_jobs()` to pass paths to outputs to job commands,
        as well as by the workflow to check if the stage's expected outputs already
        exist and can be reused.

        Can be a str, a Path object, or a dictionary of str/Path objects.
        """

    @abstractmethod
    def queue_for_multicohort(
        self,
        multicohort: MultiCohort,
    ) -> dict[str, StageOutput | None]:
        """
        Queues jobs for each corresponding target, defined by Stage subclass.

        Returns a dictionary of `StageOutput` objects indexed by target unique_id.
        """

    def _make_inputs(self) -> StageInput:
        """
        Collects outputs from all dependencies and create input for this stage
        """
        inputs = StageInput(self)
        for prev_stage in self.required_stages:
            for _, stage_output in prev_stage.output_by_target.items():
                if stage_output:
                    inputs.add_other_stage_output(stage_output)
        return inputs

    def make_outputs(
        self,
        target: Target,
        data: ExpectedResultT = None,  # TODO: ExpectedResultT is probably too broad, our code only really support dict
        *,
        jobs: Sequence[Job | None] | Job | None = None,
        meta: dict | None = None,
        reusable: bool = False,
        skipped: bool = False,
        error_msg: str | None = None,
    ) -> StageOutput:
        """
        Create StageOutput for this stage.
        """
        return StageOutput(
            target=target,
            data=data,
            jobs=jobs,
            meta=meta,
            reusable=reusable,
            skipped=skipped,
            error_msg=error_msg,
            stage=self,
        )

    def _queue_jobs_with_checks(
        self,
        target: TargetT,
        action: Action | None = None,
    ) -> StageOutput | None:
        """
        Checks what to do with target, and either queue jobs, or skip/reuse results.
        """
        if not action:
            action = self._get_action(target)

        inputs = self._make_inputs()
        expected_out = self.expected_outputs(target)

        if action == Action.QUEUE:
            outputs = self.queue_jobs(target, inputs)
        elif action == Action.REUSE:
            outputs = self.make_outputs(
                target=target,
                data=expected_out,
                reusable=True,
            )
        else:  # Action.SKIP
            outputs = None

        if not outputs:
            return None

        outputs.stage = self
        outputs.meta |= self.get_job_attrs(target)

        for output_job in outputs.jobs:
            if output_job:
                for input_job in inputs.get_jobs(target):
                    assert input_job, f'Input dependency job for stage: {self}, target: {target}'
                    output_job.depends_on(input_job)

        if outputs.error_msg:
            return outputs

        # Adding status reporter jobs
        if self.analysis_type and self.status_reporter and action == Action.QUEUE and outputs.data:
            analysis_outputs: list[str | Path] = []
            if isinstance(outputs.data, dict):
                if not self.analysis_keys:
                    raise WorkflowError(
                        f'Cannot create Analysis: `analysis_keys` '
                        f'must be set with the @stage decorator to select value from '
                        f'the expected_outputs dict: {outputs.data}',
                    )
                if not all(key in outputs.data for key in self.analysis_keys):
                    raise WorkflowError(
                        f'Cannot create Analysis for stage {self.name}: `analysis_keys` '
                        f'"{self.analysis_keys}" is not a subset of the expected_outputs '
                        f'keys {outputs.data.keys()}',
                    )

                # Handle the case where the analysis key refers to a
                # list of outputs e.g. Cromwell jobs
                for analysis_key in self.analysis_keys:
                    data = outputs.data.get(analysis_key)
                    if isinstance(data, list):
                        analysis_outputs.extend(data)
                    elif data is not None:
                        analysis_outputs.append(data)

            else:
                analysis_outputs.append(outputs.data)

            project_name = None
            if isinstance(target, SequencingGroup | Cohort):
                project_name = target.dataset.name
            elif isinstance(target, Dataset):
                project_name = target.name
            elif isinstance(target, MultiCohort):
                project_name = target.analysis_dataset.name

            assert isinstance(project_name, str)

            # bump name to include `-test`
            if get_config()['workflow']['access_level'] == 'test' and 'test' not in project_name:
                project_name = f'{project_name}-test'

            for analysis_output in analysis_outputs:
                if not outputs.jobs:
                    continue

                assert isinstance(
                    analysis_output,
                    str | Path,
                ), f'{analysis_output} should be a str or Path object'
                if outputs.meta is None:
                    outputs.meta = {}

                self.status_reporter.create_analysis(
                    b=get_batch(),
                    output=str(analysis_output),
                    analysis_type=self.analysis_type,
                    target=target,
                    jobs=outputs.jobs,
                    job_attr=self.get_job_attrs(target) | {'stage': self.name, 'tool': 'metamist'},
                    meta=outputs.meta,
                    update_analysis_meta=self.update_analysis_meta,
                    tolerate_missing_output=self.tolerate_missing_output,
                    project_name=project_name,
                )

        return outputs

    def _get_action(self, target: TargetT) -> Action:
        """
        Based on stage parameters and expected outputs existence, determines what
        to do with the target: queue, skip or reuse, etc...
        """
        if target.forced and not self.skipped:
            logger.info(f'{self.name}: {target} [QUEUE] (target is forced)')
            return Action.QUEUE

        if (d := get_config()['workflow'].get('skip_stages_for_sgs')) and self.name in d:
            skip_targets = d[self.name]
            if target.target_id in skip_targets:
                logger.info(
                    f'{self.name}: {target} [SKIP] (is in workflow/skip_stages_for_sgs)',
                )
                return Action.SKIP

        expected_out = self.expected_outputs(target)
        reusable, first_missing_path = self._is_reusable(expected_out)

        if self.skipped:
            if reusable and not first_missing_path:
                logger.debug(
                    f'{self.name}: {target} [REUSE] (stage skipped, and outputs exist)',
                )
                return Action.REUSE
            if get_config()['workflow'].get('skip_sgs_with_missing_input'):
                logger.warning(
                    f'{self.name}: {target} [SKIP] (stage is required, '
                    f'but is marked as "skipped", '
                    f'workflow/skip_sgs_with_missing_input=true '
                    f'and some expected outputs for the target do not exist: '
                    f'{first_missing_path}',
                )
                # `workflow/skip_sgs_with_missing_input` means that we can ignore
                # sgs/datasets that have missing results from skipped stages.
                # This is our case, so indicating that this sg/dataset should
                # be ignored:
                target.active = False
                return Action.SKIP
            if self.name in get_config()['workflow'].get(
                'allow_missing_outputs_for_stages',
                [],
            ):
                logger.info(
                    f'{self.name}: {target} [REUSE] (stage is skipped, some outputs are'
                    f'missing, but stage is listed in '
                    f'workflow/allow_missing_outputs_for_stages)',
                )
                return Action.REUSE
            raise WorkflowError(
                f'{self.name}: stage is required, but is skipped, and '
                f'the following expected outputs for target {target} do not exist: '
                f'{first_missing_path}',
            )

        if reusable and not first_missing_path:
            if target.forced:
                logger.info(
                    f'{self.name}: {target} [QUEUE] (can reuse, but forcing the target to rerun this stage)',
                )
                return Action.QUEUE
            if self.forced:
                logger.info(
                    f'{self.name}: {target} [QUEUE] (can reuse, but forcing the stage to rerun)',
                )
                return Action.QUEUE
            logger.info(
                f'{self.name}: {target} [REUSE] (expected outputs exist: {expected_out})',
            )
            return Action.REUSE

        logger.info(f'{self.name}: {target} [QUEUE]')

        return Action.QUEUE

    def _is_reusable(self, expected_out: ExpectedResultT) -> tuple[bool, Path | None]:
        """
        Checks if the outputs of prior stages already exist, and can be reused
        Args:
            expected_out (ExpectedResultT): expected outputs of a stage

        Returns:
            tuple[bool, Path | None]:
                bool: True if the outputs can be reused, False otherwise
                Path | None: first missing path, if any
        """
        if self.assume_outputs_exist:
            logger.debug(f'Assuming outputs exist. Expected output is {expected_out}')
            return True, None

        if not expected_out:
            # Marking is reusable. If the stage does not naturally produce any outputs,
            # it would still need to create some flag file.
            logger.debug('No expected outputs, assuming outputs exist')
            return True, None

        if get_config()['workflow'].get('check_expected_outputs'):
            paths = path_walk(expected_out)
            logger.info(
                f'Checking if {paths} from expected output {expected_out} exist',
            )
            if not paths:
                logger.info(f'{expected_out} is not reusable. No paths found.')
                return False, None

            if first_missing_path := next((p for p in paths if not exists(p)), None):
                logger.info(
                    f'{expected_out} is not reusable, {first_missing_path} is missing',
                )
                return False, first_missing_path

            return True, None
        if self.skipped:
            # Do not check the files' existence, trust they exist.
            # note that for skipped stages, we automatically assume outputs exist
            return True, None
        # Do not check the files' existence, assume they don't exist:
        return False, None

    def get_job_attrs(self, target: TargetT | None = None) -> dict[str, str]:
        """
        Create Hail Batch Job attributes dictionary
        """
        job_attrs = dict(stage=self.name)
        if sequencing_type := get_config()['workflow'].get('sequencing_type'):
            job_attrs['sequencing_type'] = sequencing_type
        if target:
            job_attrs |= target.get_job_attrs()
        return job_attrs


# ---- Overloads ----
# These overloads are used to provide type hints for the `stage` decorator.


@overload
def stage(cls: type[Stage]) -> StageDecorator: ...


@overload
def stage(
    *,
    analysis_type: str | None = None,
    analysis_keys: list[str | Path] | None = None,
    update_analysis_meta: Callable[[str], dict] | None = None,
    tolerate_missing_output: bool = False,
    required_stages: list[StageDecorator] | StageDecorator | None = None,
    skipped: bool = False,
    assume_outputs_exist: bool = False,
    forced: bool = False,
) -> Callable[[type[Stage]], StageDecorator]: ...


# ---- Actual Implementation ----
def stage(
    cls: type['Stage'] | None = None,
    *,
    analysis_type: str | None = None,
    analysis_keys: list[str | Path] | None = None,
    update_analysis_meta: Callable[[str], dict] | None = None,
    tolerate_missing_output: bool = False,
    required_stages: list[StageDecorator] | StageDecorator | None = None,
    skipped: bool = False,
    assume_outputs_exist: bool = False,
    forced: bool = False,
) -> StageDecorator | Callable[[type[Stage]], StageDecorator]:
    """
    Implements a standard class decorator pattern with optional arguments.
    The goal is to allow declaring workflow stages without requiring to implement
    a constructor method. E.g.

    @stage(required_stages=[Align])
    class GenotypeSample(SequencingGroupStage):
        def expected_outputs(self, sequencing_group: SequencingGroup):
            ...
        def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput:
            ...

    @analysis_type: if defined, will be used to create/update `Analysis` entries
        using the status reporter.
    @analysis_keys: is defined, will be used to extract the value for `Analysis.output`
        if the Stage.expected_outputs() returns a dict.
    @update_analysis_meta: if defined, this function is called on the `Analysis.output`
        field, and returns a dictionary to be merged into the `Analysis.meta`
    @tolerate_missing_output: if True, when registering the output of this stage,
        allow for the output file to be missing (only relevant for metamist entry)
    @required_stages: list of other stage classes that are required prerequisites
        for this stage. Outputs of those stages will be passed to
        `Stage.queue_jobs(... , inputs)` as `inputs`, and all required
        dependencies between Hail Batch jobs will be set automatically as well.
    @skipped: always skip this stage.
    @assume_outputs_exist: assume expected outputs of this stage always exist.
    @forced: always force run this stage, regardless of the outputs' existence.
    """

    def decorator_stage(_cls) -> StageDecorator:
        """Implements decorator."""

        @functools.wraps(_cls)
        def wrapper_stage() -> Stage:
            """Decorator helper function."""
            return _cls(
                name=_cls.__name__,
                required_stages=required_stages,
                analysis_type=analysis_type,
                analysis_keys=analysis_keys,
                update_analysis_meta=update_analysis_meta,
                skipped=skipped,
                assume_outputs_exist=assume_outputs_exist,
                forced=forced,
                tolerate_missing_output=tolerate_missing_output,
            )

        return wrapper_stage

    if cls is None:
        return decorator_stage

    return decorator_stage(cls)


class SequencingGroupStage(Stage[SequencingGroup], ABC):
    """
    Sequencing Group level stage.
    """

    @abstractmethod
    def expected_outputs(self, sequencing_group: SequencingGroup) -> ExpectedResultT:
        """
        Override to declare expected output paths.
        """

    @abstractmethod
    def queue_jobs(
        self,
        sequencing_group: SequencingGroup,
        inputs: StageInput,
    ) -> StageOutput | None:
        """
        Override to add Hail Batch jobs.
        """

    def queue_for_multicohort(
        self,
        multicohort: MultiCohort,
    ) -> dict[str, StageOutput | None]:
        """
        Plug the stage into the workflow.
        """
        output_by_target: dict[str, StageOutput | None] = dict()
        if not (active_sgs := multicohort.get_sequencing_groups()):
            all_sgs = len(multicohort.get_sequencing_groups(only_active=False))
            logger.warning(
                f'{len(active_sgs)}/{all_sgs} usable (active=True) SGs found in the multicohort. '
                'Check that input_cohorts` or `input_datasets` are provided and not skipped',
            )
            return output_by_target

        # evaluate_stuff en masse
        for sequencing_group in active_sgs:
            action = self._get_action(sequencing_group)
            output_by_target[sequencing_group.target_id] = self._queue_jobs_with_checks(
                sequencing_group,
                action,
            )
        return output_by_target


class DatasetStage(Stage, ABC):
    """
    Dataset-level stage
    """

    @abstractmethod
    def expected_outputs(self, dataset: Dataset) -> ExpectedResultT:
        """
        Override to declare expected output paths.
        """

    @abstractmethod
    def queue_jobs(self, dataset: Dataset, inputs: StageInput) -> StageOutput | None:
        """
        Override to add Hail Batch jobs.
        """

    def queue_for_multicohort(
        self,
        multicohort: MultiCohort,
    ) -> dict[str, StageOutput | None]:
        """
        Plug the stage into the workflow.
        """
        output_by_target: dict[str, StageOutput | None] = dict()
        # iterate directly over the datasets in this multicohort
        for dataset in multicohort.get_datasets():
            action = self._get_action(dataset)
            output_by_target[dataset.target_id] = self._queue_jobs_with_checks(
                dataset,
                action,
            )
        return output_by_target


class CohortStage(Stage, ABC):
    """
    Cohort-level stage (all datasets of a workflow run).
    """

    @abstractmethod
    def expected_outputs(self, cohort: Cohort) -> ExpectedResultT:
        """
        Override to declare expected output paths.
        """

    @abstractmethod
    def queue_jobs(self, cohort: Cohort, inputs: StageInput) -> StageOutput | None:
        """
        Override to add Hail Batch jobs.
        """

    def queue_for_multicohort(
        self,
        multicohort: MultiCohort,
    ) -> dict[str, StageOutput | None]:
        """
        Plug the stage into the workflow.
        """
        output_by_target: dict[str, StageOutput | None] = dict()
        for cohort in multicohort.get_cohorts():
            action = self._get_action(cohort)
            output_by_target[cohort.target_id] = self._queue_jobs_with_checks(
                cohort,
                action,
            )
        return output_by_target


class MultiCohortStage(Stage, ABC):
    """
    MultiCohort-level stage (all datasets of a workflow run).
    """

    @abstractmethod
    def expected_outputs(self, multicohort: MultiCohort) -> ExpectedResultT:
        """
        Override to declare expected output paths.
        """

    @abstractmethod
    def queue_jobs(
        self,
        multicohort: MultiCohort,
        inputs: StageInput,
    ) -> StageOutput | None:
        """
        Override to add Hail Batch jobs.
        """

    def queue_for_multicohort(
        self,
        multicohort: MultiCohort,
    ) -> dict[str, StageOutput | None]:
        """
        Plug the stage into the workflow.
        """
        output_by_target: dict[str, StageOutput | None] = dict()
        action = self._get_action(multicohort)
        output_by_target[multicohort.target_id] = self._queue_jobs_with_checks(
            multicohort,
            action,
        )
        return output_by_target
