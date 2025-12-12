"""
This module defines classes for handling multi-cohort and cohort targets in a workflow.
It includes functionality for managing datasets, sequencing groups, and generating PED files.

Classes:
    MultiCohort: Represents a multi-cohort target with multiple cohorts in the workflow.
    Cohort: Represents a cohort target with all sequencing groups from a single CustomCohort.
    Dataset: Represents a CPG dataset.
    Sex: Enum for representing sex as in PED format.
    SequencingGroup: Represents a sequencing group.
    PedigreeInfo: Represents pedigree relationships and other PED data.

Functions:
    sequencing_subdir: Returns a subdirectory parametrized by sequencing type.
"""

from typing import TYPE_CHECKING, Optional

import pandas as pd
from loguru import logger

from cpg_flow.targets import Cohort, Dataset, Target
from cpg_flow.utils import hash_from_list_of_strings
from cpg_utils import Path
from cpg_utils.config import get_config

if TYPE_CHECKING:
    from cpg_flow.targets import SequencingGroup


class MultiCohort(Target):
    """
    Represents a "multi-cohort" target - multiple cohorts in the workflow.
    """

    def __init__(self) -> None:
        super().__init__()

        # Previously MultiCohort.name was an underscore-delimited string of all the input cohorts
        # this was expanding to the point where filenames including this String were too long for *nix
        # instead we can create a hash of the input cohorts, and use that as the name
        # the exact cohorts can be obtained from the config associated with the ar-guid
        input_cohorts = get_config()['workflow'].get('input_cohorts', [])
        if input_cohorts:
            self.name = hash_from_list_of_strings(sorted(input_cohorts), suffix='cohorts')
        else:
            self.name = get_config()['workflow']['dataset']

        assert self.name, 'Ensure cohorts or dataset is defined in the config file.'

        self._cohorts_by_id: dict[str, Cohort] = {}
        self._datasets_by_name: dict[str, Dataset] = {}
        self.analysis_dataset = Dataset(name=get_config()['workflow']['dataset'])

    def __repr__(self):
        return f'MultiCohort({len(self.get_cohorts())} cohorts)'

    @property
    def target_id(self) -> str:
        """Unique target ID"""
        return self.name

    def create_dataset(self, name: str) -> 'Dataset':
        """
        Create a dataset and add it to the cohort.
        """
        if name in self._datasets_by_name:
            return self._datasets_by_name[name]

        if name == self.analysis_dataset.name:
            ds = self.analysis_dataset
        else:
            ds = Dataset(name=name)

        self._datasets_by_name[ds.name] = ds
        return ds

    def get_cohorts(self, only_active: bool = True) -> list['Cohort']:
        """
        Gets list of all cohorts.
        Include only "active" cohorts (unless only_active is False)
        """
        cohorts = list(self._cohorts_by_id.values())
        if only_active:
            cohorts = [c for c in cohorts if c.active]
        return cohorts

    def get_cohort_ids(self, only_active: bool = True) -> list['str']:
        """
        Get list of cohort IDs.
        Include only "active" cohorts (unless only_active is False)
        """
        return [c.get_cohort_id() for c in self.get_cohorts(only_active)]

    def get_cohort_by_id(
        self,
        id: str,
        only_active: bool = True,
    ) -> Optional['Cohort']:
        """
        Get cohort by id.
        Include only "active" cohorts (unless only_active is False)
        """
        cohort = self._cohorts_by_id.get(id)
        if not cohort:
            logger.warning(f'Cohort {id} not found in the multi-cohort')

        if not only_active:  # Return cohort even if it's inactive
            return cohort
        if isinstance(cohort, Cohort) and cohort.active:
            return cohort
        return None

    def get_datasets(self, only_active: bool = True) -> list['Dataset']:
        """
        Gets list of all datasets.
        Include only "active" datasets (unless only_active is False)
        """
        all_datasets = list(self._datasets_by_name.values())
        if only_active:
            all_datasets = [d for d in all_datasets if d.active and d.get_sequencing_groups()]
        return all_datasets

    def get_sequencing_groups(
        self,
        only_active: bool = True,
    ) -> list['SequencingGroup']:
        """
        Gets a flat list of all sequencing groups from all datasets.
        uses a dictionary to avoid duplicates (we could have the same sequencing group in multiple cohorts)
        Include only "active" sequencing groups (unless only_active is False)
        """
        all_sequencing_groups: dict[str, SequencingGroup] = {}
        for dataset in self.get_datasets(only_active):
            for sg in dataset.get_sequencing_groups(only_active):
                all_sequencing_groups[sg.id] = sg
        return list(all_sequencing_groups.values())

    def create_cohort(self, id: str, name: str, dataset: str | None = None) -> 'Cohort':
        """
        Create a cohort and add it to the multi-cohort.
        """
        if id in self._cohorts_by_id:
            logger.debug(f'Cohort {id} already exists in the multi-cohort')
            return self._cohorts_by_id[id]

        c = Cohort(id=id, name=name, dataset=dataset)
        self._cohorts_by_id[c.id] = c
        return c

    def add_dataset(self, d: 'Dataset') -> 'Dataset':
        """
        Add a Dataset to the MultiCohort
        Args:
            d: Dataset object
        """
        if d.name in self._datasets_by_name:
            logger.debug(
                f'Dataset {d.name} already exists in the MultiCohort {self.name}',
            )
        else:
            # We need create a new dataset to avoid manipulating the cohort dataset at this point
            self._datasets_by_name[d.name] = Dataset(d.name)
        return self._datasets_by_name[d.name]

    def get_dataset_by_name(
        self,
        name: str,
        only_active: bool = True,
    ) -> Optional['Dataset']:
        """
        Get dataset by name.
        Include only "active" datasets (unless only_active is False)
        """
        ds_by_name = {d.name: d for d in self.get_datasets(only_active)}
        return ds_by_name.get(name)

    def get_job_attrs(self) -> dict:
        """
        Attributes for Hail Batch job.
        """
        return {
            'sequencing_groups': self.get_sequencing_group_ids(),
            'datasets': [d.name for d in self.get_datasets()],
            'cohorts': [c.id for c in self.get_cohorts()],
        }

    def write_ped_file(
        self,
        out_path: Path | None = None,
        use_participant_id: bool = False,
    ) -> Path:
        """
        Create a PED file for all samples in the whole MultiCohort
        Duplication of the Cohort method
        PED is written with no header line to be strict specification compliant
        """
        datas = []
        for sequencing_group in self.get_sequencing_groups():
            datas.append(
                sequencing_group.pedigree.get_ped_dict(
                    use_participant_id=use_participant_id,
                ),
            )
        if not datas:
            raise ValueError(f'No pedigree data found for {self.name}')
        df = pd.DataFrame(datas)

        if out_path is None:
            out_path = self.analysis_dataset.tmp_prefix() / 'ped' / f'{self.get_alignment_inputs_hash()}.ped'

        if not get_config()['workflow'].get('dry_run', False):
            with out_path.open('w') as fp:
                df.to_csv(fp, sep='\t', index=False, header=False)
        return out_path
