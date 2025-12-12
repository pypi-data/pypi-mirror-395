"""
This module provides helper functions for handling sequencing type subdirectories.

Functions:
    sequencing_subdir: Returns a subdirectory name based on the sequencing type from the configuration.

"""

from cpg_utils.config import config_retrieve


def sequencing_subdir() -> str:
    """
    Subdirectory parametrised by sequencing type & technology.
    For genomes and short-read, we don't prefix at all.
    """
    seq_type = config_retrieve(['workflow', 'sequencing_type'], None)
    seq_tech = config_retrieve(['workflow', 'sequencing_technology'], None)

    if seq_tech:
        seq_tech = seq_tech.replace('-', '_')

    if not seq_tech or (seq_tech == 'short_read'):
        return '' if not seq_type or seq_type == 'genome' else seq_type

    return f'{seq_tech}/{seq_type}' if seq_type != 'genome' else seq_tech
