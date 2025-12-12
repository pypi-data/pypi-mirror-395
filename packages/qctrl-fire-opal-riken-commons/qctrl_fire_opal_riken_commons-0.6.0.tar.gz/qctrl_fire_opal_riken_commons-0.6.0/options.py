"""Custom types to be shared between Fire Opal client and server implementations."""

from pydantic import BaseModel
from qiskit_ibm_runtime.options import EstimatorOptions, SamplerOptions
from qiskit_ibm_runtime.options.utils import Unset


class FireOpalSamplerOptions(BaseModel):
    """
    Custom set of supported `SamplerOptions` for the Fire Opal Sampler.

    Parameters
    ----------
    default_shots : int, optional
        The default number of shots to use if none are specified in the PUBs
        or in the run method. If not provided, will default to 4096.
        Defaults to None.
    """

    default_shots: int | None = None

    @classmethod
    def from_sampler_options(cls, options: SamplerOptions) -> "FireOpalSamplerOptions":
        """
        Create a `FireOpalSamplerOptions` instance from a `SamplerOptions` instance.

        Parameters
        ----------
        options : SamplerOptions
            The `SamplerOptions` instance to convert.

        Returns
        -------
        FireOpalSamplerOptions
            The corresponding `FireOpalSamplerOptions` instance.
        """
        return FireOpalSamplerOptions(
            default_shots=options.default_shots
            if options.default_shots is not Unset
            else None
        )


class FireOpalEstimatorOptions(BaseModel):
    """
    Custom set of supported `EstimatorOptions` for the Fire Opal Estimator.

    Parameters
    ----------
    default_precision : float or None, optional
        The default precision to use if none are specified in the PUBs or in the run method.
        If not provided, will default to 0.015625 (1 / sqrt(4096)).
    """

    default_precision: float | None = None

    @classmethod
    def from_estimator_options(
        cls, options: EstimatorOptions
    ) -> "FireOpalEstimatorOptions":
        """
        Create a `FireOpalEstimatorOptions` instance from a `EstimatorOptions` instance.

        Parameters
        ----------
        options : EstimatorOptions
            The `EstimatorOptions` instance to convert.

        Returns
        -------
        FireOpalEstimatorOptions
            The corresponding `FireOpalEstimatorOptions` instance.
        """
        return FireOpalEstimatorOptions(
            default_precision=options.default_precision
            if options.default_precision is not Unset
            else None
        )
