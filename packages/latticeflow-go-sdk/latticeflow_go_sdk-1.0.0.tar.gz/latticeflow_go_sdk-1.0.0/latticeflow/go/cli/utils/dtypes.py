from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Union

from pydantic import Field

from latticeflow.go.models import AIAppKeyInformation
from latticeflow.go.models import BooleanParameterSpec
from latticeflow.go.models import CategoricalParameterSpec
from latticeflow.go.models import DatasetColumnParameterSpec
from latticeflow.go.models import DatasetGenerationRequest
from latticeflow.go.models import DatasetGeneratorDataSourceTemplate
from latticeflow.go.models import DatasetGeneratorSynthesizerTemplate
from latticeflow.go.models import DatasetParameterSpec
from latticeflow.go.models import EvaluatedEntityType
from latticeflow.go.models import EvaluationConfig
from latticeflow.go.models import FloatParameterSpec
from latticeflow.go.models import IntParameterSpec
from latticeflow.go.models import LFBaseModel
from latticeflow.go.models import ListParameterSpec
from latticeflow.go.models import MLTask
from latticeflow.go.models import Modality
from latticeflow.go.models import ModelAdapterCodeSnippet
from latticeflow.go.models import ModelAdapterProvider
from latticeflow.go.models import ModelCustomConnectionConfig
from latticeflow.go.models import ModelParameterSpec
from latticeflow.go.models import ModelProviderConnectionConfig
from latticeflow.go.models import StringParameterSpec
from latticeflow.go.models import TaskScorerTemplate
from latticeflow.go.models import TaskSolverTemplate


class ResolvedData(LFBaseModel):
    path: Path
    data: Any


ParameterSpecType = Union[
    FloatParameterSpec,
    IntParameterSpec,
    BooleanParameterSpec,
    StringParameterSpec,
    ModelParameterSpec,
    DatasetParameterSpec,
    DatasetColumnParameterSpec,
    ListParameterSpec,
    CategoricalParameterSpec,
]
ConfigSpecType = List[ParameterSpecType]

_user_or_provider_key = Field(
    ...,
    max_length=250,
    min_length=1,
    pattern="^((local|together|zenguard|gemini|openai|fireworks|sambanova|anthropic|novita)\\$)?[a-z0-9_-]+$",
    description="""Key: 1-250 chars, allowed: a-z 0-9 _ -. May optionally start with one of the supported prefixes:
``local$``, ``together$``, ``zenguard$``, ``gemini$``, ``openai$``, ``fireworks$``, ``sambanova$``,
``anthropic$``, or ``novita$``.
""",
)
_user_key_field = Field(
    ...,
    max_length=250,
    min_length=1,
    pattern="^[a-z0-9_\\-]+$",
    description="Key: 1-250 chars, allowed: a-z 0-9 _ - $.",
)
_user_or_lf_key = Field(
    ...,
    max_length=250,
    min_length=1,
    pattern="^[a-z0-9_\\-\\$]+$",
    description="Key: 1-250 chars, allowed: a-z 0 9 _ - $.",
)
_optional_user_or_lf_key = Field(
    None,
    max_length=250,
    min_length=1,
    pattern="^[a-z0-9_\\-\\$]+$",
    description="Optional key: 1-250 chars, allowed: a-z 0 9 _ - $.",
)


class UserOrProviderKey(LFBaseModel):
    key: str = _user_or_provider_key


class UserKey(LFBaseModel):
    key: str = _user_key_field


class UserOrLFKey(LFBaseModel):
    key: str = _user_or_lf_key


class _BaseCLIModel(LFBaseModel):
    display_name: str = Field(
        ..., description="Display name of the model.", min_length=1
    )
    description: str | None = Field(None, description="Description of the model.")
    rate_limit: int | None = Field(
        None, description="Rate limit for API calls to the model."
    )
    modality: Modality = Field(Modality.TEXT, description="Modality of the model.")
    task: MLTask = Field(MLTask.CHAT_COMPLETION, description="Task of the model.")
    config: Union[ModelCustomConnectionConfig, ModelProviderConnectionConfig] = Field(
        ...,
        discriminator="connection_type",
        description="Model connection configuration.",
    )


class CLICreateModel(_BaseCLIModel, UserOrProviderKey):
    adapter: Union[CLICreateModelAdapter, UserOrLFKey] = Field(
        ..., description="Model adapter configuration or key of an existing adapter."
    )


class CLIExportModel(_BaseCLIModel, UserOrLFKey):
    adapter: UserOrLFKey = Field(
        ..., description="Key of the model adapter associated with the model."
    )


class _BaseCLIModelAdapter(LFBaseModel):
    display_name: str = Field(
        ..., description="Display name of the model adapter.", min_length=1
    )
    description: str | None = Field(
        None, description="Description of the model adapter."
    )
    long_description: str | None = Field(
        None, description="Long description of the model adapter."
    )
    provider: ModelAdapterProvider = Field(
        ModelAdapterProvider.USER, description="Provider of the model adapter."
    )
    modality: Modality = Field(
        Modality.TEXT, description="Modality supported by the model adapter."
    )
    task: MLTask = Field(
        MLTask.CHAT_COMPLETION, description="Task supported by the model adapter."
    )
    process_input: ModelAdapterCodeSnippet | None = Field(
        None, description="Code snippet for processing input."
    )
    process_output: ModelAdapterCodeSnippet | None = Field(
        None, description="Code snippet for processing output."
    )


class CLICreateModelAdapter(_BaseCLIModelAdapter, UserKey):
    pass


class CLIExportModelAdapter(_BaseCLIModelAdapter, UserOrLFKey):
    pass


class _BaseCLITask(LFBaseModel):
    display_name: str = Field(
        ..., description="Display name of the task.", min_length=1
    )
    description: str = Field(..., description="Description of the task.")
    long_description: str | None = Field(
        None, description="Long description of the task."
    )
    tags: List[str] = Field([], description="Tags associated with the task.")
    modalities: List[Modality] = Field(
        [], description="Modalities supported by the task."
    )
    tasks: List[MLTask] = Field([], description="ML tasks supported by the task.")
    evaluated_entity_type: EvaluatedEntityType = Field(
        EvaluatedEntityType.MODEL, description="Type of entity being evaluated."
    )
    config_spec: ConfigSpecType = Field(
        ..., description="Configuration specification for the task."
    )
    definition: Union[
        CLIDeclarativeTaskDefinitionTemplate, CLIPredefinedTaskDefinition
    ] = Field(..., discriminator="type", description="Definition of the task.")


class CLICreateTask(_BaseCLITask, UserKey):
    pass


class CLIExportTask(_BaseCLITask, UserOrLFKey):
    pass


class CLIPredefinedTaskDefinition(LFBaseModel):
    type: Literal["predefined"] = Field(
        "predefined", description="Type of the task definition."
    )


class CLIDeclarativeTaskDefinitionTemplate(LFBaseModel):
    type: Literal["declarative_task"] = Field(
        "declarative_task", description="Type of the task definition."
    )
    dataset: CLITaskDatasetTemplate = Field(
        ..., description="Dataset template for the task."
    )
    solver: TaskSolverTemplate = Field(..., description="Solver template for the task.")
    scorers: List[TaskScorerTemplate] = Field(
        ..., description="List of scorer templates for the task."
    )


class CLITaskDatasetTemplate(LFBaseModel):
    key: str = Field(..., description="Key of the dataset to be used for the task.")
    fast_subset_size: Union[int, str] = Field(
        200, description="Size of the fast subset."
    )


class _BaseCLIAIApp(UserKey):
    display_name: str = Field(
        ..., description="Display name of the AI application.", min_length=1
    )
    description: str | None = Field(
        None, description="Description of the AI application."
    )
    long_description: str | None = Field(
        None, description="Long description of the AI application."
    )
    key_info: AIAppKeyInformation | None = Field(
        None, description="Key information for the AI application."
    )
    industry_type: str | None = Field(
        None, description="Industry type for the AI application."
    )


class CLICreateAIApp(_BaseCLIAIApp):
    pass


class CLIExportAIApp(_BaseCLIAIApp):
    pass


class _BaseCLIDatasetGenerator(LFBaseModel):
    display_name: str = Field(
        ..., description="Display name of the dataset generator.", min_length=1
    )
    description: str = Field(
        ..., description="Short description of the dataset generator."
    )
    long_description: str | None = Field(
        None, description="Long description of the dataset generator."
    )
    config_spec: ConfigSpecType = Field(
        ..., description="Configuration specification for the dataset generator."
    )
    definition: Union[
        CLIPredefinedDatasetGeneratorDefinition,
        CLIDeclarativeDatasetGeneratorDefinitionTemplate,
    ] = Field(
        ..., discriminator="type", description="Definition of the dataset generator."
    )
    tags: List[str] = Field(
        [], description="Tags associated with the dataset generator."
    )


class CLICreateDatasetGenerator(_BaseCLIDatasetGenerator, UserKey):
    pass


class CLIExportDatasetGenerator(_BaseCLIDatasetGenerator, UserOrLFKey):
    pass


class CLIPredefinedDatasetGeneratorDefinition(LFBaseModel):
    type: Literal["predefined"] = Field(
        "predefined", description="Type of the dataset generator definition."
    )


class CLIDeclarativeDatasetGeneratorDefinitionTemplate(LFBaseModel):
    type: Literal["declarative_dataset_generator"] = Field(
        "declarative_dataset_generator",
        description="Type of the dataset generator definition.",
    )
    data_source: DatasetGeneratorDataSourceTemplate = Field(
        ..., description="Data source configuration for the dataset generator."
    )
    synthesizer: DatasetGeneratorSynthesizerTemplate = Field(
        ..., description="Data synthesizer configuration for the dataset generator."
    )


class CLIDatasetGeneratorSpecification(DatasetGenerationRequest):
    dataset_generator_key: str = Field(
        ..., description="Key of the dataset generator to use."
    )


class _BaseCLIDataset(LFBaseModel):
    display_name: str = Field(
        ..., description="Display name of the dataset.", min_length=1
    )
    description: str | None = Field(None, description="Description of the dataset.")
    file_path: Path | None = Field(None, description="Path to the dataset file.")
    generator_specification: CLIDatasetGeneratorSpecification | None = Field(
        None, description="Specification of the dataset generator used."
    )


class CLICreateDataset(_BaseCLIDataset, UserKey):
    pass


class CLIExportDataset(_BaseCLIDataset, UserOrLFKey):
    pass


class _BaseCLIEvaluation(LFBaseModel):
    display_name: str = Field(
        ..., description="Display name of the evaluation.", min_length=1
    )
    task_specifications: List[CLITaskSpecification] = Field(
        ..., description="List of task specifications for the evaluation."
    )
    config: EvaluationConfig = Field(
        ..., description="Configuration for the evaluation."
    )


class CLICreateEvaluation(_BaseCLIEvaluation, UserKey):
    pass


class CLIExportEvaluation(_BaseCLIEvaluation, UserOrLFKey):
    pass


class CLITaskSpecification(LFBaseModel):
    task_key: str = _user_or_lf_key
    task_config: Dict[str, Any] = Field(
        ..., description="Configuration for the specified task."
    )
    model_key: str | None = _optional_user_or_lf_key
    display_name: str | None = Field(
        None,
        description="Optional display name for the task specification.",
        min_length=1,
    )
