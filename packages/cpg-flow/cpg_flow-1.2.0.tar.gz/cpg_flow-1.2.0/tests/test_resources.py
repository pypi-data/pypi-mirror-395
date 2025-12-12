import pytest

from cpg_flow.resources import (
    Job,
    JobResource,
    MachineType,
    gcp_machine_name,
    is_power_of_two,
    storage_for_cram_qc_job,
    storage_for_joint_vcf,
)


# Mock Job class for testing
class MockJob(Job):
    def __init__(self):
        self.resources = {}

    def storage(self, storage):
        self.resources['storage'] = storage
        return self

    def cpu(self, cores):
        self.resources['cpu'] = cores
        return self

    def memory(self, memory):
        self.resources['memory'] = memory
        return self


def test_is_power_of_two():
    assert is_power_of_two(1) is True
    assert is_power_of_two(2) is True
    assert is_power_of_two(4) is True
    assert is_power_of_two(3) is False
    assert is_power_of_two(5) is False


def test_gcp_machine_name():
    assert gcp_machine_name('standard', 4) == 'n1-standard-4'
    assert gcp_machine_name('highmem', 8) == 'n1-highmem-8'
    with pytest.raises(AssertionError):
        gcp_machine_name('invalid', 4)
    with pytest.raises(AssertionError):
        gcp_machine_name('standard', 3)  # Not a power of two


def test_machine_type_request_resources():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    resource = machine.request_resources(ncpu=4)
    assert resource.get_ncpu() == 4
    assert resource.get_mem_gb() == pytest.approx(4 * 3.75)


def test_machine_type_adjust_ncpu():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    assert machine.adjust_ncpu(3) == 4  # Rounded to nearest power of 2
    assert machine.adjust_ncpu(16) == 16
    with pytest.raises(ValueError):
        machine.adjust_ncpu(32)  # Exceeds max_ncpu


def test_job_resource_set_to_job():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    resource = machine.request_resources(ncpu=4)
    mock_job = MockJob()
    resource.set_to_job(mock_job)

    assert mock_job.resources['cpu'] == 4
    assert mock_job.resources['memory'] == f'{4 * 3.75}G'
    assert 'storage' in mock_job.resources


def test_job_resource_java_mem_options():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    resource = machine.request_resources(ncpu=4)
    java_options = resource.java_mem_options(overhead_gb=1)
    assert '-Xms' in java_options
    assert '-Xmx' in java_options


def test_job_resource_java_gc_thread_options():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    resource = machine.request_resources(ncpu=4)
    gc_options = resource.java_gc_thread_options(surplus=1)
    assert '-XX:+UseParallelGC' in gc_options
    assert 'ParallelGCThreads=3' in gc_options  # 4 CPUs - 1 surplus


def test_storage_for_cram_qc_job(mocker):
    mocker.patch('cpg_flow.resources.get_config', return_value={'workflow': {'sequencing_type': 'genome'}})
    assert storage_for_cram_qc_job() == 100

    mocker.patch('cpg_flow.resources.get_config', return_value={'workflow': {'sequencing_type': 'exome'}})
    assert storage_for_cram_qc_job() == 20


def test_storage_for_joint_vcf(mocker):
    mocker.patch('cpg_flow.resources.get_config', return_value={'workflow': {'sequencing_type': 'genome'}})
    assert storage_for_joint_vcf(1000) == pytest.approx(1000.0)
    assert storage_for_joint_vcf(1000, site_only=False) == pytest.approx(1500.0)

    mocker.patch('cpg_flow.resources.get_config', return_value={'workflow': {'sequencing_type': 'exome'}})
    assert storage_for_joint_vcf(1000) == pytest.approx(100.0)


def test_job_resource_get_mem_gb():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    resource = JobResource(machine_type=machine, ncpu=4)
    assert resource.get_mem_gb() == pytest.approx(4 * 3.75)


def test_job_resource_get_ncpu():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    resource = JobResource(machine_type=machine, ncpu=8)
    assert resource.get_ncpu() == 8


def test_job_resource_get_nthreads():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    resource = JobResource(machine_type=machine, ncpu=4)
    assert resource.get_nthreads() == 4  # threads_on_cpu is 1


def test_job_resource_get_storage_gb():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    resource = JobResource(machine_type=machine, ncpu=4)
    assert resource.get_storage_gb() > 0  # Ensure storage is calculated correctly


def test_job_resource_invalid_storage_override():
    machine = MachineType('standard', ncpu=16, mem_gb_per_core=3.75, price_per_hour=1.0, disk_size_gb=375)
    with pytest.raises(ValueError):
        JobResource(machine_type=machine, ncpu=4, attach_disk_storage_gb=500)  # Invalid override for partial machine
