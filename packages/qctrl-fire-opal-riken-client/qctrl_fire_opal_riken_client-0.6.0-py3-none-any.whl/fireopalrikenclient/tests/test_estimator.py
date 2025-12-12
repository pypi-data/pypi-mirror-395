"""
Unit tests for FireOpalEstimator.
"""

import logging
from unittest.mock import Mock, patch

import pytest
from qiskit.primitives.containers.pub_result import PubResult
from qiskit_ibm_runtime.base_primitive import EstimatorPub
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit_ibm_runtime.runtime_job_v2 import RuntimeJobV2

from fireopalrikenclient.estimator import FireOpalEstimator
from fireopalrikenclient.tests.conftest import MockFireOpalClient


@patch("fireopalrikenclient.estimator.FireOpalClient")
def test_estimator_initialization(mock_fire_opal_client_class: Mock) -> None:
    """Test that FireOpalEstimator initializes correctly."""
    # Setup mock
    mock_client_instance = Mock()
    mock_fire_opal_client_class.return_value = mock_client_instance

    fake_backend = FakeFez()
    estimator = FireOpalEstimator(mode=fake_backend)

    assert estimator._grpc_client is mock_client_instance
    mock_fire_opal_client_class.assert_called_once()
    mock_client_instance.connect.assert_called_once()
    assert isinstance(estimator, FireOpalEstimator)


@patch("fireopalrikenclient.utils.job.RuntimeJobV2.result")
@patch("fireopalrikenclient.estimator.SamplerV2._run")
@patch("fireopalrikenclient.estimator.FireOpalClient")
def test_estimator_run(
    mock_fire_opal_client_class: Mock,
    mock_sampler_run: Mock,
    mock_job_result_super_run: Mock,
    sample_estimator_pubs: list[EstimatorPub],
    mock_estimator_runtime_job: RuntimeJobV2,
    sample_estimator_job_results: list[PubResult],
) -> None:
    """Test successful execution path of _run method."""
    # Setup FireOpalClient mock
    mock_client = MockFireOpalClient()
    mock_fire_opal_client_class.return_value = mock_client

    # Setup other mocks
    mock_sampler_run.return_value = mock_estimator_runtime_job
    mock_job_result_super_run.return_value = sample_estimator_job_results

    fake_backend = FakeFez()
    estimator = FireOpalEstimator(mode=fake_backend)

    # Call _run directly with EstimatorPub objects
    fire_opal_job = estimator._run(sample_estimator_pubs)

    assert isinstance(fire_opal_job, RuntimeJobV2)

    # Verify calls were made during preprocessing
    assert len(mock_client.preprocessing_calls) == 1

    # Verify preprocessing request
    preprocessing_request = mock_client.preprocessing_calls[0]
    assert preprocessing_request.task_id is not None
    assert preprocessing_request.pubs is not None

    # Verify SamplerV2._run was called
    mock_sampler_run.assert_called_once()

    # Now call result() on the FireOpalJob to trigger postprocessing
    results = fire_opal_job.result()

    # Verify postprocessing was called
    assert len(mock_client.postprocessing_calls) == 1
    postprocessing_request = mock_client.postprocessing_calls[0]
    assert postprocessing_request.task_id == preprocessing_request.task_id

    # Verify we get estimator results back in the correct form
    for result in results:
        assert isinstance(result, PubResult)
        assert hasattr(result.data, "evs")
        assert hasattr(result.data, "stds")
    assert len(results) == len(sample_estimator_job_results)


@patch("fireopalrikenclient.estimator.SamplerV2._run")
@patch("fireopalrikenclient.estimator.FireOpalClient")
def test_run_with_device_failure(
    mock_fire_opal_client_class: Mock,
    mock_sampler_run: Mock,
    sample_estimator_pubs: list[EstimatorPub],
) -> None:
    """Test _run method handles device execution failures."""
    # Setup FireOpalClient mock
    mock_client = MockFireOpalClient()
    mock_fire_opal_client_class.return_value = mock_client

    # Setup mock to raise exception
    fake_backend = FakeFez()
    mock_sampler_run.side_effect = Exception("Device execution failed")

    estimator = FireOpalEstimator(mode=fake_backend)

    # Verify exception is re-raised
    with pytest.raises(Exception, match="Device execution failed"):
        estimator._run(sample_estimator_pubs)

    # Verify preprocessing was called but postprocessing was not
    assert len(mock_client.preprocessing_calls) == 1
    assert len(mock_client.postprocessing_calls) == 0


@patch("fireopalrikenclient.utils.job.RuntimeJobV2.result")
@patch("fireopalrikenclient.estimator.SamplerV2._run")
@patch("fireopalrikenclient.estimator.FireOpalClient")
def test_logging_behavior(
    mock_fire_opal_client_class: Mock,
    mock_sampler_run: Mock,
    mock_job_result_super_run: Mock,
    sample_estimator_pubs: list[EstimatorPub],
    mock_estimator_runtime_job: RuntimeJobV2,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that appropriate logging occurs during execution."""
    # Setup FireOpalClient mock
    mock_client = MockFireOpalClient()
    mock_fire_opal_client_class.return_value = mock_client

    # Setup other mocks
    mock_sampler_run.return_value = mock_estimator_runtime_job
    mock_job_result_super_run.return_value = []

    fake_backend = FakeFez()
    estimator = FireOpalEstimator(mode=fake_backend)

    with caplog.at_level(logging.INFO):
        fire_opal_job = estimator._run(sample_estimator_pubs)
        # Call result to trigger postprocessing and more logging
        fire_opal_job.result()

    # Check that logging occurred
    log_messages = [record.message for record in caplog.records]
    assert any("Starting FireOpal estimator run" in msg for msg in log_messages)
    assert any("Mock preprocessing called" in msg for msg in log_messages)
    assert any("Mock postprocessing called" in msg for msg in log_messages)
