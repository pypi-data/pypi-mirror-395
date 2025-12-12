# ruff: noqa: F401, I001
"""
This module initializes the `cpg_flow.targets` package and imports key classes and functions.

The import order is crucial to avoid circular imports.

Classes:
    Target: Represents a target in the CPG flow.
    Sex: Enum representing the sex of an individual.
    PedigreeInfo: Contains pedigree information for individuals.
    SequencingGroup: Represents a group of sequencing data.
    Dataset: Represents a dataset in the CPG flow.
    Cohort: Represents a cohort of individuals.
    MultiCohort: Represents multiple cohorts.

Functions:
    sequencing_subdir: Helper function to get the subdirectory for a given sequencing type.
"""

# Note: the import order below is important in order to avoid circular imports
from cpg_flow.targets.target import Target
from cpg_flow.targets.helpers import sequencing_subdir
from cpg_flow.targets.types import Sex
from cpg_flow.targets.pedigree_info import PedigreeInfo
from cpg_flow.targets.sequencing_group import SequencingGroup
from cpg_flow.targets.dataset import Dataset
from cpg_flow.targets.cohort import Cohort
from cpg_flow.targets.multicohort import MultiCohort
