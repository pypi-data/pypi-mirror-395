<!-- markdownlint-disable MD033 MD024 -->
# 🐙 CPG Flow

<img src="/assets/DNA_CURIOUS_FLOYD_CROPPED.png" height="300" alt="CPG Flow logo" align="right"/>

![Python](https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=2F73BF)

[![⚙️ Test Workflow](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml)
[![🚀 Deploy To Production Workflow](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml)
[![GitHub Latest Main Release](https://img.shields.io/github/v/release/populationgenomics/cpg-flow?label=main%20release)](https://GitHub.com/populationgenomics/cpg-flow/releases/)
[![GitHub Release](https://img.shields.io/github/v/release/populationgenomics/cpg-flow?include_prereleases&label=latest)](https://GitHub.com/populationgenomics/cpg-flow/releases/)
[![semantic-release: conventional commits](https://img.shields.io/badge/semantic--release-conventional%20commits-Æ1A7DBD?logo=semantic-release&color=1E7FBF)](https://github.com/semantic-release/semantic-release)
[![GitHub license](https://img.shields.io/github/license/populationgenomics/cpg-flow.svg)](https://github.com/populationgenomics/cpg-flow/blob/main/LICENSE)

[![Technical Debt](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=sqale_index&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Duplicated Lines (%)](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=duplicated_lines_density&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Code Smells](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=code_smells&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)

<br />

## 📋 Table of Contents

1. 🐙 [What is this API ?](#what-is-this-api)
2. ✨ [Production and development links](#production-and-development-links)
3. 🔨 [Installation](#installation)
4. 🚀 [Build](#build)
5. 🤖 [Usage](#usage)
6. 😵‍💫 [Key Considerations and Limitations](#key-considerations-and-limitations)
7. 🐳 [Docker](#docker)
8. 💯 [Tests](#tests)
9. ☑️ [Code analysis and consistency](#code-analysis-and-consistency)
10. 📈 [Releases & Changelog](#versions)
11. 🎬 [GitHub Actions](#github-actions)
12. ©️ [License](#license)
13. ❤️ [Contributors](#contributors)

## <a name="what-is-this-api">🐙 What is this API ?</a>

Welcome to CPG Flow!

This API provides a set of tools and workflows for managing population genomics data pipelines, designed to streamline the processing, analysis, and storage of large-scale genomic datasets. It facilitates automated pipeline execution, enabling reproducible research while integrating with cloud-based resources for scalable computation.

CPG Flow supports various stages of genomic data processing, from raw data ingestion to final analysis outputs, making it easier for researchers to manage and scale their population genomics workflows.

The API constructs a DAG (Directed Acyclic Graph) structure from a set of chained stages. This DAG structure then forms the **pipeline**.

## <a name="documentation">✨ Documentation</a>

### 🌐 Production

The production version of this API is documented at **[populationgenomics.github.io/cpg-flow/](https://populationgenomics.github.io/cpg-flow/)**.

The documentation is updated automatically when a commit is pushed on the `alpha` (prerelease) or `main` (release) branch.

## <a name="installation">🔨 Installation</a>

### 🙋‍♀️ User Installation Instructions

The packages are hosted on:

![PyPI](https://img.shields.io/badge/-PyPI-black?style=for-the-badge&logoColor=white&logo=pypi&color=3776AB)

To include `cpg-flow` in your python project simply install either the latest stable version as layed out in the PyPi package page. =

This is as simple as running the following in your project python environment
```bash
pip install cpg-flow
```

For a specific version
```bash
pip install cpg-flow==0.1.2
```

We recommend making the appropriate choice for your individual project. Simply including `cpg-flow` in your dependency management system of choice will install the latest stable relase. But if neccessary you can pin the version. For example in your `pyproject.toml` file simply include the following:
```toml
dependencies = [
    "cpg-flow",         # latest OR
    "cpg-flow==0.1.2",  # pinned version
]
```

### 🛠️ Development Installation Instructions

These instructions are for contributors and developers on the `cpg-flow` project repository. Follow the following steps to setup your environment for development.

To install this project, you will need to have Python and `uv` installed on your machine:

![uv](https://img.shields.io/badge/-uv-black?style=for-the-badge&logoColor=white&logo=uv&color=3776AB&link=https://docs.astral.sh/uv/)
![Python](https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=3776AB)

We use uv for dependency management which can sync your environment locally with the following command:

```bash
# Install the package using uv
uv sync
```

However, to setup for development we recommend using the makefile setup which will do that for you.

```bash
make init-dev # installs pre-commit as a hook
```

#### 📦 Upgrading Packages

To upgrade dependencies in your development environment:

> [!WARNING]
> Always use the `--exclude-newer` flag with a security cutoff date to exclude packages released in the last 7 days, reducing risk of vulnerable releases.

```bash
# Calculate cutoff date and upgrade packages
CUTOFF_DATE=$(python3 -c "from datetime import datetime, timedelta; print((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))")

# Upgrade all packages to their latest compatible versions
uv sync --upgrade --exclude-newer $CUTOFF_DATE

# OR upgrade a specific package
uv sync --upgrade-package <package-name> --exclude-newer $CUTOFF_DATE
```

The `--exclude-newer` flag helps avoid pulling very recent package versions that may contain vulnerabilities or haven't been thoroughly tested. Use a recent date (e.g., a few days or weeks ago) as a safety buffer.

After upgrading packages, ensure all tests pass and pre-commit hooks still work correctly.

#### 🪝 Installing Pre-commit Hooks

Pre-commit hooks help maintain code quality by running checks before each commit. The `make init-dev` command installs these hooks automatically, but you can also install them manually:

```bash
# Install pre-commit hooks for standard checks
uv run pre-commit install

# Install commit message linting hook
uv run pre-commit install --hook-type commit-msg
```

To run pre-commit hooks manually on all files:

```bash
uv run pre-commit run --all-files
```

To install `cpg-flow` locally for testing the code as an editable dependency

```bash
make install-local
```

This will install cpg-flow a an editable dependency in your environment. However, sometimes it can be useful to test the package post-build.
```bash
make install-build
```

This will build and install the package as it would be distributed.

You can confirm which version of cpg-flow is installed by running
```bash
uv pip show cpg-flow
```

For an Editable package it should show the repo location on your machine under the `Editable:` key.
```bash
Name: cpg-flow
Version: 0.1.2
Location: /Users/whoami/cpg-flow/.venv/lib/python3.10/site-packages
Editable project location: /Users/whoami/cpg-flow
Requires: cpg-utils, grpcio, grpcio-status, hail, loguru, ipywidgets, metamist, networkx, plotly, pre-commit, pyyaml
Required-by:
```

The build version (static until you rebuild) will look like the following.
```bash
Name: cpg-flow
Version: 0.1.2
Location: /Users/whoami/cpg-flow/.venv/lib/python3.10/site-packages
Requires: cpg-utils, grpcio, grpcio-status, hail, ipywidgets, loguru, metamist, networkx, plotly, pre-commit, pyyaml
Required-by:
```

To try out the pre-installed `cpg-flow` in a Docker image, find more information in the **[Docker](#docker)** section.

## <a name="build">🚀 Build</a>

To build the project, run the following command:

```bash
make build
```

To make sure that you're actually using the installed build we suggest calling the following to install the build wheel.

```bash
make install-build
```

## <a name="usage">🤖 Usage</a>

This project provides the framework to construct pipelines but does not offer hosting the logic of any pipelines themselves. This approach offers the benefit of making all components more modular, manageable and decoupled. Pipelines themselves are hosted in a separate repository.

The [test_workflows_shared repository](https://github.com/populationgenomics/test_workflows_shared) acts as a template and demonstrates how to structure a pipeline using CPG Flow.

The components required to build pipelines with CPG Flow:

### config `.toml` file

This file contains the configuration settings to your pipeline. This file allows the pipeline developer to define settings such as:

1. what stages will be run or skipped
2. what dataset to use
3. what access level to use
4. any input cohorts
5. sequencing type

```toml
[workflow]
dataset = 'fewgenomes'

# Note: for fewgenomes and sandbox mentioning datasets by name is not a security risk
# DO NOT DO THIS FOR OTHER DATASETS

input_cohorts = ['COH2142']
access_level = 'test'

# Force stage rerun
force_stages = [
    'GeneratePrimes', # the first stage
    'CumulativeCalc', # the second stage
    'FilterEvens', # the third stage
    'BuildAPrimePyramid', # the last stage
]

# Show a workflow graph locally or save to web bucket.
# Default is false, set to true to show the workflow graph.
show_workflow = true
# ...
```

For a full list of supported config options with documentation, see [defaults.toml](src/cpg_flow/defaults.toml)

This `.toml` file will be may be named anything, as long as it is correctly passed to the `analysis-runner` invocation. The `analysis-runner` supplies its own default settings, and combines it with the settings from this file, before submitting a job.

### `main.py` or equivalent entrypoint for the pipeline

This file would store the workflow definition as a list of stages, and then run said workflow:

```python
 import os
 from pathlib import Path
 from cpg_flow.workflow import run_workflow
 from cpg_utils.config import set_config_paths
 from stages import BuildAPrimePyramid, CumulativeCalc, FilterEvens, GeneratePrimes

 CONFIG_FILE = str(Path(__file__).parent / '<YOUR_CONFIG>.toml')

 def run_cpg_flow(dry_run=False):

    #See the 'Key Considerations and Limitations' section for notes on the definition of the `workflow` variable.

    # This represents the flow of the DAG
     workflow = [GeneratePrimes, CumulativeCalc, FilterEvens, BuildAPrimePyramid]

     config_paths = os.environ['CPG_CONFIG_PATH'].split(',')

     # Inserting after the "defaults" config, but before user configs:
     set_config_paths(config_paths[:1] + [CONFIG_FILE] + config_paths[1:])
     run_workflow(stages=workflow, dry_run=dry_run)

 if __name__ == '__main__':
   run_cpg_flow()
```

  The workflow definition here forms a DAG (Directed Acyclic Graph) structure.

  ![DAG](assets/newplot.png)

  > To generate a plot of the DAG, `show_workflow = True` should be included in the config. The DAG plot generated from the pipeline definition is available in the logs via the job URL. To find the link to the plot, search the *Logs* section for the string: "**INFO - Link to the graph:**".

  There are some key considerations and limitations to take into account when designing the DAG:

  - [No Forward Discovery](#no-forward-discovery)
  - [Workflow Definition](#workflow-definition)

### `stages.py` or equivalent file(s) for the `Stage` definitions

A `Stage` represents a node in the DAG. The stages can be abstracted from either a `DatasetStage`, `CohortStage`, `MultiCohortStage`, or a `SequencingGroupStage`.

The stage definition should use the `@stage` decorator to ***optionally*** set:

- dependent stages (this is used to build the DAG)
- analysis keys (this determines what outputs should be written to metamist)
- the analysis type (this determines the analysis-type to be written to metamist)

All stages require an `expected_outputs` class method definition, that sets the expected output path location for a given `Target` such as a `SequencingGroup`, `Dataset`, `Cohort`, or `MultiCohort`.

Also required, is a `queue_jobs` class method definition that calls pipeline jobs, and stores the results of these jobs to the paths defined in `expected_outputs`.

It is good practice to separate the `Stage` definitions into their own files, to keep the code compact, and manageable.

```python
from cpg_flow.stage import SequencingGroupStage, StageInput, StageOutput, stage
from cpg_flow.targets.sequencing_group import SequencingGroup
from jobs import cumulative_calc

WORKFLOW_FOLDER = 'prime_pyramid'

# ...
# This stage depends on the `GeneratePrimes` stage, and requires outputs from that stage.
@stage(required_stages=[GeneratePrimes], analysis_keys=['cumulative'], analysis_type='custom')
class CumulativeCalc(SequencingGroupStage):
 def expected_outputs(self, sequencing_group: SequencingGroup):
     return {
         'cumulative': sequencing_group.dataset.prefix() / WORKFLOW_FOLDER / f'{sequencing_group.id}_cumulative.txt',
     }

 def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
     input_txt = inputs.as_path(sequencing_group, GeneratePrimes, 'primes')
     b = get_batch()

     cumulative_calc_output_path = str(self.expected_outputs(sequencing_group).get('cumulative', ''))

     # We define a job instance from the `cumulative_calc` job definition.
     job_cumulative_calc = cumulative_calc(b, sequencing_group, input_txt, cumulative_calc_output_path)

     jobs = [job_cumulative_calc]

     return self.make_outputs(
         sequencing_group,
         data=self.expected_outputs(sequencing_group),
         jobs=jobs,
     )
# ...
```

There is a key consideration to take into account when writing the stages:

- [No Forward Discovery](#no-forward-discovery)

### `jobs.py` or equivalent file for `Job` definitions

Every `Stage` requires a collection of jobs that will be executed within. It is good practice to store these jobs in their own files, as the definitions can often get long.

```python
from cpg_flow.targets.sequencing_group import SequencingGroup
from hailtop.batch import Batch
from hailtop.batch.job import Job


def cumulative_calc(
    b: Batch,
    sequencing_group: SequencingGroup,
    input_file_path: str,
    output_file_path: str,
) -> list[Job]:
    title = f'Cumulative Calc: {sequencing_group.id}'
    job = b.new_job(name=title)
    primes_path = b.read_input(input_file_path)

    cmd = f"""
    primes=($(cat {primes_path}))
    csum=0
    cumulative=()
    for prime in "${{primes[@]}}"; do
        ((csum += prime))
        cumulative+=("$csum")
    done
    echo "${{cumulative[@]}}" > {job.cumulative}
    """

    job.command(cmd)

    print('-----PRINT CUMULATIVE-----')
    print(output_file_path)
    b.write_output(job.cumulative, output_file_path)

    return job
```

Once these required components are written, the pipeline is ready to be executed against this framework.

### Running the pipeline

All pipelines can only be exclusively run using the [`analysis-runner` package](https://pypi.org/project/analysis-runner/) which grants the user appropriate permissions based on the dataset and access level defined above. `analysis-runner` requires a repo, commit and the entrypoint file, and then runs the code inside a "driver" image on Hail Batch, logging the invocation to `metamist` for future audit and reproducibility.

Therefore, the pipeline code needs to be pushed to a remote version control system, for `analysis-runner` to be able to pull it for execution. A job can then be submitted:

```shell
analysis-runner \
  --image "australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow:1.0.0" \
  --dataset "fewgenomes" \
  --description "cpg-flow_test" \
  --access-level "test" \
  --output-dir "cpg-flow_test" \
  --config "<YOUR_CONFIG>.toml" \
  workflow.py
```

If the job is successfully created, the analysis-runner output will include a job URL. This driver job will trigger additional jobs, which can be monitored via the `/batches` page on Hail. Monitoring these jobs helps verify that the workflow ran successfully. When all expected jobs complete without errors, this confirms the successful execution of the workflow and indicates that the `cpg_flow` package is functioning as intended.

See the [Docker](#docker) section for instruction on pulling valid images releases.

## <a name="key-considerations-and-limitations">😵‍💫 Key Considerations and Limitations</a>

### No Forward Discovery

 The framework exclusively relies on backward traversal. If a stage is not explicitly or indirectly linked to one of the final stages through the `required_stages` parameter of the `@stage` decorator, it will not be included in the workflow. In other words, stages that are not reachable from a final stage are effectively ignored. This backward discovery approach ensures that only the stages directly required for the specified final stages are included, optimizing the workflow by excluding irrelevant or unused stages.

### Workflow Definition

The workflow definition serves as a lookup table for the final stages. If a final stage is not listed in this definition, it will not be part of the workflow, as there is no mechanism for forward discovery to identify it.

```python
workflow = [GeneratePrimes, CumulativeCalc, FilterEvens, BuildAPrimePyramid]
```

### Config Settings for `expected_outputs`

The `expected_outputs` method is called for every stage in the workflow, even if the `config.toml` configures the stage to be skipped. This ensures that the workflow can validate or reference the expected outputs of all stages.

Since this method may depend on workflow-specific configuration settings, these settings must be present in the workflow configuration, regardless of whether the stage will run. To avoid issues, it is common practice to include dummy values for such settings in the default configuration. This is not the intended behaviour and is marked as an area of improvement in a future release.

### Verifying results of `expected_outputs`

The API uses the results of the `expected_outputs` method to determine whether a stage needs to run. A stage is scheduled for execution only if one or more Path objects returned by `expected_outputs` do not exist in Google Cloud Platform (GCP). If a returned Path object exists, the stage is considered to have already run successfully, and is therefore skipped.

For outputs such as Matrix Tables (.mt), Hail Tables (.ht), or Variant Datasets (.vds), which are complex structures of thousands of files, the check is performed on the `object/_SUCCESS` file to verify that the output was written completely. However, it has been observed that the `object/_SUCCESS` file may be written multiple times during processing, contrary to the expectation that it should only be written once after all associated files have been fully processed.

### `String` outputs from `expected_outputs`

String outputs from the `expected_outputs` method are not checked by the API. This is because string outputs cannot reliably be assumed to represent valid file paths and may instead correspond to other forms of outputs.

### Behavior of `queue_jobs` in relation to `expected_outputs`

When the `expected_outputs` check determines that one or more required files do not exist, and the stage is not configured to be skipped, the `queue_jobs` method is invoked to define the specific work that needs to be scheduled in the workflow.

The `queue_jobs` method runs within the driver image, before any jobs in the workflow are executed. Because of this, it cannot access or read files generated by earlier stages, as those outputs have not yet been created. The actual outputs from earlier jobs only become available as the jobs are executed during runtime.

### Explicit dependency between all jobs from `queue_jobs`

When the `queue_jobs` method schedules a collection of jobs to Hail Batch, one or more jobs are returned from the method, and the framework sets an explicit dependency between *these* jobs, and all jobs from the `Stages` set in the `required_stages` parameter. Therefore, all jobs that run in a Stage must be returned within `queue_jobs` to ensure no jobs start out of sequence. As an example:

```python
# test_workflows_shared/cpg_flow_test/jobs/filter_evens.py
def filter_evens(
    b: Batch,
    inputs: StageInput,
    previous_stage: Stage,
    sequencing_groups: list[SequencingGroup],
    input_files: dict[str, dict[str, Any]],
    sg_outputs: dict[str, dict[str, Any]],
    output_file_path: str,
) -> list[Job]:
    title = 'Filter Evens'

    # Compute the no evens list for each sequencing group
    sg_jobs = []
    sg_output_files = []
    for sg in sequencing_groups:  # type: ignore
        job = b.new_job(name=title + ': ' + sg.id)
        ...

        cmd = f"""
        ...
        """

        job.command(cmd)
        b.write_output(job.sg_no_evens_file, no_evens_output_file_path)
        sg_jobs.append(job)

    # Merge the no evens lists for all sequencing groups into a single file
    job = b.new_job(name=title)
    job.depends_on(*sg_jobs)
    inputs = ' '.join([b.read_input(f) for f in sg_output_files])
    job.command(f'cat {inputs} >> {job.no_evens_file}')
    b.write_output(job.no_evens_file, output_file_path)

    # ALL jobs are returned back to `queue_jobs`
    # including new jobs created within this job.
    all_jobs = [job, *sg_jobs]
    return all_jobs
```

## <a name="docker">🐳 Docker</a>


## Docker Image Usage for cpg-flow Python Package

### Pulling and Using the Docker Image

These steps are restricted to CPG members only. Anyone will have access to the code in this public repositry and can build a version of cpg-flow themselves. The following requires authentication with the CPG's GCP.

To pull and use the Docker image for the `cpg-flow` Python package, follow these steps:

1. **Authenticate with Google Cloud Registry**:

    ```sh
    gcloud auth configure-docker australia-southeast1-docker.pkg.dev
    ```

2. **Pull the Docker Image**:
    - For alpha releases:

      ```sh
      docker pull australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow:0.1.0-alpha.11
      ```

    - For main releases:

      ```sh
      docker pull australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow:1.0.0
      ```

3. **Run the Docker Container**:

    ```sh
    docker run -it australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow:<tag>
    ```

### Temporary Images for Development

Temporary images are created for each commit and expire in 30 days. These images are useful for development and testing purposes.

- Example of pulling a temporary image:

  ```sh
  docker pull australia-southeast1-docker.pkg.dev/cpg-common/images-tmp/cpg_flow:991cf5783d7d35dee56a7ab0452d54e69c695c4e
  ```

### Accessing Build Images for CPG Members

Members of the CPG can find the build images in the Google Cloud Registry under the following paths:

- Alpha and main releases: `australia-southeast1-docker.pkg.dev/cpg-common/images/cpg_flow`
- Temporary images: `australia-southeast1-docker.pkg.dev/cpg-common/images-tmp/cpg_flow`

Ensure you have the necessary permissions and are authenticated with Google Cloud to access these images.

### <a name="tests">🧪 Unit and E2E tests</a>

#### Unit Tests

Unit tests are run in the [Test CI workflow](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml) for each branch.

#### E2E Test

We recommend frequently running the manual test workflow found in [test_workflows_shared](https://github.com/populationgenomics/test_workflows_shared)  specifically the `cpg_flow_test` workflow during development to ensure updates work with the CPG production environment.

Docummentation for running the tests are found in the repository readme.


### ▶️ Commands

Before testing, you must follow the **[installation steps](#installation)**.

## <a name="code-analysis-and-consistency">☑️ Code analysis and consistency</a>

### 🔍 Code linting & formatting

![Precommit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

In order to keep the code clean, consistent and free of bad python practices, more than **Over 10 pre-commit hooks are enabled** !

Complete list of all enabled rules is available in the **[.pre-commit-config.yaml file](https://github.com/populationgenomics/cpg-flow/blob/main/.pre-commit-config.yaml)**.

### ▶️ Commands

Before linting, you must follow the [installation steps](#installation).

Then, run the following command

```bash
# Lint
pre-commit run --all-files
```

When setting up local linting for development you can also run the following once:

```bash
# Install the pre-commit hook
pre-commit install

# Or equivalently
make init || make init-dev
```

### 🥇 Project quality scanner

Multiple tools are set up to maintain the best code quality and to prevent vulnerabilities:

![SonarQube](https://img.shields.io/badge/-SonarQube-black?style=for-the-badge&logoColor=white&logo=sonarqube&color=4E9BCD)

SonarQube summary is available **[here](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)**.

[![Coverage](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=coverage&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Duplicated Lines (%)](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=duplicated_lines_density&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Quality Gate Status](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=alert_status&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)

[![Technical Debt](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=sqale_index&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Vulnerabilities](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=vulnerabilities&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Code Smells](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=code_smells&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)

[![Reliability Rating](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=reliability_rating&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Security Rating](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=security_rating&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)
[![Bugs](https://sonarqube.populationgenomics.org.au/api/project_badges/measure?project=populationgenomics_cpg-flow&metric=bugs&token=sqb_bd2c5ce00628492c0af714f727ef6f8e939d235c)](https://sonarqube.populationgenomics.org.au/dashboard?id=populationgenomics_cpg-flow)


## <a name="versions">📈 Releases & Changelog</a>

Releases on **main** branch are generated and published automatically,
pre-releases on the **alpha** branch are also generated and published by:

![Semantic Release](https://img.shields.io/badge/-Semantic%20Release-black?style=for-the-badge&logoColor=white&logo=semantic-release&color=000000)

It uses the **[conventional commit](https://www.conventionalcommits.org/en/v1.0.0/)** strategy.

This is enforced using the **[commitlint](https://github.com/opensource-nepal/commitlint)** pre-commit hook that checks commit messages conform to the conventional commit standard.

We recommend installing and using the tool **[commitizen](https://commitizen-tools.github.io/commitizen/) in order to create commit messages. Once installed, you can use either `cz commit` or `git cz` to create a commitizen generated commit message.

Each change when a new release comes up is listed in the **<a href="https://github.com/populationgenomics/cpg-flow/blob/main/CHANGELOG.md" target="_blank">CHANGELOG.md file</a>**.

Also, you can keep up with changes by watching releases via the **Watch GitHub button** at the top of this page.

#### 🏷️ <a href="https://github.com/populationgenomics/cpg-flow/releases" target="_blank">All releases for this project are available here</a>.

## <a name="github-actions">🎬 GitHub Actions</a>

This project uses **GitHub Actions** to automate some boring tasks.

You can find all the workflows in the **[.github/workflows directory](https://github.com/populationgenomics/cpg-flow/tree/main/.github/workflows).**

### 🎢 Workflows

|                                                   Name                                                   |                                                                                                                        Description & Status                                                                                                                         |                                    Triggered on                                     |
| :------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------: |
|        **[Docker](https://github.com/populationgenomics/cpg-flow/actions/workflows/docker.yaml)**        |             Builds and pushes Docker images for the project.<br/><br/>[![Docker](https://github.com/populationgenomics/cpg-flow/actions/workflows/docker.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/docker.yaml)             | `pull_request` on `main, alpha` and `push` on `main, alpha` and `workflow_dispatch` |
|          **[Lint](https://github.com/populationgenomics/cpg-flow/actions/workflows/lint.yaml)**          |                  Runs linting checks using pre-commit hooks.<br/><br/>[![Lint](https://github.com/populationgenomics/cpg-flow/actions/workflows/lint.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/lint.yaml)                   |                                       `push`                                        |
|       **[Package](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml)**       |  Packages the project and publishes it to PyPI and GitHub Releases.<br/><br/>[![Package](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/package.yaml)   |                               `push` on `main, alpha`                               |
|      **[Renovate](https://github.com/populationgenomics/cpg-flow/actions/workflows/renovate.yaml)**      |               Runs Renovate to update dependencies.<br/><br/>[![Renovate](https://github.com/populationgenomics/cpg-flow/actions/workflows/renovate.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/renovate.yaml)                |                         `schedule` and `workflow_dispatch`                          |
|  **[Security Checks](https://github.com/populationgenomics/cpg-flow/actions/workflows/security.yaml)**   |          Performs security checks using pip-audit.<br/><br/>[![Security Checks](https://github.com/populationgenomics/cpg-flow/actions/workflows/security.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/security.yaml)          |                           `workflow_dispatch` and `push`                            |
|          **[Test](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml)**          |                Runs unit tests and generates coverage reports.<br/><br/>[![Test](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/test.yaml)                 |                                       `push`                                        |
| **[Update Badges](https://github.com/populationgenomics/cpg-flow/actions/workflows/update-badges.yaml)** | Updates badges.yaml with test results and coverage.<br/><br/>[![Update Badges](https://github.com/populationgenomics/cpg-flow/actions/workflows/update-badges.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/update-badges.yaml) |                             `workflow_run` (completed)                              |
|       **[mkdocs](https://github.com/populationgenomics/cpg-flow/actions/workflows/web-docs.yaml)**       |              Deploys API documentation to GitHub Pages.<br/><br/>[![mkdocs](https://github.com/populationgenomics/cpg-flow/actions/workflows/web-docs.yaml/badge.svg)](https://github.com/populationgenomics/cpg-flow/actions/workflows/web-docs.yaml)              |                                  `push` on `alpha`                                  |


## <a name="license">©️ License</a>

This project is licensed under the [MIT License](http://opensource.org/licenses/MIT).

## <a name="contributors">❤️ Contributors</a>

There is no contributor yet. Want to be the first ?

If you want to contribute to this project, please read the [**contribution guide**](https://github.com/populationgenomics/cpg-flow/blob/master/CONTRIBUTING.md).
