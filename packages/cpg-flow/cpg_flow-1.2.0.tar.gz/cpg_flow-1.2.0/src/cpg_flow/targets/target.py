"""

This module defines the `Target` class, which represents a target that a stage can act upon.
The `Target` class includes methods to retrieve sequencing groups and their IDs, compute a hash
for alignment inputs, and provide job attributes and prefixes. It also includes a property to
retrieve a unique target ID and a method to map internal IDs to participant or external IDs.

Classes:
    Target: Defines a target that a stage can act upon.

Methods:
    get_sequencing_groups(only_active: bool = True) -> list["SequencingGroup"]:
        Get a flat list of all sequencing groups corresponding to this target.

    get_sequencing_group_ids(only_active: bool = True) -> list[str]:
        Get a flat list of all sequencing group IDs corresponding to this target.

    get_alignment_inputs_hash() -> str:
        Compute a hash for the alignment inputs of the sequencing groups.

    target_id() -> str:
        Property to retrieve a unique target ID.

    get_job_attrs() -> dict:
        Retrieve attributes for Hail Batch job.

    get_job_prefix() -> str:
        Retrieve prefix for job names.

    rich_id_map() -> dict[str, str]:
        Map internal IDs to participant or external IDs, if the latter is provided.

Targets for workflow stages: SequencingGroup, Dataset, Cohort.

"""

import hashlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cpg_flow.targets import SequencingGroup


class Target:
    """
    Defines a target that a stage can act upon.
    """

    def __init__(self) -> None:
        # Whether to process even if outputs exist:
        self.forced: bool = False

        # If not set, exclude from the workflow:
        self.active: bool = True

        # create a self.alignment_inputs_hash variable to store the hash of the alignment inputs
        # this begins as None, and is set upon first calling
        self.alignment_inputs_hash: str | None = None

        # similar to alignment_inputs_hash, but based on the SG IDs instead of the underlying assays
        self.sg_hash: str | None = None

    def get_sequencing_groups(
        self,
        only_active: bool = True,
    ) -> list['SequencingGroup']:
        """
        Get flat list of all sequencing groups corresponding to this target.
        """
        raise NotImplementedError

    def get_sequencing_group_ids(self, only_active: bool = True) -> list[str]:
        """
        Get flat list of all sequencing group IDs corresponding to this target.
        """
        return [s.id for s in self.get_sequencing_groups(only_active=only_active)]

    def get_alignment_inputs_hash(self) -> str:
        """
        If this hash has been set, return it, otherwise set it, then return it
        This should be safe as it matches the current usage:
        - we set up the Targets in this workflow (populating SGs, Datasets, Cohorts)
            - at this point the targets are malleable (e.g. addition of an additional Cohort may add SGs to Datasets)
        - we then set up the Stages, where alignment input hashes are generated
            - at this point, the alignment inputs are fixed
            - all calls to get_alignment_inputs_hash() need to return the same value
        """
        if self.alignment_inputs_hash is None:
            self.set_alignment_inputs_hash()
        if self.alignment_inputs_hash is None:
            raise TypeError('Alignment_inputs_hash was not populated by the setter method')
        return self.alignment_inputs_hash

    def set_alignment_inputs_hash(self):
        """
        Unique hash string of sample alignment inputs. Useful to decide
        whether the analysis on the target needs to be rerun.
        """
        s = ' '.join(
            sorted(' '.join(str(s.alignment_input)) for s in self.get_sequencing_groups() if s.alignment_input),
        )
        h = hashlib.sha256(s.encode()).hexdigest()[:38]
        self.alignment_inputs_hash = f'{h}_{len(self.get_sequencing_group_ids())}'

    def get_sg_hash(self) -> str:
        """If the SG hash was generated, return it, otherwise generate and return it."""
        if self.sg_hash is None:
            self.set_sg_hash()
        if self.sg_hash is None:
            raise TypeError('SG_hash was not populated by the setter method')
        return self.sg_hash

    def set_sg_hash(self):
        """Unique hash string from Sequencing Group IDs, used to create a unique string to use in output paths."""
        sg_ids = sorted(self.get_sequencing_group_ids())
        h = hashlib.sha256(''.join(sg_ids).encode()).hexdigest()[:38]
        self.sg_hash = f'{h}_{len(sg_ids)}'

    @property
    def target_id(self) -> str:
        """
        ID should be unique across target of all levels.

        We are raising NotImplementedError instead of making it an abstract class,
        because mypy is not happy about binding TypeVar to abstract classes, see:
        https://stackoverflow.com/questions/48349054/how-do-you-annotate-the-type-of
        -an-abstract-class-with-mypy

        Specifically,
        ```
        TypeVar('TargetT', bound=Target)
        ```
        Will raise:
        ```
        Only concrete class can be given where "Type[Target]" is expected
        ```
        """
        raise NotImplementedError

    def get_job_attrs(self) -> dict:
        """
        Attributes for Hail Batch job.
        """
        raise NotImplementedError

    def get_job_prefix(self) -> str:
        """
        Prefix job names.
        """
        raise NotImplementedError

    def rich_id_map(self) -> dict[str, str]:
        """
        Map if internal IDs to participant or external IDs, if the latter is provided.
        """
        return {s.id: s.rich_id for s in self.get_sequencing_groups() if s.participant_id != s.id}
