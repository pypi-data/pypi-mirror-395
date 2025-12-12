"""
Test fixtures for FireOpalSampler tests.
"""

import logging
from unittest.mock import Mock

import pytest
from qiskit import QuantumCircuit
from qiskit.primitives.containers import SamplerPubResult
from qiskit.primitives.containers.bit_array import BitArray
from qiskit.primitives.containers.data_bin import DataBin
from qiskit_ibm_runtime.base_primitive import SamplerPub
from qiskit_ibm_runtime.runtime_job_v2 import RuntimeJobV2

from fireopalrikenclient.utils.client import FireOpalClientInterface
from fireopalrikencommons.protos import compute_service_pb2


class MockComputeServiceStub:
    """Mock gRPC stub for testing."""

    def __init__(self) -> None:
        self.preprocessing_calls: list[compute_service_pb2.PreprocessingRequest] = []
        self.postprocessing_calls: list[compute_service_pb2.PostprocessingRequest] = []

    def PreprocessCircuits(  # noqa: N802
        self, request: compute_service_pb2.PreprocessingRequest
    ) -> compute_service_pb2.PreprocessingResponse:
        """Mock preprocessing call."""
        self.preprocessing_calls.append(request)
        response = compute_service_pb2.PreprocessingResponse()
        response.task_id = request.task_id
        response.success = True
        response.pubs = request.pubs  # Echo back
        response.error_message = ""
        return response

    def PostprocessResults(  # noqa: N802
        self, request: compute_service_pb2.PostprocessingRequest
    ) -> compute_service_pb2.PostprocessingResponse:
        """Mock postprocessing call."""
        self.postprocessing_calls.append(request)
        response = compute_service_pb2.PostprocessingResponse()
        response.task_id = request.task_id
        response.success = True
        response.results = request.pub_results  # Echo back
        response.error_message = ""
        return response


class MockFireOpalClient(FireOpalClientInterface):
    """
    Mock Fire Opal client for testing.

    This client logs basic info and returns lightweight test results.
    """

    def __init__(self) -> None:
        """Initialize the mock client."""
        self.logger = logging.getLogger(__name__)
        self.preprocessing_calls: list[compute_service_pb2.PreprocessingRequest] = []
        self.postprocessing_calls: list[compute_service_pb2.PostprocessingRequest] = []

    def preprocess_circuits(
        self, request: compute_service_pb2.PreprocessingRequest
    ) -> compute_service_pb2.PreprocessingResponse:
        """
        Mock preprocessing that logs calls and returns test data.
        """
        self.logger.info("Mock preprocessing called for task: %s", request.task_id)
        self.preprocessing_calls.append(request)

        # Return the same pubs as received (no optimization in mock)
        return compute_service_pb2.PreprocessingResponse(
            task_id=request.task_id,
            success=True,
            pubs=request.pubs,  # Echo back the input pubs
            error_message="",
        )

    def postprocess_results(
        self, request: compute_service_pb2.PostprocessingRequest
    ) -> compute_service_pb2.PostprocessingResponse:
        """
        Mock postprocessing that logs calls and returns test data.
        """
        self.logger.info("Mock postprocessing called for task: %s", request.task_id)
        self.postprocessing_calls.append(request)

        # Return the same results as received (no error mitigation in mock)
        return compute_service_pb2.PostprocessingResponse(
            task_id=request.task_id,
            success=True,
            results=request.pub_results,  # Echo back the input results
            error_message="",
        )

    def close(self) -> None:
        """
        Mock close method.
        """
        self.logger.info("Mock client closed")

    def connect(self) -> None:
        """
        Mock connect method.
        """
        self.logger.info("Mock client connected")


@pytest.fixture
def mock_client() -> MockFireOpalClient:
    """Fixture providing a mock Fire Opal client."""
    return MockFireOpalClient()


@pytest.fixture
def mock_compute_service_stub() -> MockComputeServiceStub:
    """Fixture providing a mock gRPC compute service stub."""
    return MockComputeServiceStub()


@pytest.fixture
def sample_circuit() -> QuantumCircuit:
    """Fixture providing a sample quantum circuit."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    return circuit


@pytest.fixture
def sample_pubs(sample_circuit: QuantumCircuit) -> list[SamplerPub]:
    """Fixture providing sample SamplerPub objects."""
    return [SamplerPub(sample_circuit, shots=1024)]


@pytest.fixture
def sample_job_results() -> list[SamplerPubResult]:
    """Fixture providing sample SamplerPubResult objects."""
    return [SamplerPubResult(DataBin(meas=BitArray.from_samples(["00", "11"])))]


@pytest.fixture
def mock_runtime_job(sample_job_results: list[SamplerPubResult]) -> RuntimeJobV2:
    """Fixture providing a mock RuntimeJobV2 object with all required attributes."""
    mock_job = Mock(spec=RuntimeJobV2)
    mock_job.wait_for_final_state.return_value = None
    mock_job.result.return_value = sample_job_results
    mock_job.job_id.return_value = "test_job_123"
    mock_job.status.return_value = "DONE"

    # Add all the private attributes that FireOpalJob.from_runtime_job_v2 expects
    mock_job._backend = Mock()
    mock_job._api_client = Mock()
    mock_job._job_id = "test_job_123"
    mock_job._program_id = "sampler"
    mock_job._service = Mock()
    mock_job._creation_date = "2025-10-11T00:00:00Z"
    mock_job._final_result_decoder = Mock()
    mock_job._image = "qiskit-runtime:latest"
    mock_job._session_id = None
    mock_job._tags = ["test-tag"]
    mock_job._version = 2
    mock_job._private = False
    mock_job._status = "DONE"

    return mock_job
