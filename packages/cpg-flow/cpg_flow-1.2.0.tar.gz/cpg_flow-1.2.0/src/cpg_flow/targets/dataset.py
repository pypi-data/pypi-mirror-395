"""
This module defines the `Dataset` class, which is part of the cpg-flow system for managing genomic datasets.

The `Dataset` class allows for:
- Managing sequencing groups: Creation, addition, and retrieval of sequencing groups that are part of the dataset.
- Storage path management: Provides methods to access primary, temporary, analysis, and web storage paths.
- Integration with configurations: Uses configuration settings for workflow management and path handling.
- Pedigree file generation: Capable of generating PED files based on sequencing group data for genetic analysis.
- Logging: Utilizes logger to track and debug sequencing group additions.

Key Components:
- Dataset: Main class that represents a genomic dataset and extends from the `Target` class.
- SequencingGroup Management: Methods to handle sequencing groups related to the dataset.
- Path Handling: Methods to derive and handle various storage paths.
- Configurations: Integration with external configuration settings for flexible dataset handling.

This module is essential for organizing and managing data resources in CPG-related projects.

"""

from typing import TYPE_CHECKING, Optional

import pandas as pd
from loguru import logger

from cpg_flow.filetypes import AlignmentInput
from cpg_flow.targets import SequencingGroup, Target, sequencing_subdir
from cpg_utils import Path, to_path
from cpg_utils.config import dataset_path, get_config, web_url

if TYPE_CHECKING:
    from cpg_flow.targets import PedigreeInfo, Sex


class Dataset(Target):
    """
    Represents a CPG dataset.

    Each `dataset` at the CPG corresponds to
    * a GCP project: https://github.com/populationgenomics/team-docs/tree/main/storage_policies
    * a Pulumi stack: https://github.com/populationgenomics/analysis-runner/tree/main/stack
    * a metamist project
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._sequencing_group_by_id: dict[str, SequencingGroup] = {}
        self.name = name
        self.active = True

    @staticmethod
    def create(name: str) -> 'Dataset':
        """
        Create a dataset.
        """
        return Dataset(name=name)

    @property
    def target_id(self) -> str:
        """Unique target ID"""
        return self.name

    def __repr__(self):
        return f'Dataset("{self.name}", {len(self.get_sequencing_groups())} sequencing groups)'

    def __str__(self):
        return f'{self.name} ({len(self.get_sequencing_groups())} sequencing groups)'

    def prefix(self, **kwargs) -> Path:
        """
        The primary storage path.
        """
        return to_path(
            dataset_path(
                sequencing_subdir(),
                dataset=self.name,
                **kwargs,
            ),
        )

    def tmp_prefix(self, **kwargs) -> Path:
        """
        Storage path for temporary files.
        """
        return to_path(
            dataset_path(
                sequencing_subdir(),
                dataset=self.name,
                category='tmp',
                **kwargs,
            ),
        )

    def analysis_prefix(self, **kwargs) -> Path:
        """
        Storage path for analysis files.
        """
        return to_path(
            dataset_path(
                sequencing_subdir(),
                dataset=self.name,
                category='analysis',
                **kwargs,
            ),
        )

    def web_prefix(self, **kwargs) -> Path:
        """
        Path for files served by an HTTP server Matches corresponding URLs returns by
        self.web_url() URLs.
        """
        return to_path(
            dataset_path(
                sequencing_subdir(),
                dataset=self.name,
                category='web',
                **kwargs,
            ),
        )

    def web_url(self) -> str | None:
        """
        URLs matching self.storage_web_path() files serverd by an HTTP server.
        """
        return web_url(
            sequencing_subdir(),
            dataset=self.name,
        )

    def add_sequencing_group(
        self,
        id: str,  # pylint: disable=redefined-builtin
        *,
        sequencing_type: str,
        sequencing_technology: str,
        sequencing_platform: str,
        external_id: str | None = None,
        participant_id: str | None = None,
        meta: dict | None = None,
        sex: Optional['Sex'] = None,
        pedigree: Optional['PedigreeInfo'] = None,
        alignment_input: AlignmentInput | None = None,
    ) -> 'SequencingGroup':
        """
        Create a new sequencing group and add it to the dataset.
        """
        if id in self._sequencing_group_by_id:
            logger.debug(
                f'SequencingGroup {id} already exists in the dataset {self.name}',
            )
            return self._sequencing_group_by_id[id]

        force_sgs = get_config()['workflow'].get('force_sgs', set())
        forced = id in force_sgs or external_id in force_sgs or participant_id in force_sgs

        s = SequencingGroup(
            id=id,
            dataset=self,
            external_id=external_id,
            sequencing_type=sequencing_type,
            sequencing_technology=sequencing_technology,
            sequencing_platform=sequencing_platform,
            participant_id=participant_id,
            meta=meta,
            sex=sex,
            pedigree=pedigree,
            alignment_input=alignment_input,
            forced=forced,
        )
        self._sequencing_group_by_id[id] = s
        return s

    def add_sequencing_group_object(self, s: 'SequencingGroup'):
        """
        Add a sequencing group object to the dataset.
        Args:
            s: SequencingGroup object
        """
        if s.id in self._sequencing_group_by_id:
            logger.debug(
                f'SequencingGroup {s.id} already exists in the dataset {self.name}',
            )
        else:
            self._sequencing_group_by_id[s.id] = s

    def get_sequencing_group_by_id(self, id: str) -> Optional['SequencingGroup']:
        """
        Get sequencing group by ID
        """
        return self._sequencing_group_by_id.get(id)

    def get_sequencing_groups(
        self,
        only_active: bool = True,
    ) -> list['SequencingGroup']:
        """
        Get dataset's sequencing groups. Include only "active" sequencing groups, unless only_active=False
        """
        return [s for sid, s in self._sequencing_group_by_id.items() if (s.active or not only_active)]

    def get_job_attrs(self) -> dict:
        """
        Attributes for Hail Batch job.
        """
        return {
            'dataset': self.name,
            'sequencing_groups': self.get_sequencing_group_ids(),
        }

    def get_job_prefix(self) -> str:
        """
        Prefix job names.
        """
        return f'{self.name}: '

    def write_ped_file(
        self,
        out_path: Path | None = None,
        use_participant_id: bool = False,
    ) -> Path:
        """
        Create a PED file for all sequencing groups
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
            out_path = self.tmp_prefix() / 'ped' / f'{self.get_alignment_inputs_hash()}.ped'

        if not get_config()['workflow'].get('dry_run', False):
            with out_path.open('w') as fp:
                df.to_csv(fp, sep='\t', index=False, header=False)
        return out_path
