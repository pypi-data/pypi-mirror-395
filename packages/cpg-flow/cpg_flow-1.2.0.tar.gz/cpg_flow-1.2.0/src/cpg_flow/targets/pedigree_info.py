from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from cpg_flow.targets import Sex

if TYPE_CHECKING:
    from cpg_flow.targets import SequencingGroup


@dataclass
class PedigreeInfo:
    """
    Pedigree relationships with other sequencing groups in the cohort, and other PED data
    """

    sequencing_group: 'SequencingGroup'
    sex: 'Sex' = Sex.UNKNOWN
    fam_id: str | None = None
    phenotype: str | int = 0
    dad: Union['SequencingGroup', None] = None
    mom: Union['SequencingGroup', None] = None

    def get_ped_dict(self, use_participant_id: bool = False) -> dict[str, str]:
        """
        Returns a dictionary of pedigree fields for this sequencing group, corresponding
        a PED file entry.
        """

        def _get_id(_s: Union['SequencingGroup', None]) -> str:
            if _s is None:
                return '0'
            if use_participant_id:
                return _s.participant_id
            return _s.id

        return {
            'Family.ID': self.fam_id or self.sequencing_group.participant_id,
            'Individual.ID': _get_id(self.sequencing_group),
            'Father.ID': _get_id(self.dad),
            'Mother.ID': _get_id(self.mom),
            'Sex': str(self.sex.value),
            'Phenotype': str(self.phenotype),
        }
