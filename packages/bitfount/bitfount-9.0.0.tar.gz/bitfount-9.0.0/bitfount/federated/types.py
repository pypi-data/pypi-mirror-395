"""Useful types for Federated Learning."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from enum import Enum, auto
import logging
import os
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Protocol,
    TypedDict,
    Union,
    runtime_checkable,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
import desert
from marshmallow import fields, validate
from typing_extensions import NotRequired, TypeAlias

from bitfount import config
from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.schema import BitfountSchema
from bitfount.types import UsedForConfigSchemas, _JSONDict, _S3PresignedURL, _StrAnyDict

if TYPE_CHECKING:
    from bitfount.externals.general.authentication import ExternallyManagedJWT
    from bitfount.hub.api import BitfountHub, BitfountSession, PodPublicMetadata
    from bitfount.hub.types import _AMResourceUsageAndLimitJSON
    from bitfount.runners.config_schemas.common_schemas import DataSplitConfig
    from bitfount.runners.config_schemas.hub_schemas import APIKeys
    from bitfount.runners.config_schemas.pod_schemas import (
        FileSystemFilterConfig,
        PodDataConfig,
        PodDetailsConfig,
    )

_logger = logging.getLogger(__name__)


@dataclass
class DatasourceContainerConfig:
    """Contains a datasource and maybe some data related to it.

    This represents a datasource configuration _pre_-data-loading/configuration and
    so the data config and schema are not required.
    """

    name: str
    datasource: BaseSource
    datasource_details: Optional[PodDetailsConfig] = None
    data_config: Optional[PodDataConfig] = None
    schema: Optional[Union[str, os.PathLike, BitfountSchema]] = None


@dataclass
class DatasourceContainer:
    """Contains a datasource and all the data related to it.

    This represents a datasource configuration _post_-data-loading/configuration and
    so the data config and schema must be present.
    """

    name: str
    datasource: BaseSource
    datasource_details: PodDetailsConfig
    data_config: PodDataConfig
    schema: BitfountSchema


@dataclass
class MinimalDatasourceConfig:
    """Minimal serializable configuration required for creating a datasource."""

    datasource_cls_name: str
    name: str
    datasource_args: _JSONDict
    file_system_filters: Optional[FileSystemFilterConfig]
    data_split: Optional[DataSplitConfig]
    is_reconnection: bool = False


@dataclass
class MinimalSchemaGenerationConfig:
    """Minimal serializable configuration required for creating a schema."""

    datasource_name: str
    description: Optional[str]
    column_descriptions: Optional[
        Union[Mapping[str, Mapping[str, str]], Mapping[str, str]]
    ]
    ignore_cols: Optional[list[str]]
    force_stypes: Optional[
        MutableMapping[
            Literal["categorical", "continuous", "image", "text", "image_prefix"],
            list[str],
        ]
    ]


@dataclass
class MinimalSchemaUploadConfig:
    """Minimal serializable configuration required for uploading a schema."""

    # Metadata required for uploading the schema (including the schema itself)
    public_metadata: PodPublicMetadata
    # Public keys required for having permission to upload the schema
    access_manager_public_key: RSAPublicKey
    pod_public_key: RSAPublicKey


@dataclass
class HubConfig:
    """Configuration for connecting to Bitfount Hub."""

    username: Optional[str]
    secrets: Optional[Union[APIKeys, ExternallyManagedJWT]]
    session: Optional[BitfountSession] = None
    session_info: Optional[dict] = None


class TextGenerationDictionary(TypedDict):
    """Hugging Face dictionary response for text generation."""

    generated_text: str


class HuggingFaceImageClassificationInferenceDictionary(TypedDict):
    """Hugging Face dictionary response for image classification."""

    image_classification: str


TextGenerationDefaultReturnType: TypeAlias = list[list[TextGenerationDictionary]]


class SerializedDataStructure(TypedDict):
    """Serialized representation of a data structure."""

    table: NotRequired[Union[str, dict[str, str]]]
    schema_requirements: NotRequired[_StrAnyDict]
    compatible_datasources: NotRequired[list[str]]


class SerializedModel(TypedDict):
    """Serialized representation of a model."""

    class_name: str
    hub: NotRequired[Optional[BitfountHub]]
    schema: NotRequired[_StrAnyDict]
    datastructure: NotRequired[SerializedDataStructure]


class SerializedAlgorithm(TypedDict):
    """Serialized representation of an algorithm."""

    class_name: str  # value from AlgorithmType enum
    model: NotRequired[SerializedModel]
    datastructure: NotRequired[SerializedDataStructure]


class SerializedAggregator(TypedDict):
    """Serialized representation of an aggregator."""

    class_name: str  # value from AggregatorType enum


class SerializedProtocol(TypedDict):
    """Serialized representation of a protocol."""

    class_name: str  # value from ProtocolType enum
    algorithm: Union[SerializedAlgorithm, list[SerializedAlgorithm]]
    aggregator: NotRequired[SerializedAggregator]
    primary_results_path: NotRequired[str]


class ProtocolType(Enum):
    """Available protocol names from `bitfount.federated.protocol`."""

    FederatedAveraging = "bitfount.FederatedAveraging"
    ResultsOnly = "bitfount.ResultsOnly"
    InferenceAndCSVReport = "bitfount.InferenceAndCSVReport"
    InstrumentedInferenceAndCSVReport = "bitfount.InstrumentedInferenceAndCSVReport"
    InferenceAndReturnCSVReport = "bitfount.InferenceAndReturnCSVReport"
    # Ophthalmology Protocols
    GAScreeningProtocolAmethyst = "bitfount.GAScreeningProtocolAmethyst"
    GAScreeningProtocolJade = "bitfount.GAScreeningProtocolJade"
    GAScreeningProtocolBronze = "bitfount.GAScreeningProtocolBronze"
    GAScreeningProtocolBronzeWithEHR = "bitfount.GAScreeningProtocolBronzeWithEHR"
    GAScreeningProtocolCharcoal = "bitfount.GAScreeningProtocolCharcoal"
    GAScreeningProtocol = (
        "bitfount.GAScreeningProtocol"  # Kept for backwards compatibility
    )
    RetinalDiseaseProtocolCobalt = "bitfount.RetinalDiseaseProtocolCobalt"
    BasicOCTProtocol = "bitfount.BasicOCTProtocol"  # Kept for backwards compatibility
    InferenceAndImageOutput = "bitfount.InferenceAndImageOutput"
    InSiteInsightsProtocol = "bitfount.InSiteInsightsProtocol"
    WetAMDScreeningProtocolSapphire = "bitfount.WetAMDScreeningProtocolSapphire"
    # EHR Protocols
    NextGenSearchProtocol = "bitfount.NextGenSearchProtocol"
    DataExtractionProtocolCharcoal = "bitfount.DataExtractionProtocolCharcoal"
    FluidVolumeScreeningProtocol = "bitfount.FluidVolumeScreeningProtocol"


class AlgorithmType(Enum):
    """Available algorithm names from `bitfount.federated.algorithm`."""

    FederatedModelTraining = "bitfount.FederatedModelTraining"
    ModelTrainingAndEvaluation = "bitfount.ModelTrainingAndEvaluation"
    ModelEvaluation = "bitfount.ModelEvaluation"
    ModelInference = "bitfount.ModelInference"
    SqlQuery = "bitfount.SqlQuery"
    PrivateSqlQuery = "bitfount.PrivateSqlQuery"
    HuggingFacePerplexityEvaluation = "bitfount.HuggingFacePerplexityEvaluation"
    HuggingFaceTextGenerationInference = "bitfount.HuggingFaceTextGenerationInference"
    HuggingFaceImageClassificationInference = (
        "bitfount.HuggingFaceImageClassificationInference"
    )
    HuggingFaceImageSegmentationInference = (
        "bitfount.HuggingFaceImageSegmentationInference"
    )
    HuggingFaceTextClassificationInference = (
        "bitfount.HuggingFaceTextClassificationInference"
    )
    CSVReportAlgorithm = "bitfount.CSVReportAlgorithm"
    TIMMFineTuning = "bitfount.TIMMFineTuning"
    TIMMInference = "bitfount.TIMMInference"
    # Ophthalmology Algorithms
    CSTCalculationAlgorithm = "bitfount.CSTCalculationAlgorithm"
    CSVReportGeneratorOphthalmologyAlgorithm = (
        "bitfount.CSVReportGeneratorOphthalmologyAlgorithm"
    )
    CSVReportGeneratorAlgorithm = (
        "bitfount.CSVReportGeneratorAlgorithm"  # Kept for backwards compatibility
    )
    ETDRSAlgorithm = "bitfount.ETDRSAlgorithm"
    FluidVolumeCalculationAlgorithm = "bitfount.FluidVolumeCalculationAlgorithm"
    FoveaCoordinatesAlgorithm = "bitfount.FoveaCoordinatesAlgorithm"
    GATrialCalculationAlgorithmJade = "bitfount.GATrialCalculationAlgorithmJade"
    GATrialCalculationAlgorithmAmethyst = "bitfount.GATrialCalculationAlgorithmAmethyst"
    GATrialCalculationAlgorithmCharcoal = "bitfount.GATrialCalculationAlgorithmCharcoal"
    GATrialCalculationAlgorithmBronze = "bitfount.GATrialCalculationAlgorithmBronze"
    GATrialCalculationAlgorithm = (
        "bitfount.GATrialCalculationAlgorithm"  # Kept for backwards compatibility
    )
    TrialInclusionCriteriaMatchAlgorithmAmethyst = (
        "bitfount.TrialInclusionCriteriaMatchAlgorithmAmethyst"
    )
    TrialInclusionCriteriaMatchAlgorithmBronze = (
        "bitfount.TrialInclusionCriteriaMatchAlgorithmBronze"
    )
    TrialInclusionCriteriaMatchAlgorithmJade = (
        "bitfount.TrialInclusionCriteriaMatchAlgorithmJade"
    )
    TrialInclusionCriteriaMatchAlgorithmCharcoal = (
        "bitfount.TrialInclusionCriteriaMatchAlgorithmCharcoal"
    )
    TrialInclusionCriteriaMatchAlgorithmSapphire = (
        "bitfount.TrialInclusionCriteriaMatchAlgorithmSapphire"
    )
    TrialInclusionCriteriaMatchAlgorithm = "bitfount.TrialInclusionCriteriaMatchAlgorithm"  # Kept for backwards compatibility # noqa: E501
    GATrialPDFGeneratorAlgorithmAmethyst = (
        "bitfount.GATrialPDFGeneratorAlgorithmAmethyst"
    )
    GATrialPDFGeneratorAlgorithmJade = "bitfount.GATrialPDFGeneratorAlgorithmJade"
    GATrialPDFGeneratorAlgorithm = (
        "bitfount.GATrialPDFGeneratorAlgorithm"  # Kept for backwards compatibility
    )
    _SimpleCSVAlgorithm = "bitfount._SimpleCSVAlgorithm"
    ReduceCSVAlgorithmCharcoal = "bitfount.ReduceCSVAlgorithmCharcoal"
    RecordFilterAlgorithm = "bitfount.RecordFilterAlgorithm"
    BscanImageAndMaskGenerationAlgorithm = (
        "bitfount.BscanImageAndMaskGenerationAlgorithm"
    )
    S3UploadAlgorithm = "bitfount.S3UploadAlgorithm"
    # EHR Algorithms
    EHRPatientQueryAlgorithm = "bitfount.EHRPatientQueryAlgorithm"
    EHRPatientInfoDownloadAlgorithm = "bitfount.EHRPatientInfoDownloadAlgorithm"
    ImageSelectionAlgorithm = "bitfount.ImageSelectionAlgorithm"
    LongitudinalAlgorithm = "bitfount.LongitudinalAlgorithm"
    PatientIDExchangeAlgorithm = "bitfount.PatientIDExchangeAlgorithm"


class AggregatorType(Enum):
    """Available aggregator names from `bitfount.federated.aggregator`."""

    Aggregator = "bitfount.Aggregator"
    SecureAggregator = "bitfount.SecureAggregator"


class _PodResponseType(Enum):
    """Pod response types sent to `Modeller` on a training job request.

    Responses correspond to those from /api/access.
    """

    ACCEPT = auto()
    NO_ACCESS = auto()
    INVALID_PROOF_OF_IDENTITY = auto()
    UNAUTHORISED = auto()
    NO_PROOF_OF_IDENTITY = auto()
    NO_DATA = auto()
    INCOMPATIBLE_DATASOURCE = auto()
    TASK_SETUP_ERROR = auto()
    TASK_TIMEOUT = auto()


class AccessCheckResult(TypedDict):
    """Container for the result of the access manager check."""

    response_type: _PodResponseType
    limits: Optional[list[_AMResourceUsageAndLimitJSON]]


class _DataLessAlgorithm:
    """Base algorithm class for tagging purposes.

    Used in algorithms for which data loading is done at runtime.
    """

    ...


EHRProvider = Literal[
    "nextgen enterprise", "nextech intellechartpro r4", "smarthealthit r4", "epic r4"
]


@dataclass
class EHRConfig(UsedForConfigSchemas):
    """Configuration for EHR details."""

    base_url: str
    provider: EHRProvider = desert.field(
        fields.String(
            allow_none=False,
            validate=validate.OneOf(
                (
                    "nextgen enterprise",
                    "nextech intellechartpro r4",
                    "smarthealthit r4",
                    "epic r4",
                )
            ),
        )
    )
    enterprise_url: Optional[str] = None  # only used for nextgen
    smart_on_fhir_url: Optional[str] = None  # only used for nextgen
    smart_on_fhir_resource_server_url: Optional[str] = None  # only used for nextgen


_RESPONSE_MESSAGES = {
    # /api/access response messages
    _PodResponseType.ACCEPT: "Job accepted",
    _PodResponseType.NO_ACCESS: "There are no permissions for this modeller/pod combination.",  # noqa: E501
    _PodResponseType.INVALID_PROOF_OF_IDENTITY: "Unable to verify identity; ensure correct login used.",  # noqa: E501
    _PodResponseType.UNAUTHORISED: "Insufficient permissions for the requested task on this pod.",  # noqa: E501
    _PodResponseType.NO_PROOF_OF_IDENTITY: "Unable to verify identity, please try again.",  # noqa: E501
    _PodResponseType.NO_DATA: "No data available for the requested task.",
    _PodResponseType.INCOMPATIBLE_DATASOURCE: "Incompatible datasource for the requested task.",  # noqa: E501
    _PodResponseType.TASK_SETUP_ERROR: "Task setup failed due to an unexpected error.",
    _PodResponseType.TASK_TIMEOUT: "Task request timed out.",
}


@runtime_checkable
class _TaskRequestMessageGenerator(Protocol):
    """Callback protocol describing a task request message generator."""

    def __call__(
        self,
        serialized_protocol: SerializedProtocol,
        pod_identifiers: list[str],
        aes_key: bytes,
        pod_public_key: RSAPublicKey,
        project_id: Optional[str],
        run_on_new_data_only: bool = False,
        batched_execution: Optional[bool] = None,
        test_run: bool = False,
        force_rerun_failed_files: bool = True,
    ) -> bytes:
        """Function signature for the callback."""
        ...


#################################
# Protocol/Task Context Classes #
#################################
@dataclass(kw_only=True)
class InferenceLimits:
    """Container class for model inference usage limits.

    Attributes:
        limit: The total number of inferences that can be performed.
        total_usage: The total number of inferences performed so far.
    """

    limit: int
    total_usage: int
    _initial_total_usage: int = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self._initial_total_usage = self.total_usage

    @property
    def initial_total_usage(self) -> int:
        """Returns the total usage that was set when this instance was created."""
        return self._initial_total_usage

    @classmethod
    def from_access_check_result(
        cls, access_check_result: AccessCheckResult
    ) -> dict[str, InferenceLimits]:
        """Construct model name -> inference usage limits from access check results.

        If a model usage `limit` is `undefined` or not present, this indicates that
        there is no usage limit, and so we do not add this to the constructed dict.

        Returns:
            Dictionary of full model name (e.g. "some-model-owner/some-model:12"
            to the model inference usage limits for that model as detailed in
            `access_check_results`).
        """
        limits: Optional[list[_AMResourceUsageAndLimitJSON]] = access_check_result[
            "limits"
        ]
        if not limits:
            return {}
        else:
            limits_dict: dict[str, InferenceLimits] = {}
            for d in limits:
                if d["resourceType"] == "MODEL_INFERENCE":
                    # If a model usage `limit` is `undefined` or not present,
                    # this indicates that there is no usage limit, and so we do not
                    # add this to the constructed dict.
                    limit: Optional[int] = d.get("limit", None)
                    if limit is not None:
                        limits_dict[d["resourceName"]] = InferenceLimits(
                            limit=limit, total_usage=d["totalUsage"]
                        )
            return limits_dict


@dataclass(kw_only=True)
class ModelURLs:
    """Container class for model download URLs from the authorisation checker.

    Attributes:
        model_download_url: URL for downloading the model code.
        model_weights_url: URL for downloading the model weights.
    """

    model_download_url: _S3PresignedURL
    model_weights_url: _S3PresignedURL | None
    # TODO: [BIT-4857] Add model hash information here

    @classmethod
    def from_access_check_result(
        cls, access_check_result: AccessCheckResult
    ) -> dict[str, ModelURLs]:
        """Construct model name -> model download URLs from access check results.

        Returns:
            Dictionary of full model name/id (e.g. "some-model-owner/some-model:12"
            to the model download URL and/or model weights URL for that model as
            detailed in `access_check_results`).
        """
        limits: Optional[list[_AMResourceUsageAndLimitJSON]] = access_check_result[
            "limits"
        ]
        if not limits:
            return {}
        else:
            model_urls_dict: dict[str, ModelURLs] = {}
            for d in limits:
                if d["resourceType"] == "MODEL_INFERENCE":
                    # Only add the model URLs information to the dict if it has
                    # a download URL (it may optionally also have a weights URL)
                    model_download_url: Optional[_S3PresignedURL] = (
                        _S3PresignedURL(url)
                        if (url := d.get("modelDownloadUrl", None)) is not None
                        else None
                    )
                    if model_download_url:
                        model_weights_url: Optional[_S3PresignedURL] = (
                            _S3PresignedURL(url)
                            if (url := d.get("weightsDownloadUrl", None)) is not None
                            else None
                        )
                        model_urls_dict[d["resourceName"]] = ModelURLs(
                            model_download_url=model_download_url,
                            model_weights_url=model_weights_url,
                        )
            return model_urls_dict


class TaskContext(Enum):
    """Describes the context (modeller or worker) in which the task is running.

    This is used for models where the model differs depending on if it is on the
    modeller-side or worker-side of the federated process. It is also used for
    batched execution.
    """

    MODELLER = auto()
    WORKER = auto()


@dataclass(kw_only=True)
class ProtocolContext:
    """Details needed for the protocol at runtime.

    Attributes:
        inference_limits: A mapping of model name (full name, including owner and
            version) to the inference limits information for that model.
            e.g. `{"some-model-owner/some-model:12": {"limit": 90, "total_usage": 10}}`
        model_urls: A mapping of model name (full name, including owner and version)
            to any URLs needed to download the model/weights in the context of the
            task.
        task_context: Which context (modeller or worker) the task is running in.
        project_id: Optional. The ID of the project this task is part of.
        task_id: The ID of the task this context is for.
    """

    task_id: str
    task_context: TaskContext
    inference_limits: dict[str, InferenceLimits] = dataclasses.field(
        default_factory=dict
    )
    model_urls: dict[str, ModelURLs] = dataclasses.field(default_factory=dict)
    project_id: Optional[str] = None

    def get_task_results_dir(self) -> Path:
        """Get the directory where task results should be stored for this task run.

        If TASK_RESULTS_DIR is set, that is used as the base. Otherwise, the base
        will be OUTPUT_DIR/"task-results".

        Within that directory, create a subdirectories named after the project ID,
        and task ID, if provided.
        """
        task_results_dir = config.settings.paths.task_results_dir
        task_results_dir.mkdir(parents=True, exist_ok=True)

        specific_task_results_dir = task_results_dir
        if self.project_id is not None:
            specific_task_results_dir = (
                specific_task_results_dir / self.project_id / self.task_id
            )
            specific_task_results_dir.mkdir(parents=True, exist_ok=True)

        _logger.info(f"Using task results directory: {specific_task_results_dir}")
        return specific_task_results_dir


def get_task_results_directory(context: ProtocolContext) -> Path:
    """Return the path to the task results directory based on the provided context."""
    return context.get_task_results_dir()
