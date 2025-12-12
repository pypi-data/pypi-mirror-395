import logging
from typing import Any

from qiskit.providers import BackendV2
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime.base_primitive import SamplerPub
from qiskit_ibm_runtime.batch import Batch
from qiskit_ibm_runtime.models import BackendConfiguration, BackendProperties
from qiskit_ibm_runtime.options import SamplerOptions
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
from fireopalrikencommons.options import FireOpalSamplerOptions
from fireopalrikencommons.serializers import (
    decode_sampler_pubs,
)

logger = logging.getLogger(__name__)


class FireOpalSampler(SamplerV2):
    """
    Base class of the qiskit SamplerV2 class that calls the Fire Opal server.

    Parameters
    ----------
    mode : BackendV2 or Session or Batch or None
        The mode to run the sampler. If None, will default to Job mode. Defaults to None.
    options : dict or SamplerOptions or None
        Options for the Sampler primitive. If None, default options are used. Defaults to None.
    """

    def __init__(
        self,
        mode: BackendV2 | Session | Batch | None = None,
        options: dict[str, Any] | SamplerOptions | None = None,
    ) -> None:
        """
        Initialize the FireOpalSampler primitive.
        """
        super().__init__(mode=mode, options=options)

        self._grpc_client: FireOpalClientInterface = FireOpalClient()
        self._grpc_client.connect()

        if options is None:
            self.fire_opal_run_options = FireOpalSamplerOptions()
        elif isinstance(options, dict):
            self.fire_opal_run_options = FireOpalSamplerOptions(**options)
        else:
            self.fire_opal_run_options = FireOpalSamplerOptions.from_sampler_options(
                options
            )

    def _run(self, pubs: list[SamplerPub]) -> RuntimeJobV2:
        """
        Override the base qiskit SamplerV2 _run method to call the Fire Opal
        pre-processing and post-processing grpc tasks.

        Parameters
        ----------
        pubs : list[SamplerPub]
            The list of EstimatorPub or SamplerPub objects to run.

        Returns
        -------
        list[SamplerPubResult]
            The output results
        """
        logger.info("Starting FireOpal sampling run with %d pubs", len(pubs))

        # =======================================================================
        # NOTE: Replace fake backend data with `ibm_kobe` backend data if needed.
        backend_properties: BackendProperties = self.backend().properties()
        backend_configuration: BackendConfiguration = self.backend().configuration()
        # =======================================================================

        # Create a unique task identifier.
        task_id = generate_task_id()

        # Step 1: Call fire opal pre-processing grpc task
        preprocessing_request = create_fire_opal_preprocessing_request(
            task_id,
            pubs,
            backend_properties,
            backend_configuration,
            self.fire_opal_run_options,
        )
        preprocessing_result = self._grpc_client.preprocess_circuits(
            preprocessing_request
        )

        # Step 2: Call the default IBM runtime SamplerV2 _run method
        preprocessed_pubs = decode_sampler_pubs(preprocessing_result.pubs)
        logger.info(preprocessed_pubs)
        job = super()._run(preprocessed_pubs)

        # Step 3: Wrap the returned job in a FireOpalJob to handle post-processing
        # once the job completes.
        fire_opal_job = FireOpalJob.from_qiskit_job(
            job,
            grpc_client=self._grpc_client,
            task_id=task_id,
            input_pubs=pubs,
            preprocessed_pubs=preprocessed_pubs,
        )

        logger.info("Circuits sent for execution. Call `result()` to retrieve results.")
        return fire_opal_job
