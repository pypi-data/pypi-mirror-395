"""
Fire Opal job functionality.
"""

# ruff: noqa: SLF001

import logging
from collections.abc import Callable
from types import MethodType
from typing import Any

from qiskit.primitives.containers import SamplerPubResult
from qiskit_ibm_runtime.base_primitive import SamplerPub
from qiskit_ibm_runtime.fake_provider.local_runtime_job import LocalRuntimeJob
from qiskit_ibm_runtime.runtime_job_v2 import RuntimeJobV2

from fireopalrikenclient.utils.client import (
    FireOpalClientInterface,
)
from fireopalrikenclient.utils.requests import (
    create_fire_opal_postprocessing_request,
)
from fireopalrikencommons.serializers import (
    decode_sampler_pub_results,
)

logger = logging.getLogger(__name__)


def create_fire_opal_result_method(
    original_result_method: Callable,
    grpc_client: FireOpalClientInterface,
    task_id: str,
    input_pubs: list[SamplerPub],
    preprocessed_pubs: list[SamplerPub],
    backend: RuntimeJobV2 | LocalRuntimeJob,
) -> Callable:
    """
    Create a Fire Opal result method that wraps the original job's result method.

    Parameters
    ----------
    original_result_method : Callable
        The original result method from the job
    grpc_client : FireOpalClientInterface
        The gRPC client used to communicate with the Fire Opal server
    task_id : str
        The unique identifier for the Fire Opal task
    input_pubs : list[SamplerPub]
        The list of input publications for the job
    preprocessed_pubs : list[SamplerPub]
        The list of preprocessed publications for the job
    backend : RuntimeJobV2 or LocalRuntimeJob
        The backend for logging purposes

    Returns
    -------
    callable
        A new result method that includes Fire Opal post-processing
    """
    # Cache for post-processed results
    post_processed_results: list[SamplerPubResult] | None = None

    def fire_opal_result(
        _: RuntimeJobV2 | LocalRuntimeJob,
        *args: Any,
        **kwargs: Any,
    ) -> list[SamplerPubResult]:
        """
        Fire Opal result method that calls post-processing after getting device results.
        """
        nonlocal post_processed_results

        if post_processed_results is not None:
            return post_processed_results

        try:
            # Call the original result method
            device_result_pubs: list[SamplerPubResult] = original_result_method(
                *args, **kwargs
            )
            logger.info(device_result_pubs)
        except Exception:
            logger.exception(
                "Failed to retrieve results for task '%s' on device '%s'.",
                task_id,
                backend.name,
            )
            raise

        logger.info(
            "Results received from device '%s' for job '%s'",
            backend.name,
            task_id,
        )

        # Call fire opal post-processing grpc task.
        postprocessing_request = create_fire_opal_postprocessing_request(
            task_id, device_result_pubs, input_pubs, preprocessed_pubs
        )

        logger.info("Calling Fire Opal post-processing gRPC task")
        postprocessing_result = grpc_client.postprocess_results(postprocessing_request)

        output_result_pubs = decode_sampler_pub_results(postprocessing_result.results)
        logger.info("Fire Opal job '%s' completed successfully", task_id)

        # Cache the post-processed results for subsequent calls to result.
        post_processed_results = output_result_pubs
        return output_result_pubs

    return fire_opal_result


class FireOpalJob:
    """
    Factory class for creating Fire Opal jobs from qiskit jobs.

    This class provides a method to wrap a Qiskit Job object (e.g. RuntimeJobV2,
    LocalRuntimeJob) instance with Fire Opal post-processing capabilities after
    result retrieval by replacing the result method.
    """

    @classmethod
    def from_qiskit_job(
        cls,
        job: RuntimeJobV2 | LocalRuntimeJob,
        task_id: str,
        input_pubs: list[SamplerPub],
        preprocessed_pubs: list[SamplerPub],
        grpc_client: FireOpalClientInterface,
    ) -> RuntimeJobV2 | LocalRuntimeJob:
        """
        Modify a job object with Fire Opal post-processing by replacing its result method.

        This approach works with any job type (RuntimeJobV2, LocalRuntimeJob, etc.)
        without requiring inheritance or class-specific handling.

        Parameters
        ----------
        job : RuntimeJobV2 or LocalRuntimeJob
            The original job to be modified. Can be RuntimeJobV2, LocalRuntimeJob, or any
            job-like object with a result() method.
        task_id : str
            The unique identifier for the Fire Opal task.
        input_pubs : list[SamplerPub]
            The list of input publications for the job.
        preprocessed_pubs : list[SamplerPub]
            The list of preprocessed publications for the job.
        grpc_client : FireOpalClientInterface
            The gRPC client used to communicate with the Fire Opal server.

        Returns
        -------
        RuntimeJobV2 or LocalRuntimeJob
            The same job instance with an modified result method that includes
            Fire Opal post-processing.
        """
        # Create the modified result method
        modified_result = create_fire_opal_result_method(
            job.result,
            grpc_client,
            task_id,
            input_pubs,
            preprocessed_pubs,
            job._backend,
        )

        # Replace the result method on the job instance
        job.result = MethodType(modified_result, job)

        return job
