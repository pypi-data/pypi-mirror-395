"""
Test fixtures for FireOpalSampler tests.
"""

import logging
from unittest.mock import Mock

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.primitives.containers import SamplerPubResult
from qiskit.primitives.containers.bit_array import BitArray
from qiskit.primitives.containers.data_bin import DataBin, make_data_bin
from qiskit.primitives.containers.observables_array import ObservablesArray
from qiskit.primitives.containers.pub_result import PubResult
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime.base_primitive import EstimatorPub, SamplerPub
from qiskit_ibm_runtime.runtime_job_v2 import RuntimeJobV2

from fireopalrikenclient.utils.client import FireOpalClientInterface
from fireopalrikencommons.protos import compute_service_pb2
from fireopalrikencommons.serializers import decode_estimator_pubs, encode_sampler_pubs


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

        encoded_pre_processed_pubs: str = ""

        # For estimator tasks, convert EstimatorPubs to SamplerPubs to get back the expected
        # pubs format from preprocessing.
        if request.task_type == compute_service_pb2.TaskType.TASK_TYPE_ESTIMATOR:
            estimator_pubs = decode_estimator_pubs(request.pubs)
            pre_processed_estimator_pubs: list[SamplerPub] = [
                SamplerPub.coerce(pub.circuit) for pub in estimator_pubs
            ]
            encoded_pre_processed_pubs = encode_sampler_pubs(
                pre_processed_estimator_pubs
            )
        else:
            encoded_pre_processed_pubs = request.pubs

        # Return the same pubs as received (no optimization in mock)
        return compute_service_pb2.PreprocessingResponse(
            task_id=request.task_id,
            success=True,
            pubs=encoded_pre_processed_pubs,
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
def sample_estimator_pubs(sample_circuit: QuantumCircuit) -> list[EstimatorPub]:
    """Fixture providing sample EstimatorPub objects."""
    observable = SparsePauliOp.from_list([("ZZ", 1.0), ("XX", 0.5)])
    observable_array = ObservablesArray([observable])
    return [EstimatorPub(sample_circuit, observable_array, precision=0.01)]


@pytest.fixture
def sample_job_results() -> list[SamplerPubResult]:
    """Fixture providing sample SamplerPubResult objects."""
    return [SamplerPubResult(DataBin(meas=BitArray.from_samples(["00", "11"])))]


@pytest.fixture
def sample_estimator_job_results() -> list[PubResult]:
    """
    Fixture providing sample EstimatorPub result objects (using PubResult with expectation values
    and standard deviations).
    """
    # Create data bin with expectation values and standard deviations
    data_bin_class = make_data_bin(
        (("evs", np.ndarray), ("stds", np.ndarray)),
        shape=(1,),
    )

    return [
        PubResult(
            data_bin_class(evs=np.array([0.5, -0.3]), stds=np.array([0.1, 0.05]))
        ),
    ]


@pytest.fixture
def mock_sampler_runtime_job(
    sample_job_results: list[SamplerPubResult],
) -> RuntimeJobV2:
    """Fixture providing a mock RuntimeJobV2 object with all required attributes."""
    mock_job = Mock(spec=RuntimeJobV2)
    mock_job.wait_for_final_state.return_value = None
    mock_job.result.return_value = sample_job_results
    mock_job.job_id.return_value = "test_job_123"
    mock_job.status.return_value = "DONE"

    # Add all the private attributes that FireOpalJob.from_runtime_job_v2 expects
    mock_job._backend = Mock()
    mock_job._service = Mock()
    return mock_job


@pytest.fixture
def mock_estimator_runtime_job(
    sample_estimator_job_results: list[PubResult],
) -> RuntimeJobV2:
    """Fixture providing a mock RuntimeJobV2 object with all required attributes."""
    mock_job = Mock(spec=RuntimeJobV2)
    mock_job.wait_for_final_state.return_value = None
    mock_job.result.return_value = sample_estimator_job_results
    mock_job.job_id.return_value = "test_job_123"
    mock_job.status.return_value = "DONE"

    # Add all the private attributes that FireOpalJob.from_runtime_job_v2 expects
    mock_job._backend = Mock()
    mock_job._service = Mock()
    return mock_job
