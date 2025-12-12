"""
Fire Opal preprocessing and postprocessing operations for RIKEN native integration.

This module contains the core Fire Opal operations that can be used independently
of the sampler implementation.
"""

import json
import logging
import uuid

from qiskit.primitives.containers.pub_result import PubResult
from qiskit_ibm_runtime import RuntimeEncoder
from qiskit_ibm_runtime.base_primitive import EstimatorPub, SamplerPub
from qiskit_ibm_runtime.models import BackendConfiguration, BackendProperties

from fireopalrikencommons.options import (
    FireOpalEstimatorOptions,
    FireOpalSamplerOptions,
)
from fireopalrikencommons.protos import compute_service_pb2
from fireopalrikencommons.serializers import (
    encode_backend_configuration,
    encode_backend_properties,
    encode_fire_opal_run_options,
    encode_input_pubs,
)

logger = logging.getLogger(__name__)


def generate_task_id() -> str:
    """
    Generate a unique task ID for the Fire Opal request.

    Returns
    -------
    str
        A unique task identifier.
    """
    return str(uuid.uuid4())


def create_fire_opal_preprocessing_request(
    task_id: str,
    pubs: list[SamplerPub] | list[EstimatorPub],
    backend_properties: BackendProperties,
    backend_configuration: BackendConfiguration,
    options: FireOpalSamplerOptions | FireOpalEstimatorOptions,
    task_type: compute_service_pb2.TaskType,
) -> compute_service_pb2.PreprocessingRequest:
    """
    Creates and validates a Fire Opal preprocessing gRPC request.

    Parameters
    ----------
    task_id : str
        Unique identifier for the preprocessing task.
    pubs : list[SamplerPub] | list[EstimatorPub]
        The input sampler or estimator pub objects for preprocessing.
    backend_properties : BackendProperties
        The properties of the backend to use for preprocessing.
    backend_configuration : BackendConfiguration
        The configuration of the backend to use for preprocessing.
    options : FireOpalSamplerOptions or FireOpalEstimatorOptions
        The custom sampler or estimator run options for Fire Opal preprocessing.
    task_type : compute_service_pb2.TaskType
        The type of task this is (SAMPLER_TASK or ESTIMATOR_TASK).

    Returns
    -------
    compute_service_pb2.PreprocessingRequest
        The validated preprocessing request ready for gRPC messaging.

    Raises
    ------
    CompilationError
        If the static constraints could not be compiled.

    ValidationError
        If the message is invalid.
    """
    pre_processing_request = compute_service_pb2.PreprocessingRequest(
        task_id=task_id,
        backend_configuration=encode_backend_configuration(backend_configuration),
        backend_properties=encode_backend_properties(backend_properties),
        pubs=encode_input_pubs(pubs),
        run_options=encode_fire_opal_run_options(options),
        task_type=task_type,
    )

    return pre_processing_request


def create_fire_opal_postprocessing_request(
    task_id: str,
    pub_results: list[PubResult],
    task_type: compute_service_pb2.TaskType,
) -> compute_service_pb2.PostprocessingRequest:
    """
    Creates and validates a Fire Opal postprocessing gRPC request.

    Parameters
    ----------
    task_id : str
        Unique identifier for the preprocessing task.
    pubs_submitted : list[SamplerPub] | list[EstimatorPub]
    pub_results : list[SamplerPub]
        The pub results coming from the device.
    task_type : compute_service_pb2.TaskType
        The type of task this is (SAMPLER_TASK or ESTIMATOR_TASK).

    Returns
    -------
    compute_service_pb2.PostprocessingRequest
        The validated postprocessing request ready for gRPC messaging.

    Raises
    ------
    CompilationError
        If the static constraints could not be compiled.

    ValidationError
        If the message is invalid.
    """
    post_processing_request = compute_service_pb2.PostprocessingRequest(
        task_id=task_id,
        pub_results=json.dumps(pub_results, cls=RuntimeEncoder),
        task_type=task_type,
    )

    return post_processing_request
