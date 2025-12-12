# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""TAO API v2 Request Schemas"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, fields
from typing import Any, Type


def to_dict_without_none(cls: Type[Any]) -> Type[Any]:
    """A class decorator to add a to_dict method that omits None values."""

    def to_dict(self) -> dict[str, Any]:
        """Converts the dataclass instance to a dictionary, omitting None values."""
        # Use a dictionary comprehension to filter out None values
        return {field.name: getattr(self, field.name)
                for field in fields(self)
                if getattr(self, field.name) is not None}

    # Attach the new method to the class
    setattr(cls, 'to_dict', to_dict)
    return cls


@to_dict_without_none
@dataclass
class AWSCloudPull:
    """Request schema for AWS cloud pull configuration (v2 API)."""

    # Required fields
    access_key: str
    secret_key: str

    # Optional fields
    cloud_region: Optional[str] = None
    endpoint_url: Optional[str] = None
    cloud_bucket_name: Optional[str] = None
    cloud_type: str = "aws"  # Default value as per V2_API_SPECS_NEW2.json

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class AzureCloudPull:
    """Request schema for Azure cloud pull configuration (v2 API)."""

    # Required fields
    access_key: str
    account_name: str

    # Optional fields
    cloud_region: Optional[str] = None
    endpoint_url: Optional[str] = None
    cloud_bucket_name: Optional[str] = None
    cloud_type: str = "azure"  # Default value as per V2_API_SPECS_NEW2.json

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class HuggingFaceCloudPull:
    """Request schema for HuggingFace cloud pull configuration (v2 API)."""

    # Optional fields
    token: Optional[str] = None
    cloud_type: str = "huggingface"  # Default value as per V2_API_SPECS_NEW2.json

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class SeaweedFSCloudPull:
    """Request schema for SeaweedFS cloud pull configuration (v2 API)."""

    # Required fields
    access_key: str
    secret_key: str

    # Optional fields
    cloud_region: Optional[str] = None
    endpoint_url: Optional[str] = None
    cloud_bucket_name: Optional[str] = None
    cloud_type: str = "seaweedfs"  # Default value as per V2_API_SPECS_NEW2.json

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class SlurmCloudPull:
    """Request schema for SLURM cloud pull configuration (v2 API).

    SLURM workspaces are used for running jobs on SLURM clusters with Lustre storage.

    Example:
        slurm_config = SlurmCloudPull(
            slurm_user="username",
            slurm_hostname="login.cluster.com",
            base_results_dir="/lustre/fsw/portfolios/project/users/username"
        )
        workspace = client.create_workspace(
            name="My SLURM Workspace",
            cloud_type="slurm",
            cloud_specific_details=slurm_config
        )
    """

    # Required fields
    slurm_user: str
    slurm_hostname: str

    # Optional fields
    base_results_dir: Optional[str] = None  # Base directory for results (e.g., /lustre/.../users/username)
    cloud_type: str = "slurm"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


# Union Types (Discriminated Unions from V2_API_SPECS_NEW2.json)
# Define these here before they're used in other schemas

# CloudSpecificDetails is a discriminated union of cloud configurations
CloudSpecificDetails = Union[AWSCloudPull, AzureCloudPull, HuggingFaceCloudPull, SeaweedFSCloudPull, SlurmCloudPull]


@to_dict_without_none
@dataclass
class WorkspaceReq:
    """Request schema for creating a workspace (v2 API)."""

    # Required fields
    name: str
    cloud_type: str  # "aws", "azure", "seaweedfs", "huggingface", "self_hosted"
    cloud_specific_details: Union[Dict[str, Any], CloudSpecificDetails]  # Can be dict or structured cloud config

    # Optional fields
    shared: Optional[bool] = None
    version: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                # Handle cloud_specific_details properly
                if key == "cloud_specific_details" and hasattr(value, 'to_dict'):
                    result[key] = value.to_dict()
                else:
                    result[key] = value
        return result


@to_dict_without_none
@dataclass
class DatasetReq:
    """Request schema for creating a dataset (v2 API)."""

    # Required fields
    type: str  # Dataset type from enum (e.g., "image_classification", "object_detection", etc.)
    format: str  # Dataset format from enum (e.g., "coco", "classification_pyt", etc.)

    # Optional fields
    name: Optional[str] = None
    shared: Optional[bool] = None
    user_id: Optional[str] = None
    description: Optional[str] = None
    docker_env_vars: Optional[Dict[str, str]] = None
    version: Optional[str] = None
    logo: Optional[str] = None
    workspace: Optional[str] = None
    cloud_file_path: Optional[str] = None
    url: Optional[str] = None
    use_for: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class ExperimentJobReq:
    """Request schema for creating an experiment job (v2 API)."""

    # Required fields
    kind: str  # Always "experiment"
    name: str
    network_arch: str
    encryption_key: str
    workspace: str
    action: str
    specs: Dict[str, Any]

    # Optional experiment fields
    description: Optional[str] = None
    docker_env_vars: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    base_experiment_ids: Optional[List[str]] = None
    automl_settings: Optional[Dict[str, Any]] = None

    # Dataset fields
    train_datasets: Optional[List[str]] = None
    eval_dataset: Optional[str] = None
    inference_dataset: Optional[str] = None
    calibration_dataset: Optional[str] = None

    # Optional job fields
    parent_job_id: Optional[str] = None
    platform_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class DatasetJobReq:
    """Request schema for creating a dataset job (v2 API)."""

    # Required fields
    kind: str  # Always "dataset"
    dataset_id: str
    action: str
    specs: Dict[str, Any]

    # Optional dataset fields
    tags: Optional[List[str]] = None

    # Optional job fields
    parent_job_id: Optional[str] = None
    platform_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


def create_experiment_job_request(
    name: str,
    network_arch: str,
    encryption_key: str,
    workspace: str,
    action: str,
    specs: Dict[str, Any],
    docker_env_vars: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    base_experiment_ids: Optional[List[str]] = None,
    automl_settings: Optional[Dict[str, Any]] = None,
    parent_job_id: Optional[str] = None,
    platform_id: Optional[str] = None,
    train_datasets: Optional[List[str]] = None,
    eval_dataset: Optional[str] = None,
    inference_dataset: Optional[str] = None,
    calibration_dataset: Optional[str] = None,
) -> ExperimentJobReq:
    """Create a structured ExperimentJobReq object."""
    return ExperimentJobReq(
        kind="experiment",
        name=name,
        network_arch=network_arch,
        encryption_key=encryption_key,
        workspace=workspace,
        docker_env_vars=docker_env_vars,
        action=action,
        specs=specs,
        description=description,
        tags=tags,
        base_experiment_ids=base_experiment_ids,
        automl_settings=automl_settings,
        parent_job_id=parent_job_id,
        platform_id=platform_id,
        train_datasets=train_datasets,
        eval_dataset=eval_dataset,
        inference_dataset=inference_dataset,
        calibration_dataset=calibration_dataset,
    )


def create_dataset_job_request(
    dataset_id: str,
    action: str,
    specs: Dict[str, Any],
    tags: Optional[List[str]] = None,
    parent_job_id: Optional[str] = None,
    platform_id: Optional[str] = None,
) -> DatasetJobReq:
    """Create a structured DatasetJobReq object."""
    return DatasetJobReq(
        kind="dataset",
        dataset_id=dataset_id,
        action=action,
        specs=specs,
        tags=tags,
        parent_job_id=parent_job_id,
        platform_id=platform_id,
    )


@to_dict_without_none
@dataclass
class InferenceMicroserviceReq:
    """Request schema for creating an inference microservice (v2 API)."""

    # Required fields
    docker_image: str
    gpu_type: str
    num_gpus: int

    # Optional fields
    parent_job_id: Optional[str] = None
    kind: Optional[str] = None  # "experiment" or "dataset"
    model_path: Optional[str] = None
    workspace: Optional[str] = None
    docker_env_vars: Optional[Dict[str, str]] = None
    checkpoint_choose_method: Optional[str] = None  # "latest_model", "best_model", "from_epoch_number"
    checkpoint_epoch_number: Optional[Dict[str, int]] = None
    network_arch: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class InferenceReq:
    """Request schema for making inference requests (v2 API)."""

    # All fields are optional - at least one should be provided
    input: Optional[List[str]] = None  # Base64-encoded images/videos with data URI format
    media: Optional[str] = None  # Cloud path to media file (e.g., aws://bucket/path/to/video.mp4)
    model: Optional[str] = None  # Model identifier (e.g. nvidia/nvdino-v2)
    prompt: Optional[str] = None  # Text prompt for VLM inference
    enable_lora: Optional[bool] = None  # Enable LoRA for inference

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


def create_inference_microservice_request(
    docker_image: str,
    gpu_type: str,
    num_gpus: int,
    parent_job_id: Optional[str] = None,
    kind: Optional[str] = None,
    model_path: Optional[str] = None,
    workspace: Optional[str] = None,
    docker_env_vars: Optional[Dict[str, str]] = None,
    checkpoint_choose_method: Optional[str] = None,
    checkpoint_epoch_number: Optional[Dict[str, int]] = None,
    network_arch: Optional[str] = None,
) -> InferenceMicroserviceReq:
    """Create a structured InferenceMicroserviceReq object."""
    return InferenceMicroserviceReq(
        docker_image=docker_image,
        gpu_type=gpu_type,
        num_gpus=num_gpus,
        parent_job_id=parent_job_id,
        kind=kind,
        model_path=model_path,
        workspace=workspace,
        docker_env_vars=docker_env_vars,
        checkpoint_choose_method=checkpoint_choose_method,
        checkpoint_epoch_number=checkpoint_epoch_number,
        network_arch=network_arch,
    )


def create_inference_request(
    input: Optional[List[str]] = None,
    media: Optional[str] = None,
    model: Optional[str] = None,
    prompt: Optional[str] = None,
    enable_lora: Optional[bool] = None,
) -> InferenceReq:
    """Create a structured InferenceReq object."""
    return InferenceReq(
        input=input,
        media=media,
        model=model,
        prompt=prompt,
        enable_lora=enable_lora,
    )


# Additional Union Types

# JobReq is a discriminated union of DatasetJobReq and ExperimentJobReq
JobReq = Union[DatasetJobReq, ExperimentJobReq]

# JobRsp is a discriminated union of DatasetJobRsp and ExperimentJobRsp (response schemas)
# Note: We don't implement response schemas as dataclasses since they're only for parsing API responses
# JobRsp = Union[DatasetJobRsp, ExperimentJobRsp]


def create_workspace_request(
    name: str,
    cloud_type: str,
    cloud_specific_details: Union[Dict[str, Any], CloudSpecificDetails],
    shared: Optional[bool] = None,
    version: Optional[str] = None,
) -> WorkspaceReq:
    """Create a structured WorkspaceReq object."""
    return WorkspaceReq(
        name=name,
        cloud_type=cloud_type,
        cloud_specific_details=cloud_specific_details,
        shared=shared,
        version=version,
    )


def create_dataset_request(
    dataset_type: str,
    dataset_format: str,
    name: Optional[str] = None,
    shared: Optional[bool] = None,
    user_id: Optional[str] = None,
    description: Optional[str] = None,
    docker_env_vars: Optional[Dict[str, str]] = None,
    version: Optional[str] = None,
    logo: Optional[str] = None,
    workspace: Optional[str] = None,
    cloud_file_path: Optional[str] = None,
    url: Optional[str] = None,
    use_for: Optional[List[str]] = None,
) -> DatasetReq:
    """Create a structured DatasetReq object."""
    return DatasetReq(
        type=dataset_type,
        format=dataset_format,
        name=name,
        shared=shared,
        user_id=user_id,
        description=description,
        docker_env_vars=docker_env_vars,
        version=version,
        logo=logo,
        workspace=workspace,
        cloud_file_path=cloud_file_path,
        url=url,
        use_for=use_for,
    )


def create_aws_cloud_pull_request(
    access_key: str,
    secret_key: str,
    cloud_region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    cloud_bucket_name: Optional[str] = None,
) -> AWSCloudPull:
    """Create a structured AWSCloudPull object."""
    return AWSCloudPull(
        access_key=access_key,
        secret_key=secret_key,
        cloud_region=cloud_region,
        endpoint_url=endpoint_url,
        cloud_bucket_name=cloud_bucket_name,
    )


def create_azure_cloud_pull_request(
    access_key: str,
    account_name: str,
    cloud_region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    cloud_bucket_name: Optional[str] = None,
) -> AzureCloudPull:
    """Create a structured AzureCloudPull object."""
    return AzureCloudPull(
        access_key=access_key,
        account_name=account_name,
        cloud_region=cloud_region,
        endpoint_url=endpoint_url,
        cloud_bucket_name=cloud_bucket_name,
    )


def create_huggingface_cloud_pull_request(
    token: Optional[str] = None,
) -> HuggingFaceCloudPull:
    """Create a structured HuggingFaceCloudPull object."""
    return HuggingFaceCloudPull(
        token=token,
    )


def create_seaweedfs_cloud_pull_request(
    access_key: str,
    secret_key: str,
    cloud_region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    cloud_bucket_name: Optional[str] = None,
) -> SeaweedFSCloudPull:
    """Create a structured SeaweedFSCloudPull object."""
    return SeaweedFSCloudPull(
        access_key=access_key,
        secret_key=secret_key,
        cloud_region=cloud_region,
        endpoint_url=endpoint_url,
        cloud_bucket_name=cloud_bucket_name,
    )


# Additional Request Schemas for SDK Operations

@to_dict_without_none
@dataclass
class WorkspaceBackupReq:
    """Request schema for backing up a workspace (v2 API)."""

    backup_file_name: str
    workspace_metadata: Dict[str, Any]


@to_dict_without_none
@dataclass
class WorkspaceRestoreReq:
    """Request schema for restoring a workspace from backup (v2 API)."""

    backup_file_name: str
    workspace_metadata: Dict[str, Any]


@to_dict_without_none
@dataclass
class JobResumeReq:
    """Request schema for resuming a paused job (v2 API)."""

    specs: Dict[str, Any]
    parent_job_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class ModelPublishReq:
    """Request schema for publishing a model to NGC registry (v2 API)."""

    display_name: str
    description: str
    team_name: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class ModelLoadReq:
    """Request schema for loading an air-gapped model (v2 API)."""

    # The exact fields depend on the API specification
    # For now, we'll use a flexible approach that accepts any model data
    model_config: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        # For model loading, we return the model_config directly
        # since it contains the actual model loading parameters
        return self.model_config


# Helper functions for creating request objects

def create_workspace_backup_request(backup_file_name: str, workspace_metadata: Dict[str, Any]) -> WorkspaceBackupReq:
    """Create a structured WorkspaceBackupReq object."""
    return WorkspaceBackupReq(backup_file_name=backup_file_name, workspace_metadata=workspace_metadata)


def create_workspace_restore_request(backup_file_name: str, workspace_metadata: Dict[str, Any]) -> WorkspaceRestoreReq:
    """Create a structured WorkspaceRestoreReq object."""
    return WorkspaceRestoreReq(backup_file_name=backup_file_name, workspace_metadata=workspace_metadata)


def create_job_resume_request(specs: Dict[str, Any], parent_job_id: Optional[str] = None) -> JobResumeReq:
    """Create a structured JobResumeReq object."""
    return JobResumeReq(specs=specs, parent_job_id=parent_job_id)


def create_model_publish_request(display_name: str, description: str, team_name: str) -> ModelPublishReq:
    """Create a structured ModelPublishReq object."""
    return ModelPublishReq(display_name=display_name, description=description, team_name=team_name)


def create_model_load_request(model_config: Dict[str, Any]) -> ModelLoadReq:
    """Create a structured ModelLoadReq object."""
    return ModelLoadReq(model_config=model_config)


@to_dict_without_none
@dataclass
class LoginReq:
    """Request schema for user login authentication (v2 API)."""

    ngc_key: str
    ngc_org_name: str
    enable_telemetry: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@dataclass
class DatasetUpdateReq:
    """Request schema for updating dataset metadata (v2 API)."""

    # This is a flexible schema that accepts any dataset update fields
    update_data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        # For dataset updates, we return the update_data directly
        # since it contains the actual fields to update
        return self.update_data


def create_login_request(ngc_key: str, ngc_org_name: str, enable_telemetry: Optional[bool] = None) -> LoginReq:
    """Create a structured LoginReq object."""
    return LoginReq(ngc_key=ngc_key, ngc_org_name=ngc_org_name, enable_telemetry=enable_telemetry)


def create_dataset_update_request(update_data: Dict[str, Any]) -> DatasetUpdateReq:
    """Create a structured DatasetUpdateReq object."""
    return DatasetUpdateReq(update_data=update_data)


# Additional schemas from V2_API_SPECS_NEW.json
# All schemas are included for completeness, even if not actively used by the SDK

@to_dict_without_none
@dataclass
class AutoML:
    """AutoML configuration schema (v2 API)."""

    automl_enabled: Optional[bool] = None
    automl_algorithm: Optional[str] = None
    automl_max_recommendations: Optional[int] = None
    automl_delete_intermediate_ckpt: Optional[bool] = None
    override_automl_disabled_params: Optional[bool] = None
    automl_r: Optional[int] = None
    automl_nu: Optional[int] = None
    epoch_multiplier: Optional[int] = None
    automl_hyperparameters: Optional[str] = None
    automl_range_override: Optional[List[Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class AutoMLParameterDetail:
    """AutoML parameter detail schema (v2 API)."""

    param_name: Optional[str] = None
    param_type: Optional[str] = None
    param_values: Optional[List[Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class AutoMLParameterDetailsRsp:
    """AutoML parameter details response schema (v2 API)."""

    parameter_details: Optional[List[AutoMLParameterDetail]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                if key == "parameter_details" and value:
                    result[key] = [detail.to_dict() if hasattr(detail, 'to_dict') else detail for detail in value]
                else:
                    result[key] = value
        return result


@to_dict_without_none
@dataclass
class AutoMLResults:
    """AutoML results schema (v2 API)."""

    metric: Optional[str] = None
    value: Optional[float] = None
    epoch: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class AutoMLResultsDetailed:
    """Detailed AutoML results schema (v2 API)."""

    results: Optional[List[AutoMLResults]] = None
    best_model_checkpoint: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                if key == "results" and value:
                    result[key] = [res.to_dict() if hasattr(res, 'to_dict') else res for res in value]
                else:
                    result[key] = value
        return result


@to_dict_without_none
@dataclass
class AutoMLUpdateParameterRangesReq:
    """Request schema for updating AutoML parameter ranges (v2 API)."""

    parameter_ranges: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class BaseExperimentMetadata:
    """Base experiment metadata schema (v2 API)."""

    task: Optional[str] = None
    domain: Optional[str] = None
    backbone_type: Optional[str] = None
    backbone_class: Optional[str] = None
    num_parameters: Optional[str] = None
    accuracy: Optional[str] = None
    license: Optional[str] = None
    model_card_link: Optional[str] = None
    is_backbone: Optional[bool] = None
    is_trainable: Optional[bool] = None
    spec_file_present: Optional[bool] = None
    specs: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class BulkOps:
    """Bulk operations schema (v2 API)."""

    operation: Optional[str] = None
    ids: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class BulkOpsRsp:
    """Bulk operations response schema (v2 API)."""

    successful: Optional[List[str]] = None
    failed: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class Category:
    """Category schema (v2 API)."""

    name: Optional[str] = None
    count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class CategoryWise:
    """Category-wise schema (v2 API)."""

    categories: Optional[List[Category]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                if key == "categories" and value:
                    result[key] = [cat.to_dict() if hasattr(cat, 'to_dict') else cat for cat in value]
                else:
                    result[key] = value
        return result


@to_dict_without_none
@dataclass
class DatasetActions:
    """Dataset actions schema (v2 API)."""

    actions: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class DatasetJob:
    """Dataset job schema (v2 API)."""

    job_id: Optional[str] = None
    status: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class DatasetJobRsp:
    """Dataset job response schema (v2 API)."""

    id: Optional[str] = None
    user_id: Optional[str] = None
    created_on: Optional[str] = None
    last_modified: Optional[str] = None
    kind: Optional[str] = None
    dataset_id: Optional[str] = None
    action: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    parent_job_id: Optional[str] = None
    platform_id: Optional[str] = None
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class DatasetListRsp:
    """Dataset list response schema (v2 API)."""

    datasets: Optional[List[Dict[str, Any]]] = None
    pagination_info: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class DatasetPathLst:
    """Dataset path list schema (v2 API)."""

    paths: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class DatasetRsp:
    """Dataset response schema (v2 API)."""

    id: Optional[str] = None
    user_id: Optional[str] = None
    created_on: Optional[str] = None
    last_modified: Optional[str] = None
    name: Optional[str] = None
    shared: Optional[bool] = None
    description: Optional[str] = None
    docker_env_vars: Optional[Dict[str, Any]] = None
    version: Optional[str] = None
    logo: Optional[str] = None
    type: Optional[str] = None
    format: Optional[str] = None
    workspace: Optional[str] = None
    url: Optional[str] = None
    cloud_file_path: Optional[str] = None
    actions: Optional[List[str]] = None
    jobs: Optional[Dict[str, Any]] = None
    client_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    filters: Optional[str] = None
    status: Optional[str] = None
    use_for: Optional[List[str]] = None
    base_experiment_pull_complete: Optional[str] = None
    base_experiment_ids: Optional[List[str]] = None
    skip_validation: Optional[bool] = None
    authorized_party_nca_id: Optional[str] = None
    validation_details: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class DetailedStatus:
    """Detailed status schema (v2 API)."""

    status: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class ErrorRsp:
    """Error response schema (v2 API)."""

    error: Optional[str] = None
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class ExperimentActions:
    """Experiment actions schema (v2 API)."""

    actions: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class ExperimentJobRsp:
    """Experiment job response schema (v2 API)."""

    id: Optional[str] = None
    user_id: Optional[str] = None
    created_on: Optional[str] = None
    last_modified: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    network_arch: Optional[str] = None
    encryption_key: Optional[str] = None
    workspace: Optional[str] = None
    action: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    base_experiment_ids: Optional[List[str]] = None
    automl_settings: Optional[Dict[str, Any]] = None
    train_datasets: Optional[List[str]] = None
    eval_dataset: Optional[str] = None
    inference_dataset: Optional[str] = None
    calibration_dataset: Optional[str] = None
    parent_job_id: Optional[str] = None
    platform_id: Optional[str] = None
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class GpuDetails:
    """GPU details schema (v2 API)."""

    gpu_type: Optional[str] = None
    gpu_memory: Optional[str] = None
    gpu_count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class Graph:
    """Graph schema (v2 API)."""

    nodes: Optional[List[Dict[str, Any]]] = None
    edges: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class InferenceMicroserviceRsp:
    """Inference microservice response schema (v2 API)."""

    id: Optional[str] = None
    status: Optional[str] = None
    docker_image: Optional[str] = None
    created_on: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class JobListRsp:
    """Job list response schema (v2 API)."""

    jobs: Optional[List[Dict[str, Any]]] = None
    pagination_info: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class JobResult:
    """Job result schema (v2 API)."""

    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    artifacts: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class JobResume:
    """Job resume schema (v2 API)."""

    parent_job_id: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class JobRsp:
    """Job response schema (v2 API)."""

    id: Optional[str] = None
    user_id: Optional[str] = None
    created_on: Optional[str] = None
    last_modified: Optional[str] = None
    kind: Optional[str] = None
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class JobSubset:
    """Job subset schema (v2 API)."""

    job_id: Optional[str] = None
    status: Optional[str] = None
    action: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class KPI:
    """Key Performance Indicator schema (v2 API)."""

    name: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class LoadAirgappedExperimentsReq:
    """Load air-gapped experiments request schema (v2 API)."""

    model_file: Optional[str] = None
    workspace_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class LoadAirgappedExperimentsRsp:
    """Load air-gapped experiments response schema (v2 API)."""

    experiment_id: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class LoginRsp:
    """Login response schema (v2 API)."""

    user_id: Optional[str] = None
    token: Optional[str] = None
    org_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class LstStr:
    """List of strings schema (v2 API)."""

    items: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class MessageOnly:
    """Message-only schema (v2 API)."""

    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class MissingFile:
    """Missing file schema (v2 API)."""

    file_path: Optional[str] = None
    required: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class NVCFReq:
    """NVCF request schema (v2 API)."""

    function_id: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class PaginationInfo:
    """Pagination information schema (v2 API)."""

    page: Optional[int] = None
    size: Optional[int] = None
    total: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class ParameterRangeSchema:
    """Parameter range schema (v2 API)."""

    parameter_name: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class PublishModel:
    """Publish model schema (v2 API)."""

    display_name: Optional[str] = None
    description: Optional[str] = None
    team_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class Stats:
    """Statistics schema (v2 API)."""

    count: Optional[int] = None
    average: Optional[float] = None
    total: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class ValidationDetails:
    """Validation details schema (v2 API)."""

    is_valid: Optional[bool] = None
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class WorkspaceListRsp:
    """Workspace list response schema (v2 API)."""

    workspaces: Optional[List[Dict[str, Any]]] = None
    pagination_info: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class WorkspaceRsp:
    """Workspace response schema (v2 API)."""

    id: Optional[str] = None
    user_id: Optional[str] = None
    created_on: Optional[str] = None
    last_modified: Optional[str] = None
    name: Optional[str] = None
    shared: Optional[bool] = None
    version: Optional[str] = None
    cloud_type: Optional[str] = None
    cloud_specific_details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class huggingface:
    """HuggingFace cloud configuration schema (v2 API)."""

    token: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@to_dict_without_none
@dataclass
class seaweedfs:
    """SeaweedFS cloud configuration schema (v2 API)."""

    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    endpoint_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result
