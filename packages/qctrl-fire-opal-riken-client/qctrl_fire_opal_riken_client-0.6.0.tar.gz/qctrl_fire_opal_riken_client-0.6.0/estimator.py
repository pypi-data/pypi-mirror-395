import logging
from typing import Any

from qiskit.providers import BackendV2
from qiskit_ibm_runtime import EstimatorV2, SamplerV2
from qiskit_ibm_runtime.base_primitive import EstimatorPub
from qiskit_ibm_runtime.batch import Batch
from qiskit_ibm_runtime.models import BackendConfiguration, BackendProperties
from qiskit_ibm_runtime.options import EstimatorOptions
from qiskit_ibm_runtime.runtime_job_v2 import RuntimeJobV2
from qiskit_ibm_runtime.session import Session

from fireopalrikenclient.utils.client import (
    FireOpalClient,
    FireOpalClientInterface,
)
from fireopalrikenclient.utils.job import FireOpalJob
from fireopalrikenclient.utils.requests import (
    create_fire_opal_preprocessing_request,
    generate_task_id,
)
from fireopalrikencommons.options import (
    FireOpalEstimatorOptions,
)
from fireopalrikencommons.protos import compute_service_pb2
from fireopalrikencommons.serializers import (
    decode_sampler_pubs,
)

logger = logging.getLogger(__name__)


class FireOpalEstimator(EstimatorV2):
    """
    Base class of the qiskit EstimatorV2 class that calls the Fire Opal server.

    Parameters
    ----------
    mode : BackendV2 or Session or Batch or None
        The mode to run the estimator. If None, will default to Job mode. Defaults to None.
    options : dict or EstimatorOptions or None
        Options for the Estimator primitive. If None, default options are used. Defaults to None.
    """

    def __init__(
        self,
        mode: BackendV2 | Session | Batch | None = None,
        options: dict[str, Any] | EstimatorOptions | None = None,
    ) -> None:
        """
        Initialize the FireOpalEstimator primitive
        """
        self._input_mode = mode
        super().__init__(mode=mode, options=options)

        self._grpc_client: FireOpalClientInterface = FireOpalClient()
        self._grpc_client.connect()

        if options is None:
            self.fire_opal_run_options = FireOpalEstimatorOptions()
        elif isinstance(options, dict):
            self.fire_opal_run_options = FireOpalEstimatorOptions(**options)
        else:
            self.fire_opal_run_options = (
                FireOpalEstimatorOptions.from_estimator_options(options)
            )

    def _run(self, pubs: list[EstimatorPub]) -> RuntimeJobV2:
        """
        Override the base qiskit EstimatorV2 _run method to call the Fire Opal estimator
        pre-processing and post-processing grpc tasks.

        Parameters
        ----------
        pubs : list[EstimatorPub]
            The list of EstimatorPub objects to run.

        Returns
        -------
        list[EstimatorPubResult]
            The output results
        """
        logger.info("Starting FireOpal estimator run with %d pubs", len(pubs))

        backend_properties: BackendProperties = self.backend().properties()
        backend_configuration: BackendConfiguration = self.backend().configuration()

        # Create a unique task identifier.
        task_id = generate_task_id()

        # Step 1: Call fire opal pre-processing grpc task
        preprocessing_request = create_fire_opal_preprocessing_request(
            task_id,
            pubs,
            backend_properties,
            backend_configuration,
            self.fire_opal_run_options,
            compute_service_pb2.TaskType.TASK_TYPE_ESTIMATOR,
        )
        preprocessing_result = self._grpc_client.preprocess_circuits(
            preprocessing_request
        )

        # Step 2: Call IBM runtime SamplerV2 _run method.
        # Fire Opal uses the Sampler to run the preprocessed Estimator circuits.
        preprocessed_pubs = decode_sampler_pubs(preprocessing_result.pubs)
        logger.info(preprocessed_pubs)

        sampler = SamplerV2(mode=self._input_mode)
        job = sampler._run(preprocessed_pubs)  # noqa: SLF001 # private-member-access

        # Step 3: Wrap the returned job in a FireOpalJob to handle post-processing
        # once the job completes.
        fire_opal_job = FireOpalJob.from_qiskit_job(
            job,
            grpc_client=self._grpc_client,
            task_id=task_id,
            task_type=compute_service_pb2.TaskType.TASK_TYPE_ESTIMATOR,
        )

        logger.info("Circuits sent for execution. Call `result()` to retrieve results.")
        return fire_opal_job
