"""
Fire Opal preprocessing and postprocessing operations for RIKEN native integration.

This module contains the core Fire Opal operations that can be used independently
of the sampler implementation.
"""

import logging
import uuid

from qiskit_ibm_runtime.base_primitive import SamplerPub
from qiskit_ibm_runtime.models import BackendConfiguration, BackendProperties

from fireopalrikencommons.options import FireOpalSamplerOptions
from fireopalrikencommons.protos import compute_service_pb2
from fireopalrikencommons.serializers import (
    encode_backend_configuration,
    encode_backend_properties,
    encode_fire_opal_run_options,
    encode_sampler_pub_results,
    encode_sampler_pubs,
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
    pubs: list[SamplerPub],
    backend_properties: BackendProperties,
    backend_configuration: BackendConfiguration,
    options: FireOpalSamplerOptions,
) -> compute_service_pb2.PreprocessingRequest:
    """
    Creates and validates a Fire Opal preprocessing gRPC request.

    Parameters
    ----------
    task_id : str
        Unique identifier for the preprocessing task.
    pubs : list[SamplerPub]
        The input sampler pub objects for preprocessing.
    backend_properties : BackendProperties
        The properties of the backend to use for preprocessing.
    backend_configuration : BackendConfiguration
        The configuration of the backend to use for preprocessing.
    options : FireOpalSamplerOptions
        The custom Sampler run options for Fire Opal preprocessing.

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
        pubs=encode_sampler_pubs(pubs),
        run_options=encode_fire_opal_run_options(options),
    )

    return pre_processing_request


def create_fire_opal_postprocessing_request(
    task_id: str,
    pub_results: list[SamplerPub],
    pubs_original: list[SamplerPub],
    pubs_submitted: list[SamplerPub],
) -> compute_service_pb2.PostprocessingRequest:
    """
    Creates and validates a Fire Opal postprocessing gRPC request.

    Parameters
    ----------
    task_id : str
        Unique identifier for the preprocessing task.
    pub_results : list[SamplerPub]
        The pub results coming from the device.
    pubs_original : list[SamplerPub]
        The original sampler pubs sent to pre_processing.
    pubs_submitted : list[SamplerPub]
        The submitted sampler pubs for post_processing.

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
        pub_results=encode_sampler_pub_results(pub_results),
        pubs_original=encode_sampler_pubs(pubs_original),
        pubs_submitted=encode_sampler_pubs(pubs_submitted),
    )

    return post_processing_request
