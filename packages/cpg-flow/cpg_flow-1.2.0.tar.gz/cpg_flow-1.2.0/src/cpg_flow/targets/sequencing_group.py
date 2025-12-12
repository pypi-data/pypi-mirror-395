from typing import TYPE_CHECKING, Optional

from cpg_flow.filetypes import AlignmentInput, BamPath, CramPath, FastqPairs, GvcfPath
from cpg_flow.metamist import Assay
from cpg_flow.targets import PedigreeInfo, Sex, Target
from cpg_utils import Path
from cpg_utils.config import reference_path

if TYPE_CHECKING:
    from cpg_flow.targets import Dataset


class SequencingGroup(Target):
    """
    Represents a sequencing group.
    """

    def __init__(
        self,
        id: str,
        dataset: 'Dataset',
        *,
        sequencing_type: str,
        sequencing_technology: str,
        sequencing_platform: str,
        external_id: str | None = None,
        participant_id: str | None = None,
        meta: dict | None = None,
        sex: Sex | None = None,
        pedigree: Optional['PedigreeInfo'] = None,
        alignment_input: AlignmentInput | None = None,
        assays: tuple[Assay, ...] | None = None,
        forced: bool = False,
    ):
        super().__init__()
        self.id = id
        self.name = id
        self._external_id = external_id
        self.sequencing_type = sequencing_type
        self.sequencing_technology = sequencing_technology
        self.sequencing_platform = sequencing_platform

        self.dataset = dataset
        self._participant_id = participant_id
        self.meta: dict = meta or dict()
        self.pedigree: PedigreeInfo = pedigree or PedigreeInfo(
            sequencing_group=self,
            fam_id=self.participant_id,
            sex=sex or Sex.UNKNOWN,
        )
        if sex:
            self.pedigree.sex = sex
        self.alignment_input: AlignmentInput | None = alignment_input
        self.assays: tuple[Assay, ...] | None = assays
        self.forced = forced
        self.active = True
        # Only set if the file exists / found in Metamist:
        self.gvcf: GvcfPath | None = None
        self.cram: CramPath | None = None

    def __repr__(self):
        values = {
            'participant': self._participant_id if self._participant_id else '',
            'sequencing_type': self.sequencing_type,
            'sequencing_technology': self.sequencing_technology,
            'sequencing_platform': self.sequencing_platform,
            'forced': str(self.forced),
            'active': str(self.active),
            'meta': str(self.meta),
            'alignment_inputs': self.alignment_input,
            'pedigree': self.pedigree,
        }
        retval = f'SequencingGroup({self.dataset.name}/{self.id}'
        if self._external_id:
            retval += f'|{self._external_id}'
        return retval + ''.join(f', {k}={v}' for k, v in values.items())

    def __str__(self):
        ai_tag = ''
        if self.alignment_input:
            ai_tag += f'|SEQ={self.sequencing_type}:'
            if isinstance(self.alignment_input, CramPath):
                ai_tag += 'CRAM'
            elif isinstance(self.alignment_input, BamPath):
                ai_tag += 'BAM'
            elif isinstance(self.alignment_input, FastqPairs):
                ai_tag += f'{len(self.alignment_input)}FQS'
            else:
                raise ValueError(
                    f'Unrecognised alignment input type {type(self.alignment_input)}',
                )

        ext_id = f'|{self._external_id}' if self._external_id else ''
        return f'SequencingGroup({self.dataset.name}/{self.id}{ext_id}{ai_tag})'

    @property
    def participant_id(self) -> str:
        """
        Get ID of participant corresponding to this sequencing group,
        or substitute it with external ID.
        """
        return self._participant_id or self.external_id

    @participant_id.setter
    def participant_id(self, val: str):
        """
        Set participant ID.
        """
        self._participant_id = val

    @property
    def external_id(self) -> str:
        """
        Get external sample ID, or substitute it with the internal ID.
        """
        return self._external_id or self.id

    @property
    def rich_id(self) -> str:
        """
        ID for reporting purposes: composed of internal as well as external
        or participant IDs.
        """
        return self.id + '|' + self.participant_id

    def get_ped_dict(self, use_participant_id: bool = False) -> dict[str, str]:
        """
        Returns a dictionary of pedigree fields for this sequencing group, corresponding
        a PED file entry.
        """
        return self.pedigree.get_ped_dict(use_participant_id)

    def make_cram_path(self) -> CramPath:
        """
        Path to a CRAM file. Not checking its existence here.
        """
        path = self.dataset.prefix() / 'cram' / f'{self.id}.cram'
        return CramPath(
            path=path,
            index_path=path.with_suffix('.cram.crai'),
            reference_assembly=reference_path('broad/ref_fasta'),
        )

    def make_gvcf_path(self) -> GvcfPath:
        """
        Path to a GVCF file. Not checking its existence here.
        """
        return GvcfPath(self.dataset.prefix() / 'gvcf' / f'{self.id}.g.vcf.gz')

    @property
    def make_sv_evidence_path(self) -> Path:
        """
        Path to the evidence root for GATK-SV evidence files.
        """
        return self.dataset.prefix() / 'sv_evidence'

    @property
    def target_id(self) -> str:
        """Unique target ID"""
        return self.id

    def get_sequencing_groups(
        self,
        only_active: bool = True,
    ) -> list['SequencingGroup']:
        """
        Implementing the abstract method.
        """
        if only_active and not self.active:
            return []
        return [self]

    def get_job_attrs(self) -> dict:
        """
        Attributes for Hail Batch job.
        """
        attrs = {
            'dataset': self.dataset.name,
            'sequencing_group': self.id,
        }
        participant_id: str | None = self._participant_id or self._external_id
        if participant_id:
            attrs['participant_id'] = participant_id
        return attrs

    def get_job_prefix(self) -> str:
        """
        Prefix job names.
        """
        return f'{self.dataset.name}/{self.id}: '
