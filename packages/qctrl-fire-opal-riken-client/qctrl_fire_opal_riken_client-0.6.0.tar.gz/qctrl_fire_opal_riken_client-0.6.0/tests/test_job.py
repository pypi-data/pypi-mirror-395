"""
Unit tests for FireOpalJob.
"""

import logging
from unittest.mock import Mock

import pytest
from qiskit_ibm_runtime.runtime_job_v2 import RuntimeJobV2

from fireopalrikenclient.tests.conftest import MockFireOpalClient
from fireopalrikenclient.utils.job import FireOpalJob
from fireopalrikencommons.protos import compute_service_pb2


@pytest.mark.parametrize(
    "task_type",
    [
        compute_service_pb2.TaskType.TASK_TYPE_SAMPLER,
        compute_service_pb2.TaskType.TASK_TYPE_ESTIMATOR,
    ],
)
def test_from_qiskit_job_modifies_job_with_fire_opal_result(
    mock_client: MockFireOpalClient,
    mock_sampler_runtime_job: RuntimeJobV2,
    task_type: compute_service_pb2.TaskType,
) -> None:
    """Test that from_qiskit_job modifies a job with Fire Opal result method."""
    task_id = "test_task_123"

    # Store original result method for comparison
    original_result = mock_sampler_runtime_job.result

    # Modify job with FireOpal capabilities
    modified_job = FireOpalJob.from_qiskit_job(
        job=mock_sampler_runtime_job,
        task_id=task_id,
        task_type=task_type,
        grpc_client=mock_client,
    )

    # Verify it returns the same job instance, not a FireOpalJob instance
    assert modified_job is mock_sampler_runtime_job
    assert isinstance(modified_job, RuntimeJobV2)
    assert not isinstance(modified_job, FireOpalJob)

    # Verify the result method was replaced with Fire Opal version
    assert modified_job.result is not original_result

    # Verify original job attributes are preserved
    assert modified_job.job_id() == mock_sampler_runtime_job.job_id()
    assert modified_job.status() == mock_sampler_runtime_job.status()
    assert modified_job._backend is mock_sampler_runtime_job._backend
    assert modified_job._service is mock_sampler_runtime_job._service


@pytest.mark.parametrize(
    "task_type,results_fixture",
    [
        (
            compute_service_pb2.TaskType.TASK_TYPE_SAMPLER,
            "sample_job_results",
        ),
        (
            compute_service_pb2.TaskType.TASK_TYPE_ESTIMATOR,
            "sample_estimator_job_results",
        ),
    ],
)
def test_result_calls_postprocessing_and_returns_results(
    mock_client: MockFireOpalClient,
    mock_sampler_runtime_job: RuntimeJobV2,
    task_type: compute_service_pb2.TaskType,
    results_fixture: str,
    caplog: pytest.LogCaptureFixture,
    request: pytest.FixtureRequest,
) -> None:
    """Test that result method calls postprocessing and returns processed results."""
    job_results = request.getfixturevalue(results_fixture)

    # Setup mock for the original result method
    original_result_mock = Mock(return_value=job_results)
    mock_sampler_runtime_job.result = original_result_mock
    task_id = "test_task_456"

    # Modify job with FireOpal capabilities
    modified_job = FireOpalJob.from_qiskit_job(
        job=mock_sampler_runtime_job,
        task_id=task_id,
        task_type=task_type,
        grpc_client=mock_client,
    )

    # Call result method
    with caplog.at_level(logging.INFO):
        results = modified_job.result()

    # Verify original result() was called
    original_result_mock.assert_called_once()

    # Verify postprocessing was called
    assert len(mock_client.postprocessing_calls) == 1
    postprocessing_request = mock_client.postprocessing_calls[0]
    assert postprocessing_request.task_id == task_id

    # Verify results are returned
    assert isinstance(results, list)
    assert len(results) == len(job_results)

    # Verify appropriate logging occurred
    log_messages = [record.message for record in caplog.records]
    assert any("Results received from device" in msg for msg in log_messages)
    assert any(
        "Calling Fire Opal post-processing gRPC task" in msg for msg in log_messages
    )
    assert any(
        f"Fire Opal job '{task_id}' completed successfully" in msg
        for msg in log_messages
    )


@pytest.mark.parametrize(
    "task_type",
    [
        compute_service_pb2.TaskType.TASK_TYPE_SAMPLER,
        compute_service_pb2.TaskType.TASK_TYPE_ESTIMATOR,
    ],
)
def test_result_handles_device_failure(
    mock_client: MockFireOpalClient,
    mock_sampler_runtime_job: RuntimeJobV2,
    task_type: compute_service_pb2.TaskType,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that result method handles device execution failures."""

    # Setup mock to raise exception
    original_result_mock = Mock(side_effect=Exception("Device execution failed"))
    mock_sampler_runtime_job.result = original_result_mock
    task_id = "test_task_error"

    # Modify job with FireOpal capabilities
    modified_job = FireOpalJob.from_qiskit_job(
        job=mock_sampler_runtime_job,
        task_id=task_id,
        task_type=task_type,
        grpc_client=mock_client,
    )

    # Verify exception is re-raised and logged
    with caplog.at_level(logging.ERROR):
        with pytest.raises(Exception, match="Device execution failed"):
            modified_job.result()

    # Verify error was logged
    log_messages = [record.message for record in caplog.records]
    assert any(
        f"Failed to retrieve results for task '{task_id}'" in msg
        for msg in log_messages
    )

    # Verify postprocessing was not called since device failed
    assert len(mock_client.postprocessing_calls) == 0


@pytest.mark.parametrize(
    "task_type,results_fixture",
    [
        (
            compute_service_pb2.TaskType.TASK_TYPE_SAMPLER,
            "sample_job_results",
        ),
        (
            compute_service_pb2.TaskType.TASK_TYPE_ESTIMATOR,
            "sample_estimator_job_results",
        ),
    ],
)
def test_result_caches_post_processed_results(
    mock_client: MockFireOpalClient,
    mock_sampler_runtime_job: RuntimeJobV2,
    task_type: compute_service_pb2.TaskType,
    results_fixture: str,
    request: pytest.FixtureRequest,
) -> None:
    """Test that result method caches post-processed results for subsequent calls."""
    job_results = request.getfixturevalue(results_fixture)

    # Setup mocks
    original_result_mock = Mock(return_value=job_results)
    mock_sampler_runtime_job.result = original_result_mock
    task_id = "test_task_cache"

    # Modify job with FireOpal capabilities
    modified_job = FireOpalJob.from_qiskit_job(
        job=mock_sampler_runtime_job,
        task_id=task_id,
        task_type=task_type,
        grpc_client=mock_client,
    )

    # First call to result() - should perform full processing
    results_1 = modified_job.result()

    # Verify postprocessing was called once
    assert len(mock_client.postprocessing_calls) == 1
    assert original_result_mock.call_count == 1

    # Second call to result() - should return cached results
    results_2 = modified_job.result()

    # Verify postprocessing was NOT called again (still only 1 call)
    assert len(mock_client.postprocessing_calls) == 1
    # Verify original result() was NOT called again (still only 1 call)
    assert original_result_mock.call_count == 1

    # Verify same results are returned (shows caching is working)
    assert results_2 is results_1
    assert results_2 == results_1
