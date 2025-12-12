"""
Unit tests for FireOpalClient gRPC implementation.
"""

from unittest.mock import Mock, patch

import grpc
import pytest
from qiskit.primitives.containers import SamplerPubResult
from qiskit_ibm_runtime.base_primitive import SamplerPub
from qiskit_ibm_runtime.fake_provider import FakeFez

from fireopalrikenclient.sampler import FireOpalSampler
from fireopalrikenclient.tests.conftest import MockComputeServiceStub
from fireopalrikenclient.utils.client import FireOpalClient
from fireopalrikencommons.protos import compute_service_pb2


def test_fire_opal_client_initialization(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that FireOpalClient initializes correctly."""
    monkeypatch.setenv("FIRE_OPAL_GRPC_SERVER_ADDRESS", "test-server:8080")
    client = FireOpalClient()
    assert client.server_address == "test-server:8080"
    assert client.channel is None
    assert client.stub is None


@patch("fireopalrikenclient.utils.client.grpc.insecure_channel")
@patch("fireopalrikenclient.utils.client.ComputeServiceStub")
def test_fire_opal_client_connect(
    mock_stub_class: Mock,
    mock_channel: Mock,
    mock_compute_service_stub: MockComputeServiceStub,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test client connection."""
    # Setup mocks
    monkeypatch.setenv("FIRE_OPAL_GRPC_SERVER_ADDRESS", "test-server:8080")
    mock_channel_instance = Mock()
    mock_channel.return_value = mock_channel_instance
    mock_stub_class.return_value = mock_compute_service_stub

    client = FireOpalClient()
    client.connect()

    # Verify connection was established
    assert client.channel is mock_channel_instance
    assert client.stub is mock_compute_service_stub
    mock_channel.assert_called_once()
    mock_stub_class.assert_called_once_with(mock_channel_instance)


def test_fire_opal_client_close() -> None:
    """Test client disconnection."""
    client = FireOpalClient()

    # Mock a connected state
    mock_channel = Mock()
    client.channel = mock_channel
    client.stub = Mock()

    client.close()

    # Verify disconnection
    assert client.channel is None
    assert client.stub is None
    mock_channel.close.assert_called_once()


@patch("fireopalrikenclient.utils.client.grpc.insecure_channel")
@patch("fireopalrikenclient.utils.client.ComputeServiceStub")
def test_fire_opal_client_context_manager(
    mock_stub_class: Mock,
    mock_channel: Mock,
    mock_compute_service_stub: MockComputeServiceStub,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test client as context manager."""
    mock_channel_instance = Mock()
    mock_channel.return_value = mock_channel_instance
    mock_stub_class.return_value = mock_compute_service_stub

    monkeypatch.setenv("FIRE_OPAL_GRPC_SERVER_ADDRESS", "test-server:8080")
    with FireOpalClient() as client:
        # Verify connection is established
        assert client.channel is mock_channel_instance
        assert client.stub is mock_compute_service_stub

    # Verify connection is closed after context
    mock_channel_instance.close.assert_called_once()


@patch("fireopalrikenclient.utils.client.grpc.insecure_channel")
@patch("fireopalrikenclient.utils.client.ComputeServiceStub")
def test_preprocess_circuits_success(
    mock_stub_class: Mock,
    mock_channel: Mock,
    mock_compute_service_stub: MockComputeServiceStub,
) -> None:
    """Test successful preprocessing call."""
    # Setup mocks
    mock_channel.return_value = Mock()
    mock_stub_class.return_value = mock_compute_service_stub

    client = FireOpalClient()
    client.connect()

    # Create request
    request = compute_service_pb2.PreprocessingRequest()
    request.task_id = "test-task-123"
    request.pubs = '{"test": "data"}'

    # Call preprocessing
    response = client.preprocess_circuits(request)

    # Verify response
    assert response.task_id == "test-task-123"
    assert response.success is True
    assert response.pubs == '{"test": "data"}'
    assert len(mock_compute_service_stub.preprocessing_calls) == 1


@patch("fireopalrikenclient.utils.client.grpc.insecure_channel")
@patch("fireopalrikenclient.utils.client.ComputeServiceStub")
def test_postprocess_results_success(
    mock_stub_class: Mock,
    mock_channel: Mock,
    mock_compute_service_stub: MockComputeServiceStub,
) -> None:
    """Test successful postprocessing call."""
    # Setup mocks
    mock_channel.return_value = Mock()
    mock_stub_class.return_value = mock_compute_service_stub

    client = FireOpalClient()
    client.connect()

    # Create request
    request = compute_service_pb2.PostprocessingRequest()
    request.task_id = "test-task-456"
    request.pub_results = '{"results": "data"}'

    # Call postprocessing
    response = client.postprocess_results(request)

    # Verify response
    assert response.task_id == "test-task-456"
    assert response.success is True
    assert response.results == '{"results": "data"}'
    assert len(mock_compute_service_stub.postprocessing_calls) == 1


def test_client_not_connected_error() -> None:
    """Test error when trying to use client without connecting."""
    client = FireOpalClient()

    request = compute_service_pb2.PreprocessingRequest()

    with pytest.raises(RuntimeError, match="Client not connected"):
        client.preprocess_circuits(request)

    with pytest.raises(RuntimeError, match="Client not connected"):
        client.postprocess_results(compute_service_pb2.PostprocessingRequest())


@patch("fireopalrikenclient.utils.client.grpc.insecure_channel")
@patch("fireopalrikenclient.utils.client.ComputeServiceStub")
def test_grpc_error_handling(mock_stub_class: Mock, mock_channel: Mock) -> None:
    """Test error handling for gRPC failures."""
    # Setup mocks
    mock_channel.return_value = Mock()
    mock_stub = Mock()
    mock_stub.PreprocessCircuits.side_effect = grpc.RpcError("Connection failed")
    mock_stub_class.return_value = mock_stub

    client = FireOpalClient()
    client.connect()

    # Create request
    request = compute_service_pb2.PreprocessingRequest()
    request.task_id = "test-task-error"

    # Call preprocessing - should handle error gracefully
    response = client.preprocess_circuits(request)

    # Verify error response
    assert response.task_id == "test-task-error"
    assert response.success is False
    assert "gRPC error" in response.error_message


@patch("fireopalrikenclient.utils.client.grpc.insecure_channel")
@patch("fireopalrikenclient.utils.client.ComputeServiceStub")
@patch("fireopalrikenclient.sampler.SamplerV2._run")
def test_fire_opal_client_with_sampler_integration(
    mock_super_run: Mock,
    mock_stub_class: Mock,
    mock_channel: Mock,
    sample_pubs: list[SamplerPub],
    sample_job_results: list[SamplerPubResult],
    mock_compute_service_stub: MockComputeServiceStub,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test FireOpalClient integration with FireOpalSampler."""
    # Setup mocks for gRPC client
    mock_channel.return_value = Mock()
    mock_stub_class.return_value = mock_compute_service_stub

    # Setup mock runtime job
    mock_runtime_job = Mock()
    mock_runtime_job.result.return_value = sample_job_results
    mock_super_run.return_value = mock_runtime_job

    # Create real FireOpalClient and connect it
    monkeypatch.setenv("FIRE_OPAL_GRPC_SERVER_ADDRESS", "test-server:8080")

    fake_backend = FakeFez()
    sampler = FireOpalSampler(mode=fake_backend)

    # Run sampler - use just the circuits from the pubs
    circuits = [pub.circuit for pub in sample_pubs]
    sampler.run(circuits)

    # Verify gRPC calls were made
    assert len(mock_compute_service_stub.preprocessing_calls) == 1
    preprocessing_request = mock_compute_service_stub.preprocessing_calls[0]
    assert preprocessing_request.task_id is not None
