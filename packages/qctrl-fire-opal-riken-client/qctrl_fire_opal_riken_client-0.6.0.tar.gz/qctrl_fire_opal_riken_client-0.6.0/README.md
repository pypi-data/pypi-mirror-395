# Fire Opal RIKEN Client

This is the Fire Opal client integration for RIKEN quantum computing infrastructure using a gRPC client.

## Architecture Overview

- **Client**: Qiskit `SamplerV2` implementation that sends circuits to Fire Opal server for optimization
- **Server**: gRPC service that performs Fire Opal preprocessing/postprocessing

## Usage

Here is a small example of how to use the Fire Opal RIKEN client with Qiskit. This will communicate with a gRPC server to perform Fire Opal pre-processing on a quantum circuit before executing it on the `ibm_kobe` backend. Once the job is complete, results post-processed by Fire Opal will be returned from the `job.result()` call.

```python
import os
from qiskit import QuantumCircuit
from qiskit.providers import BackendV2
from fireopalrikenclient.sampler import FireOpalSampler
from fireopalrikenclient.utils.client import FireOpalClient

# Create circuit.
circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()

# Create sampler with Fire Opal preprocessing.
service = QiskitRuntimeService(token="...", instance="...", channel="ibm_quantum_platform")
sampler = FireOpalSampler(mode=service.backend("ibm_kobe"))

# Run with Fire Opal optimization.
sampler_pub = (circuit, None, 1024)
job = sampler.run([sampler_pub])
result = job.result()
```
