"""
Serialization functions for Fire Opal embedded Riken client Qiskit objects.
"""

import json
import logging

from qiskit.primitives.containers import PrimitiveResult
from qiskit_ibm_runtime import RuntimeDecoder, RuntimeEncoder
from qiskit_ibm_runtime.base_primitive import EstimatorPub, SamplerPub
from qiskit_ibm_runtime.models import BackendConfiguration, BackendProperties

from fireopalrikencommons.options import (
    FireOpalEstimatorOptions,
    FireOpalSamplerOptions,
)

logger = logging.getLogger(__name__)


def encode_input_pubs(input_pubs: list[SamplerPub] | list[EstimatorPub]) -> str:
    """
    Encode a list of SamplerPub or EstimatorPub objects to a JSON string.

    Parameters
    ----------
    input_pubs : list[SamplerPub] | list[EstimatorPub]
        The SamplerPub or EstimatorPub objects to be encoded.

    Returns
    -------
    str
        A JSON string representing the encoded SamplerPub or EstimatorPub objects.
    """
    return json.dumps(input_pubs, cls=RuntimeEncoder)


def encode_sampler_pubs(sampler_pubs: list[SamplerPub]) -> str:
    """
    Encode a list of SamplerPub objects to a JSON string.

    Parameters
    ----------
    sampler_pubs : list[SamplerPub]
        The SamplerPub objects to be encoded.

    Returns
    -------
    str
        A JSON string representing the encoded SamplerPub objects.
    """
    return json.dumps(sampler_pubs, cls=RuntimeEncoder)


def decode_sampler_pubs(sampler_pubs_json: str) -> list[SamplerPub]:
    """
    Decode a list of SamplerPub objects from JSON string format.

    Parameters
    ----------
    sampler_pubs_json : str
        A JSON string representing the SamplerPub objects.

    Returns
    -------
    list[SamplerPub]
        The decoded SamplerPub objects.
    """
    data = json.loads(sampler_pubs_json, cls=RuntimeDecoder)
    return [SamplerPub.coerce(pub) for pub in data]


def decode_estimator_pubs(estimator_pubs_json: str) -> list[EstimatorPub]:
    """
    Decode a list of EstimatorPub objects from JSON string format.

    Parameters
    ----------
    estimator_pubs_json : str
        A JSON string representing the EstimatorPub objects.

    Returns
    -------
    list[EstimatorPub]
        The decoded EstimatorPub objects.
    """
    data = json.loads(estimator_pubs_json, cls=RuntimeDecoder)
    return [EstimatorPub.coerce(pub) for pub in data]


def encode_sampler_pub_results(sampler_pub_results: PrimitiveResult) -> str:
    """
    Encode a list of SamplerPub objects to a JSON string.

    Parameters
    ----------
    sampler_pub_results : PrimitiveResult
        The SamplerPub objects to be encoded.

    Returns
    -------
    str
        A JSON string representing the encoded SamplerPub objects.
    """
    return json.dumps(sampler_pub_results, cls=RuntimeEncoder)


def decode_sampler_pub_results(sampler_pub_results_json: str) -> PrimitiveResult:
    """
    Decode a list of SamplerPub objects from JSON string format.

    Parameters
    ----------
    sampler_pub_results_json : str
        A JSON string representing the SamplerPub objects.

    Returns
    -------
    PrimitiveResult
        The decoded SamplerPub objects.
    """
    return json.loads(sampler_pub_results_json, cls=RuntimeDecoder)


def encode_backend_properties(backend_properties: BackendProperties) -> str:
    """
    Encode a BackendProperties object to a JSON string.

    Parameters
    ----------
    backend_properties : BackendProperties
        The BackendProperties object to be encoded.

    Returns
    -------
    str
        A JSON string representing the encoded BackendProperties object.
    """
    return json.dumps(backend_properties.to_dict(), cls=RuntimeEncoder)


def decode_backend_properties(backend_properties_json: str) -> BackendProperties:
    """
    Decode a BackendProperties object from JSON string format.

    Parameters
    ----------
    backend_properties_json : str
        A JSON string representing the BackendProperties object.

    Returns
    -------
    BackendProperties
        The decoded BackendProperties object.
    """
    data = json.loads(backend_properties_json, cls=RuntimeDecoder)
    return BackendProperties.from_dict(data)


def encode_backend_configuration(backend_configuration: BackendConfiguration) -> str:
    """
    Encode a BackendConfiguration object to a JSON string.

    Parameters
    ----------
    backend_configuration : BackendConfiguration
        The BackendConfiguration object to be encoded.

    Returns
    -------
    str
        A JSON string representing the encoded BackendConfiguration object.
    """
    return json.dumps(backend_configuration.to_dict(), cls=RuntimeEncoder)


def decode_backend_configuration(
    backend_configuration_json: str,
) -> BackendConfiguration:
    """
    Decode a BackendConfiguration object from JSON string format.

    Parameters
    ----------
    backend_configuration_json : str
        A JSON string representing the BackendConfiguration object.

    Returns
    -------
    BackendConfiguration
        The decoded BackendConfiguration object.
    """
    data = json.loads(backend_configuration_json, cls=RuntimeDecoder)
    return BackendConfiguration.from_dict(data)


def encode_fire_opal_run_options(
    options: FireOpalSamplerOptions | FireOpalEstimatorOptions,
) -> str:
    """
    Encode a FireOpalSamplerOptions object to a JSON string using custom encoder.

    Parameters
    ----------
    options : FireOpalSamplerOptions
        Sampler options to encode.

    Returns
    -------
    str
        A JSON string representing the encoded SamplerOptions object.
    """
    return options.model_dump_json()


def decode_fire_opal_run_options(options_json: str) -> FireOpalSamplerOptions:
    """
    Decode a FireOpalSamplerOptions object from JSON string using custom decoder.

    Parameters
    ----------
    options_json : str
        A JSON string representing the FireOpalSamplerOptions object.

    Returns
    -------
    FireOpalSamplerOptions
        The decoded FireOpalSamplerOptions object.
    """
    return FireOpalSamplerOptions.model_validate_json(options_json)


def decode_fire_opal_estimator_options(options_json: str) -> FireOpalEstimatorOptions:
    """
    Decode a FireOpalEstimatorOptions object from JSON string using custom decoder.

    Parameters
    ----------
    options_json : str
        A JSON string representing the FireOpalEstimatorOptions object.

    Returns
    -------
    FireOpalEstimatorOptions
        The decoded FireOpalEstimatorOptions object.
    """
    return FireOpalEstimatorOptions.model_validate_json(options_json)
