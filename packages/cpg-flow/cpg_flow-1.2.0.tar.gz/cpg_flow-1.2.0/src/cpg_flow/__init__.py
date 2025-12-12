# This is used to define what pdoc will generate documentation for
"""
cpg_flow package

This package provides the core functionality for defining and managing computational pipelines.
It includes modules for specifying pipeline targets, stages, and workflows.

Modules:
- targets: Defines the targets or endpoints of the pipeline.
- stage: Manages individual stages or steps within the pipeline.
- workflow: Orchestrates the overall workflow of the pipeline, connecting stages and targets.

This package is designed to be used with pdoc for generating documentation.
"""

from . import stage, targets, workflow

__version__ = '1.2.0'

__all__ = ['stage', 'targets', 'workflow']
