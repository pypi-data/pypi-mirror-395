"""
gRPC client interface and implementation for Fire Opal preprocessing and postprocessing services.

This module provides a minimal client interface and concrete implementation for communicating with the
Fire Opal gRPC server.
"""

import logging
import os
from abc import ABC, abstractmethod
from types import TracebackType

import grpc

from fireopalrikencommons.protos import compute_service_pb2
from fireopalrikencommons.protos.compute_service_pb2_grpc import ComputeServiceStub

logger = logging.getLogger(__name__)


class FireOpalClientInterface(ABC):
    """
    Abstract interface for Fire Opal gRPC client implementations.

    This interface defines the contract for communicating with Fire Opal
    preprocessing and postprocessing services.
    """

    @abstractmethod
    def preprocess_circuits(
        self, request: compute_service_pb2.PreprocessingRequest
    ) -> compute_service_pb2.PreprocessingResponse:
        """
        Call the Fire Opal preprocessing service.

        Parameters
        ----------
        request : compute_service_pb2.PreprocessingRequest
            The gRPC preprocessing request.

        Returns
        -------
        compute_service_pb2.PreprocessingResponse
            Preprocessing response containing optimized circuits.

        Raises
        ------
        grpc.RpcError
            If the gRPC call fails.
        """

    @abstractmethod
    def postprocess_results(
        self, request: compute_service_pb2.PostprocessingRequest
    ) -> compute_service_pb2.PostprocessingResponse:
        """
        Call the Fire Opal postprocessing service.

        Parameters
        ----------
        request : compute_service_pb2.PostprocessingRequest
            The gRPC postprocessing request.

        Returns
        -------
        compute_service_pb2.PostprocessingResponse
            Postprocessing response containing error-mitigated results.

        Raises
        ------
        grpc.RpcError
            If the gRPC call fails.
        """

    @abstractmethod
    def close(self) -> None:
        """
        Close the gRPC client connection.
        """


class FireOpalClient(FireOpalClientInterface):
    """
    Concrete gRPC client implementation for Fire Opal pre/post-processing. This client will
    connect a server address and port specified by the `FIRE_OPAL_GRPC_SERVER_ADDRESS` environment
    variable. If the environment variable is not set, it defaults to `riken.api.q-ctrl.com:50051`.
    """

    def __init__(self) -> None:
        self.server_address = os.environ.get(
            "FIRE_OPAL_GRPC_SERVER_ADDRESS", "riken.api.q-ctrl.com:50051"
        )
        self.channel: grpc.Channel | None = None
        self.stub: ComputeServiceStub | None = None

    def __enter__(self) -> "FireOpalClient":
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Context manager exit."""
        self.close()

    def connect(self) -> None:
        """Connect to the gRPC server."""
        self.channel = grpc.insecure_channel(
            self.server_address,
            options=[
                ("grpc.max_receive_message_length", 500 * 1024 * 1024),  # 500 MB
                ("grpc.max_send_message_length", 500 * 1024 * 1024),  # 500 MB
            ],
        )
        self.stub = ComputeServiceStub(self.channel)
        logger.info("Connected to Fire Opal server at %s", self.server_address)

    def close(self) -> None:
        """Close the gRPC client connection."""
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None
            logger.info("Disconnected from Fire Opal server")

    def preprocess_circuits(
        self, request: compute_service_pb2.PreprocessingRequest
    ) -> compute_service_pb2.PreprocessingResponse:
        """
        Call the Fire Opal preprocessing service.

        Parameters
        ----------
        request : compute_service_pb2.PreprocessingRequest
            The gRPC preprocessing request.

        Returns
        -------
        compute_service_pb2.PreprocessingResponse
            Preprocessing response containing optimized circuits.

        Raises
        ------
        grpc.RpcError
            If the gRPC call fails.
        """
        if not self.stub:
            raise RuntimeError("Client not connected. Call connect() first.")

        try:
            logger.info("Sending preprocessing request for task %s", request.task_id)
            response = self.stub.PreprocessCircuits(request)
            return response

        except grpc.RpcError as e:
            logger.error("gRPC error in preprocessing: %s", e)
            # Create error response
            error_response = compute_service_pb2.PreprocessingResponse()
            error_response.task_id = request.task_id
            error_response.success = False
            error_response.pubs = "[]"
            error_response.error_message = f"gRPC error: {e!s}"
            return error_response
        except Exception as e:  # noqa: BLE001
            logger.error("Error in preprocessing: %s", e)
            # Create error response
            error_response = compute_service_pb2.PreprocessingResponse()
            error_response.task_id = request.task_id
            error_response.success = False
            error_response.pubs = "[]"
            error_response.error_message = f"Error: {e!s}"
            return error_response

    def postprocess_results(
        self, request: compute_service_pb2.PostprocessingRequest
    ) -> compute_service_pb2.PostprocessingResponse:
        """
        Call the Fire Opal postprocessing service.

        Parameters
        ----------
        request : compute_service_pb2.PostprocessingRequest
            The gRPC postprocessing request.

        Returns
        -------
        compute_service_pb2.PostprocessingResponse
            Postprocessing response containing error-mitigated results.

        Raises
        ------
        grpc.RpcError
            If the gRPC call fails.
        """
        if not self.stub:
            raise RuntimeError("Client not connected. Call connect() first.")

        try:
            logger.info("Sending postprocessing request for task %s", request.task_id)
            response = self.stub.PostprocessResults(request)
            return response

        except grpc.RpcError as e:
            logger.error("gRPC error in postprocessing: %s", e)
            # Create error response
            error_response = compute_service_pb2.PostprocessingResponse()
            error_response.task_id = request.task_id
            error_response.success = False
            error_response.results = "[]"
            error_response.error_message = f"gRPC error: {e!s}"
            return error_response
        except Exception as e:  # noqa: BLE001
            logger.error("Error in postprocessing: %s", e)
            # Create error response
            error_response = compute_service_pb2.PostprocessingResponse()
            error_response.task_id = request.task_id
            error_response.success = False
            error_response.results = "[]"
            error_response.error_message = f"Error: {e!s}"
            return error_response
