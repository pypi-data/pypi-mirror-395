"""
Unit tests for serializers functions.
"""

from qiskit import QuantumCircuit
from qiskit.primitives.containers.observables_array import ObservablesArray
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime.base_primitive import EstimatorPub, SamplerPub
from qiskit_ibm_runtime.fake_provider import FakeFez

from fireopalrikencommons.options import (
    FireOpalEstimatorOptions,
    FireOpalSamplerOptions,
)
from fireopalrikencommons.serializers import (
    decode_backend_configuration,
    decode_backend_properties,
    decode_estimator_pubs,
    decode_fire_opal_estimator_options,
    decode_fire_opal_run_options,
    decode_sampler_pubs,
    encode_backend_configuration,
    encode_backend_properties,
    encode_fire_opal_run_options,
    encode_input_pubs,
)


def test_sampler_pubs_serialization() -> None:
    """Test round-trip serialization for SamplerPub objects."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    original_pubs = [SamplerPub(circuit, shots=1024)]

    # Round-trip: objects -> JSON -> objects
    json_str = encode_input_pubs(original_pubs)
    decoded_pubs = decode_sampler_pubs(json_str)

    assert len(decoded_pubs) == 1
    assert decoded_pubs[0].shots == 1024
    assert decoded_pubs[0].circuit.num_qubits == 2


def test_estimator_pubs_serialization() -> None:
    """Test round-trip serialization for EstimatorPub objects."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)

    # Create a simple observable
    observable_array = ObservablesArray(
        [SparsePauliOp.from_list([("ZZ", 1.0), ("XX", 0.5)])]
    )

    original_pubs = [EstimatorPub(circuit, observable_array, precision=0.01)]

    # Round-trip: objects -> JSON -> objects
    json_str = encode_input_pubs(original_pubs)
    decoded_pubs = decode_estimator_pubs(json_str)

    assert len(decoded_pubs) == 1
    assert decoded_pubs[0].precision == 0.01
    assert decoded_pubs[0].circuit.num_qubits == 2
    assert decoded_pubs[0].observables.shape == (1,)
    assert decoded_pubs[0].observables[0] == observable_array[0]


def test_backend_properties_serialization() -> None:
    """Test round-trip serialization for BackendProperties objects."""
    fake_backend = FakeFez()
    original_properties = fake_backend.properties()

    # Round-trip: object -> JSON -> object
    json_str = encode_backend_properties(original_properties)
    decoded_properties = decode_backend_properties(json_str)

    assert decoded_properties.backend_name == "ibm_fez"
    assert len(decoded_properties.qubits) == 156


def test_backend_configuration_serialization() -> None:
    """Test round-trip serialization for BackendConfiguration objects."""
    fake_backend = FakeFez()
    original_configuration = fake_backend.configuration()

    # Round-trip: object -> JSON -> object
    json_str = encode_backend_configuration(original_configuration)
    decoded_configuration = decode_backend_configuration(json_str)

    assert decoded_configuration.backend_name == "fake_fez"
    assert decoded_configuration.n_qubits == 156


def test_run_options_serialization() -> None:
    """Test round-trip serialization for SamplerOptions objects."""
    # Create SamplerOptions with some basic settings
    original_options = FireOpalSamplerOptions(
        default_shots=2048,
    )

    # Round-trip: object -> JSON -> object
    json_str = encode_fire_opal_run_options(original_options)
    decoded_options = decode_fire_opal_run_options(json_str)

    assert decoded_options.default_shots == 2048


def test_estimator_options_serialization() -> None:
    """Test round-trip serialization for FireOpalEstimatorOptions objects."""
    # Create EstimatorOptions with some basic settings
    original_options = FireOpalEstimatorOptions(
        default_precision=0.005,
    )

    # Round-trip: object -> JSON -> object
    json_str = encode_fire_opal_run_options(original_options)
    decoded_options = decode_fire_opal_estimator_options(json_str)

    assert decoded_options.default_precision == 0.005
