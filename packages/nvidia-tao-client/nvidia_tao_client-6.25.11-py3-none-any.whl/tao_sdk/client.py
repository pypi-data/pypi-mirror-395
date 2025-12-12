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

"""TAO SDK Client."""

import json
import logging
import os
import time
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

import requests

from .exceptions import (
    TaoError,
    TaoAuthenticationError,
    TaoAPIError,
    TaoNotFoundError,
    TaoValidationError,
)
from .schemas import (
    create_experiment_job_request,
    create_dataset_job_request,
    create_inference_microservice_request,
    create_inference_request,
    create_workspace_request,
    create_dataset_request,
    create_aws_cloud_pull_request,
    create_azure_cloud_pull_request,
    create_huggingface_cloud_pull_request,
    create_seaweedfs_cloud_pull_request,
    create_workspace_backup_request,
    create_workspace_restore_request,
    create_job_resume_request,
    create_model_publish_request,
    create_model_load_request,
    create_login_request,
    create_dataset_update_request,
    InferenceMicroserviceReq,
    InferenceReq,
    WorkspaceReq,
    DatasetReq,
    AWSCloudPull,
    AzureCloudPull,
    HuggingFaceCloudPull,
    SeaweedFSCloudPull,
    CloudSpecificDetails,
    JobReq,
    WorkspaceBackupReq,
    WorkspaceRestoreReq,
    JobResumeReq,
    ModelPublishReq,
    ModelLoadReq,
    LoginReq,
    DatasetUpdateReq,
)

# Set up logger for TAO SDK
logger = logging.getLogger(__name__)


def _get_tao_config_path() -> Path:
    """Get the path to the TAO config file."""
    return Path.home() / ".tao" / "config"


def _load_tao_config() -> Dict[str, str]:
    """Load TAO configuration from ~/.tao/config file.

    Returns:
        Dict containing TAO_BASE_URL, TAO_ORG, TAO_TOKEN if available
    """
    config_path = _get_tao_config_path()
    config = {}

    if config_path.exists():
        try:
            parser = ConfigParser()
            parser.read(config_path)

            # Read from [CURRENT] section, fall back to DEFAULT section if needed
            if parser.has_section('CURRENT'):
                section = parser['CURRENT']
            elif parser.has_section('DEFAULT') or len(parser.defaults()) > 0:
                section = parser['DEFAULT']
            else:
                section = {}

            # Extract the values we need
            for key in ['TAO_BASE_URL', 'TAO_ORG', 'TAO_TOKEN']:
                if key in section:
                    config[key] = section[key]

        except Exception:
            # If config file is corrupted or unreadable, return empty config
            pass

    return config


def _save_tao_config(tao_base_url: str, tao_org: str, tao_token: str) -> None:
    """Save TAO configuration to ~/.tao/config file in .ini format.

    Args:
        tao_base_url: TAO API base URL
        tao_org: NGC organization name
        tao_token: JWT authentication token

    Creates config file with [CURRENT] section containing credentials.
    """
    config_path = _get_tao_config_path()

    # Create directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Create ConfigParser and add [CURRENT] section
    parser = ConfigParser()
    parser.add_section('CURRENT')
    parser.set('CURRENT', 'TAO_BASE_URL', tao_base_url)
    parser.set('CURRENT', 'TAO_ORG', tao_org)
    parser.set('CURRENT', 'TAO_TOKEN', tao_token)

    # Write to file
    with open(config_path, 'w') as f:
        parser.write(f)

    # Set secure permissions (read and write for current user only)
    config_path.chmod(0o600)


def _clear_tao_config() -> None:
    """Clear TAO configuration by removing ~/.tao/config file."""
    config_path = _get_tao_config_path()
    if config_path.exists():
        config_path.unlink()


class TaoClient:
    """Python SDK client for NVIDIA TAO Toolkit API.

    This client provides programmatic access to all TAO functionality including:
    - Authentication and login
    - Workspace management
    - Dataset operations
    - Job execution and monitoring
    - Model publishing

    Example:
        >>> client = TaoClient()
        >>> client.login(ngc_key="your_key", ngc_org_name="your_org")
        >>> jobs = client.list_jobs()
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        org_name: Optional[str] = None,
        token: Optional[str] = None,
        timeout: int = 3600 * 24,
    ):
        """Initialize the TAO Client.

        Args:
            base_url: Base URL for TAO API. If None, will check env vars then config file.
            org_name: NGC organization name. If None, will check env vars then config file.
            token: Authentication token. If None, will check env vars then config file.
            timeout: Request timeout in seconds.

        Credential Loading Order:
            1. Provided arguments (highest priority)
            2. Environment variables (TAO_BASE_URL, TAO_ORG, TAO_TOKEN)
            3. Config file (~/.tao/config) (lowest priority)

        Environment Variables:
            - TAO_BASE_URL: API base URL (validated when making API calls)
            - TAO_ORG: NGC organization name
            - TAO_TOKEN: Authentication token
            - LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Note:
            TAO_BASE_URL validation occurs when making API calls, not during initialization.
            This allows for flexible initialization patterns and lazy configuration.
        """
        self.timeout = timeout

        # Load from config file
        config = _load_tao_config()

        # Load from environment variables with fallbacks to legacy env vars and config file
        default_org = os.getenv("TAO_ORG", os.getenv("ORG", config.get("TAO_ORG", "noorg")))
        default_token = os.getenv("TAO_TOKEN", os.getenv("TOKEN", config.get("TAO_TOKEN", "invalid")))
        default_base_url = os.getenv("TAO_BASE_URL", os.getenv("BASE_URL", config.get("TAO_BASE_URL")))

        # Use provided values or fall back to env vars/config
        self.org_name = org_name or default_org
        self.token = token or default_token
        self._raw_base_url = base_url or default_base_url

        # Configure logger level based on LOG_LEVEL environment variable
        self._configure_logging()

        # Store base URL (will be validated when making requests)
        self.base_url = None
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _configure_logging(self) -> None:
        """Configure logger level based on LOG_LEVEL environment variable.

        Supported LOG_LEVEL values:
        - DEBUG: Show all debug messages including request details
        - INFO: Show general information messages
        - WARNING: Show warnings and errors only
        - ERROR: Show errors only
        - CRITICAL: Show only critical errors

        If LOG_LEVEL is not set or invalid, logger level remains unchanged.
        """
        log_level_str = os.getenv("LOG_LEVEL", "").upper()

        # Map string values to logging constants
        log_level_mapping = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "WARN": logging.WARNING,  # Alternative spelling
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
            "FATAL": logging.CRITICAL,  # Alternative spelling
        }

        if log_level_str in log_level_mapping:
            log_level = log_level_mapping[log_level_str]
            logger.setLevel(log_level)

            # Also configure the root logger if no handlers are configured yet
            # This helps ensure the messages actually get displayed
            if not logging.getLogger().handlers:
                logging.basicConfig(
                    level=log_level,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )

    def _ensure_credentials(self) -> None:
        """Ensure all credentials (base_url, org, token) are configured before making API requests.

        Credential Loading Order for API calls (excluding login):
            1. SDK client constructor values (highest priority)
            2. Environment variables (TAO_BASE_URL, TAO_ORG, TAO_TOKEN)
            3. Config file (~/.tao/config) (lowest priority)

        Raises:
            TaoAuthenticationError: If credentials are not found or invalid
        """
        if self.base_url is not None:
            # Already validated and constructed
            return

        # Load credentials using precedence order
        base_url = None
        org_name = None
        token = None

        # 1. Use SDK client constructor values (highest priority)
        if self._raw_base_url and self.org_name and self.token:
            if (self._raw_base_url.strip() and self.org_name.strip() and
                self.token.strip() and self.token != "invalid" and self.org_name != "noorg"):
                base_url = self._raw_base_url.strip()
                org_name = self.org_name.strip()
                token = self.token.strip()

        # 2. Use environment variables if constructor values not complete
        if not (base_url and org_name and token):
            env_base_url = os.getenv("TAO_BASE_URL")
            env_org = os.getenv("TAO_ORG")
            env_token = os.getenv("TAO_TOKEN")

            if (env_base_url and env_org and env_token and
                env_base_url.strip() and env_org.strip() and env_token.strip()):
                base_url = env_base_url.strip()
                org_name = env_org.strip()
                token = env_token.strip()

        # 3. Use config file if other sources not complete (lowest priority)
        if not (base_url and org_name and token):
            config = _load_tao_config()
            config_base_url = config.get("TAO_BASE_URL")
            config_org = config.get("TAO_ORG")
            config_token = config.get("TAO_TOKEN")

            if (config_base_url and config_org and config_token and
                config_base_url.strip() and config_org.strip() and config_token.strip()):
                base_url = config_base_url.strip()
                org_name = config_org.strip()
                token = config_token.strip()

        # Validate that we found all required credentials
        if not (base_url and org_name and token):
            raise TaoAuthenticationError(
                "Authentication credentials not found. Please run 'tao login' first, "
                "or set TAO_BASE_URL, TAO_ORG, and TAO_TOKEN environment variables, "
                "or provide credentials when creating TaoClient(base_url=..., org_name=..., token=...)."
            )

        # Normalize base_url (ensure it ends with /api/v2)
        clean_base_url = base_url.rstrip('/')
        if not clean_base_url.endswith('/api/v2'):
            clean_base_url = clean_base_url + '/api/v2'

        # Update client instance with validated credentials
        self._raw_base_url = clean_base_url
        self.org_name = org_name
        self.token = token
        self.base_url = f"{clean_base_url}/orgs/{org_name}"
        self.headers = {"Authorization": f"Bearer {token}"}

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        expected_status: tuple = (200, 201),
        stream: bool = False,
    ) -> requests.Response:
        """Make an HTTP request with error handling.

        Automatically loads credentials from available sources before making the request.

        Credential Loading Order:
            1. SDK client constructor values (highest priority)
            2. Environment variables (TAO_BASE_URL, TAO_ORG, TAO_TOKEN)
            3. Config file (~/.tao/config) (lowest priority)

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint
            data: Request data (will be JSON serialized)
            params: Query parameters
            expected_status: Expected HTTP status codes
            stream: Whether to stream the response

        Returns:
            requests.Response object

        Raises:
            TaoAPIError: For API errors
            TaoAuthenticationError: For authentication errors or missing credentials
            TaoNotFoundError: For 404 errors
        """
        # Ensure all credentials are configured before making the request
        self._ensure_credentials()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Copy headers to avoid modifying the original
        headers = self.headers.copy()

        kwargs = {
            "headers": headers,
            "timeout": self.timeout,
            "stream": stream,
        }

        if data is not None:
            kwargs["data"] = json.dumps(data)
            # Add Content-Type header for JSON data as required by v2 API
            headers["Content-Type"] = "application/json"

        if params is not None:
            kwargs["params"] = params

        # Log the request details for debugging
        self._log_request(method, url, headers, data, params)

        try:
            response = requests.request(method, url, **kwargs)
        except requests.RequestException as e:
            raise TaoAPIError(f"Request failed: {str(e)}")

        if response.status_code == 401:
            raise TaoAuthenticationError("Authentication failed. Check your token.")
        elif response.status_code == 404:
            raise TaoNotFoundError("Resource not found.", response.status_code, response.text)
        elif response.status_code not in expected_status:
            raise TaoAPIError(
                f"Request failed with status {response.status_code}: {response.text}",
                response.status_code,
                response.text,
            )

        return response

    def _log_request(self, method: str, url: str, headers: Dict[str, str], data: Optional[Dict] = None, params: Optional[Dict] = None) -> None:
        """Log request details for debugging.

        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers
            data: Request data/payload
            params: Query parameters
        """
        if logger.isEnabledFor(logging.DEBUG):
            # Create a copy of headers and mask sensitive information
            safe_headers = headers.copy()
            if 'Authorization' in safe_headers:
                auth_value = safe_headers['Authorization']
                if auth_value.startswith('Bearer '):
                    # Show only first 10 chars of token for debugging
                    token = auth_value[7:]  # Remove 'Bearer '
                    safe_headers['Authorization'] = f'Bearer {token[:10]}...'

            logger.debug(f"TAO API Request: {method.upper()} {url}")
            logger.debug(f"Headers: {safe_headers}")

            if params:
                logger.debug(f"Query Parameters: {params}")

            if data:
                # For large payloads, show only a summary
                if isinstance(data, dict):
                    data_summary = {k: f"<{type(v).__name__}>" if len(str(v)) > 100 else v for k, v in data.items()}
                    logger.debug(f"Request Data: {json.dumps(data_summary, indent=2)}")
                else:
                    logger.debug(f"Request Data: {data}")

    # Authentication methods
    def login(
        self,
        ngc_key: str,
        ngc_org_name: str,
        enable_telemetry: Optional[bool] = None,
        tao_base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Login to TAO API and save credentials to config file.

        Args:
            ngc_key: NGC personal API key
            ngc_org_name: NGC organization name
            enable_telemetry: Whether to enable telemetry collection
            tao_base_url: TAO API base URL (optional)

        Returns:
            Dict containing login response with token and user info

        TAO_BASE_URL Loading Order:
            1. tao_base_url argument (highest priority)
            2. SDK client constructor base_url
            3. TAO_BASE_URL environment variable
            4. TAO_BASE_URL in ~/.tao/config (lowest priority)

        Config File:
            Upon successful login, saves credentials to ~/.tao/config file:
            - TAO_BASE_URL: TAO API base URL
            - TAO_ORG: NGC organization name
            - TAO_TOKEN: JWT authentication token

        Raises:
            TaoAuthenticationError: If TAO_BASE_URL not found in any source or login fails

        Note:
            Credentials are persisted to ~/.tao/config file for use across sessions.
            For CLI usage, use: `tao login`
        """
        # Determine base_url using priority order
        base_url = None

        # 1. Use tao_base_url argument (highest priority)
        if tao_base_url:
            base_url = tao_base_url.strip()

        # 2. Use SDK client constructor base_url
        elif self._raw_base_url:
            base_url = self._raw_base_url.strip()

        # 3. Use TAO_BASE_URL environment variable
        elif os.getenv("TAO_BASE_URL"):
            base_url = os.getenv("TAO_BASE_URL").strip()

        # 4. Use TAO_BASE_URL from ~/.tao/config (lowest priority)
        else:
            config = _load_tao_config()
            if config.get("TAO_BASE_URL"):
                base_url = config.get("TAO_BASE_URL").strip()

        # Validate that we found a base_url from one of the sources
        if not base_url:
            raise TaoAuthenticationError(
                "TAO_BASE_URL not found. Please set the TAO base URL using one of these methods:\n"
                "1. Pass tao_base_url argument to login()\n"
                "2. Set TAO_BASE_URL when creating TaoClient(base_url=...)\n"
                "3. Set TAO_BASE_URL environment variable\n"
                "4. Save TAO_BASE_URL in ~/.tao/config file"
            )

        # Normalize base_url (ensure it ends with /api/v2)
        clean_base_url = base_url.rstrip('/')
        if not clean_base_url.endswith('/api/v2'):
            clean_base_url = clean_base_url + '/api/v2'
        base_url = clean_base_url

        endpoint = base_url + "/login"

        login_req = create_login_request(ngc_key, ngc_org_name, enable_telemetry)
        response = requests.post(endpoint, data=json.dumps(login_req.to_dict()), timeout=600)

        if response.status_code not in (200, 201):
            raise TaoAuthenticationError(
                f"Login failed with status {response.status_code}: {response.text}"
            )

        creds = response.json()
        token = creds.get("token", "invalid")

        # Save credentials to config file (TAO_BASE_URL, TAO_ORG, TAO_TOKEN)
        _save_tao_config(base_url, ngc_org_name, token)

        # Update client instance with new credentials
        self.org_name = ngc_org_name
        self.token = token
        self._raw_base_url = base_url
        self.base_url = f"{base_url}/orgs/{self.org_name}"
        self.headers = {"Authorization": f"Bearer {self.token}"}

        return creds

    def logout(self) -> Dict[str, str]:
        """Clear saved authentication credentials from config file.

        Removes ~/.tao/config file and resets client credentials.
        For CLI usage, use the command: `tao logout`

        Returns:
            Dict containing logout confirmation message
        """
        # Clear config file
        _clear_tao_config()

        # Clear current client credentials
        self.token = "invalid"
        self.headers = {"Authorization": "Bearer invalid"}

        return {"message": "Successfully logged out and cleared config file"}

    def is_authenticated(self) -> bool:
        """Check if the client has valid authentication credentials.

        Returns:
            True if authenticated with valid credentials, False otherwise
        """
        if not self.token or self.token == "invalid":
            return False

        # Try a simple API call to verify credentials
        try:
            self._make_request("GET", "workspaces", params={"limit": 1})
            return True
        except (TaoAuthenticationError, TaoAPIError):
            return False
        except Exception:
            # Any other error (network, etc.) - assume credentials might be valid
            return True

    def require_authentication(self):
        """Ensure the client is authenticated, raise error if not.

        Raises:
            TaoAuthenticationError: If not authenticated
        """
        if not self.is_authenticated():
            raise TaoAuthenticationError(
                "Authentication required. Please run 'tao login' to authenticate."
            )

    def get_gpu_types(self) -> List[Dict[str, Any]]:
        """Get available GPU types for job execution.

        Returns:
            List of available GPU types with specifications
        """
        response = self._make_request("GET", "jobs:gpu_types")
        return response.json()

    # Workspace methods
    def create_workspace(
        self,
        name: str,
        cloud_type: str,
        cloud_specific_details: Union[Dict[str, Any], CloudSpecificDetails],
        shared: Optional[bool] = None,
        version: Optional[str] = None,
    ) -> str:
        """Create a new workspace using WorkspaceReq schema.

        Args:
            name: Workspace name
            cloud_type: Cloud storage type ("aws", "azure", "seaweedfs", "huggingface", "self_hosted")
            cloud_specific_details: Cloud-specific configuration (dict or structured cloud config)
            shared: Whether workspace is shared (optional)
            version: Workspace version (optional)

        Returns:
            Workspace ID
        """
        # Create structured WorkspaceReq using schema
        workspace_req = create_workspace_request(
            name=name,
            cloud_type=cloud_type,
            cloud_specific_details=cloud_specific_details,
            shared=shared,
            version=version
        )

        response = self._make_request("POST", "workspaces", data=workspace_req.to_dict())
        result = response.json()

        if "id" not in result:
            raise TaoValidationError(f"ID not present in response: {result}")

        return result["id"]

    def backup_workspace(self, backup_file_name: str, workspace_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Backup a workspace.

        Args:
            backup_file_name: Name for the backup file
            workspace_metadata: Workspace metadata

        Returns:
            Backup operation response
        """
        backup_req = create_workspace_backup_request(backup_file_name, workspace_metadata)
        response = self._make_request("POST", "workspaces:backup", data=backup_req.to_dict())
        return response.json()

    def restore_workspace(self, backup_file_name: str, workspace_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Restore a workspace from backup.

        Args:
            backup_file_name: Name of the backup file to restore from
            workspace_metadata: Workspace metadata

        Returns:
            Restore operation response
        """
        restore_req = create_workspace_restore_request(backup_file_name, workspace_metadata)
        response = self._make_request("POST", f"workspaces:restore", data=restore_req.to_dict())
        return response.json()

    def delete_workspace(self, workspace_id: str) -> Dict[str, Any]:
        """Delete a workspace. Cancels all related running jobs and removes the workspace.

        Args:
            workspace_id: Workspace ID to delete

        Returns:
            Information about the deleted workspace
        """
        response = self._make_request("DELETE", f"workspaces/{workspace_id}")
        return response.json()

    def list_workspaces(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List workspaces accessible to the user.

        Args:
            filter_params: Optional dictionary of filter parameters

        Returns:
            List of workspace dictionaries
        """
        params = filter_params or {}
        response = self._make_request("GET", "workspaces", params=params)
        result = response.json()
        # v2 API may return workspaces directly or in a wrapper object
        return result if isinstance(result, list) else result.get("workspaces", [])

    def get_workspace_metadata(self, workspace_id: str) -> Dict[str, Any]:
        """Get metadata for a specific workspace.

        Args:
            workspace_id: Workspace ID

        Returns:
            Workspace metadata dictionary
        """
        response = self._make_request("GET", f"workspaces/{workspace_id}")
        return response.json()

    # Dataset methods
    def create_dataset(
        self,
        dataset_type: str,
        dataset_format: str,
        workspace_id: Optional[str] = None,
        cloud_file_path: Optional[str] = None,
        url: Optional[str] = None,
        use_for: Optional[List[str]] = None,
    ) -> str:
        """Create a new dataset using DatasetReq schema.

        Args:
            dataset_type: Type of dataset (e.g., "image_classification", "object_detection")
            dataset_format: Format of the dataset (e.g., "coco", "classification_pyt")
            workspace_id: Workspace ID (optional)
            cloud_file_path: Path to dataset in cloud storage (optional)
            url: Public URL to dataset (optional)
            use_for: List of purposes (training, evaluation, testing) (optional)

        Returns:
            Dataset ID
        """
        # Create structured DatasetReq using schema
        dataset_req = create_dataset_request(
            dataset_type=dataset_type,
            dataset_format=dataset_format,
            workspace=workspace_id,
            cloud_file_path=cloud_file_path,
            url=url,
            use_for=use_for
        )

        response = self._make_request("POST", "datasets", data=dataset_req.to_dict())
        result = response.json()

        if "id" not in result:
            raise TaoValidationError(f"ID not present in response: {result}")

        return result["id"]


    def list_datasets(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List available datasets.

        Args:
            filter_params: Optional filtering parameters

        Returns:
            List of datasets
        """
        response = self._make_request("GET", "datasets", params=filter_params)
        return response.json()["datasets"]

    def get_dataset_metadata(self, dataset_id: str) -> Dict[str, Any]:
        """Get metadata for a specific dataset.

        Args:
            dataset_id: Dataset ID

        Returns:
            Dataset metadata
        """
        response = self._make_request("GET", f"datasets/{dataset_id}")
        return response.json()

    def update_dataset_metadata(
        self, dataset_id: str, update_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update dataset metadata.

        Args:
            dataset_id: Dataset ID
            update_info: Dictionary containing fields to update. Supported fields:
                - name: Dataset name
                - description: Dataset description
                - version: Version string
                - logo: Logo URL
                - shared: Boolean for shared access
                - base_experiment_ids: List of base experiment IDs
                - authorized_party_nca_id: Authorized party ID
                - cloud_file_path: Cloud file path (triggers re-pull if status is pull_complete or invalid_pull)
                - docker_env_vars: Docker environment variables
                - public: Boolean for public visibility
                - tags: List of tags

        Returns:
            Updated dataset metadata

        Raises:
            TaoValidationError: If update_info is empty or invalid
            TaoAPIError: If the update fails

        Note:
            - Fields 'type' and 'format' are immutable and cannot be changed
            - Updating 'cloud_file_path' triggers a dataset re-pull
        """
        if not update_info or not isinstance(update_info, dict):
            raise TaoValidationError("update_info must be a non-empty dictionary")

        update_req = create_dataset_update_request(update_info)
        response = self._make_request("PATCH", f"datasets/{dataset_id}", data=update_req.to_dict())
        return response.json()

    def delete_dataset(self, dataset_id: str) -> None:
        """Delete a dataset.

        Args:
            dataset_id: Dataset ID to delete
        """
        self._make_request("DELETE", f"datasets/{dataset_id}")

    # Experiment methods
    # create_experiment removed - use create_job() with ExperimentJobReq instead in v2 API

    # list_experiments removed - use list_jobs() instead in v2 API

    def list_base_experiments(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List available base experiments (v2 API).

        Base experiments are pre-configured experiment templates that can be used
        as starting points for creating new experiment jobs.

        Args:
            filter_params: Optional filtering parameters

        Returns:
            List of base experiments available for job creation
        """
        response = self._make_request("GET", "jobs:list_base_experiments", params=filter_params)
        result = response.json()
        # Handle both possible response formats for backward compatibility
        if "experiments" in result:
            return result["experiments"]
        return result

    # v1 experiment metadata methods removed - not applicable to v2 API
    # In v2 API, everything is job-based. Use job methods instead:

    # Job execution methods
    def get_job_specs(
        self, artifact_id: str, action: Optional[str] = None, artifact_type: str = "experiment"
    ) -> Dict[str, Any]:
        """Get specification schema for a job action.

        This method is deprecated in favor of get_job_schema() for v2 API compatibility.

        Args:
            artifact_id: Base experiment or dataset ID
            action: Action name (train, evaluate, inference, etc.)
            artifact_type: Type of artifact ("experiment", "base_experiment" or "dataset")

        Returns:
            Job specification
        """
        # For v2 API, determine schema parameters based on artifact type
        if artifact_type == "experiment":
            # For experiment jobs, use base_experiment_id if available
            result = self.get_job_schema(action=action, job_id=artifact_id)
            return result.get("default", {})
        elif artifact_type == "base_experiment":
            result = self.get_job_schema(action=action, base_experiment_id=artifact_id)
            return result.get("default", {})
        else:
            # For dataset jobs, just use action (no dataset_id parameter in get_job_schema)
            return self.get_job_schema(action=action)

    def get_job_schema(
        self,
        job_id: Optional[str] = None,
        base_experiment_id: Optional[str] = None,
        network_arch: Optional[str] = None,
        action: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get job specification schema using the unified v2 endpoint.

        Args:
            job_id: Job ID (for getting schema from existing job)
            base_experiment_id: Base experiment ID (for getting schema for new job)
            network_arch: Network architecture (for getting schema for new job)
            action: Action name (for getting schema for new job)

        Returns:
            Job specification schema
        """
        params = {}
        if job_id:
            params["job_id"] = job_id
        if base_experiment_id:
            params["base_experiment_id"] = base_experiment_id
        if network_arch:
            params["network_arch"] = network_arch
        if action:
            params["action"] = action

        while True:
            try:
                response = self._make_request("GET", "jobs:schema", params=params)
                break
            except TaoNotFoundError as e:
                if "Base spec file download state is " in str(e.response_text):
                    print("Base experiment spec file is being downloaded")
                    time.sleep(2)
                    continue
                raise

        result = response.json()
        # Return the default schema or the full response based on structure
        return result

    def get_automl_defaults(
        self,
        base_experiment_id: Optional[str] = None,
        network_arch: Optional[str] = None,
        action: Optional[str] = None,
    ) -> Dict[str, Any]:

        """Get AutoML default parameters for an experiment.

        Args:
            base_experiment_id: Base Experiment ID
            action: Action name (usually "train")

        Returns:
            AutoML default parameters
        """
        # Use the unified v2 schema endpoint
        if not (base_experiment_id or network_arch):
            raise TaoValidationError("base_experiment_id or network_arch is required")
        params = {"action": "train"}
        if base_experiment_id:
            params["base_experiment_id"] = base_experiment_id
        if network_arch:
            params["network_arch"] = network_arch
        if action:
            params["action"] = action
        response = self._make_request("GET", "jobs:schema", params=params)
        result = response.json()

        # Return automl_default_parameters if available, otherwise empty dict
        return result.get("automl_default_parameters", {})

    def get_automl_param_details(
        self,
        network_arch: str,
        parameters: Union[str, List[str]],
    ) -> Dict[str, Any]:
        """Get AutoML parameter details for specific parameters.

        Args:
            network_arch: Network architecture name (e.g., "cosmos-rl")
            parameters: Single parameter name or list of parameter names
                       (e.g., "train.optm_decay_type" or ["train.epoch", "train.optm_lr"])

        Returns:
            Dictionary with parameter details including valid ranges, data types, and default values
        """
        # Convert list to comma-separated string if needed
        if isinstance(parameters, list):
            parameters = ",".join(parameters)

        params = {
            "network_arch": network_arch,
            "parameters": parameters
        }
        response = self._make_request("GET", "automl:get_param_details", params=params)
        return response.json()

    def create_job(
        self,
        kind: str,
        action: str,
        specs: Dict[str, Any],
        name: Optional[str] = None,
        description: Optional[str] = None,
        network_arch: Optional[str] = None,
        encryption_key: Optional[str] = None,
        workspace: Optional[str] = None,
        docker_env_vars: Optional[Dict[str, Any]] = None,
        base_experiment_ids: Optional[List[str]] = None,
        dataset_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        parent_job_id: Optional[str] = None,
        platform_id: Optional[str] = None,
        automl_settings: Optional[Dict[str, Any]] = None,
        train_datasets: Optional[List[str]] = None,
        eval_dataset: Optional[str] = None,
        inference_dataset: Optional[str] = None,
        calibration_dataset: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a unified job (v2 API).

        This is the primary method for creating jobs in API v2. It supports both
        experiment and dataset jobs in a single unified interface using structured
        ExperimentJobReq or DatasetJobReq message bodies.

        Args:
            kind: Job type ("experiment" or "dataset")
            action: Action to run (train, evaluate, inference, etc.)
            specs: Action specifications
            name: Job/experiment name (required for experiment jobs)
            description: Job/experiment description (optional)
            network_arch: Network architecture (required for experiment jobs)
            encryption_key: Encryption key (required for experiment jobs)
            workspace: Workspace ID (required for experiment jobs)
            base_experiment_ids: List of base experiment IDs (optional)
            dataset_id: Dataset ID (required for dataset jobs)
            tags: List of tags (optional)
            parent_job_id: Parent job ID (optional)
            platform_id: Platform ID for NVCF backend (optional)
            automl_settings: AutoML configuration dictionary (optional)
            train_datasets: List of training dataset IDs (optional)
            eval_dataset: Evaluation dataset ID (optional)
            inference_dataset: Inference dataset ID (optional)
            calibration_dataset: Calibration dataset ID (optional)

        Returns:
            Job ID
        """
        if kind == "experiment":
            # Validate required experiment fields
            if not name:
                raise TaoValidationError("name is required for experiment jobs")
            if not network_arch:
                raise TaoValidationError("network_arch is required for experiment jobs")
            if not workspace:
                raise TaoValidationError("workspace is required for experiment jobs")

            # Create structured ExperimentJobReq message body
            experiment_job_req = create_experiment_job_request(
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
            data = experiment_job_req.to_dict()

        elif kind == "dataset":
            # Validate required dataset fields
            if not dataset_id:
                raise TaoValidationError("dataset_id is required for dataset jobs")

            # Create structured DatasetJobReq message body
            dataset_job_req = create_dataset_job_request(
                dataset_id=dataset_id,
                action=action,
                specs=specs,
                tags=tags,
                parent_job_id=parent_job_id,
                platform_id=platform_id,
            )
            data = dataset_job_req.to_dict()
        else:
            raise TaoValidationError(f"Invalid job kind: {kind}. Must be 'experiment' or 'dataset'")

        response = self._make_request("POST", "jobs", data=data, expected_status=(201,))
        result = response.json()

        if "id" not in result:
            raise TaoValidationError(f"ID not present in response: {result}")

        return result["id"]


    def list_jobs(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List jobs using the unified v2 endpoint.

        Args:
            filter_params: Optional filtering parameters (network_arch, status, kind, etc.)

        Returns:
            List of jobs with polymorphic fields based on job kind
        """
        response = self._make_request("GET", "jobs", params=filter_params)
        # v2 API may return jobs directly or in a wrapper object
        result = response.json()
        jobs = result if isinstance(result, list) else result.get("jobs", [])

        # Process each job response to handle polymorphic fields
        return [self._process_job_response(job) for job in jobs]

    def get_job_metadata(self, job_id: str) -> Dict[str, Any]:
        """Get metadata for a specific job using the unified v2 endpoint.

        Args:
            job_id: Job ID

        Returns:
            Job metadata dictionary with polymorphic fields based on job kind
        """
        response = self._make_request("GET", f"jobs/{job_id}")
        job_data = response.json()

        # Process polymorphic response - v2 jobs have a 'kind' field
        # that determines which fields are present
        return self._process_job_response(job_data)


    def _process_job_response(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a job response and handle polymorphic fields.

        Args:
            job_data: Raw job response data

        Returns:
            Processed job data with type-specific fields
        """
        if not isinstance(job_data, dict):
            return job_data

        # v2 jobs have a 'kind' field that determines the schema
        kind = job_data.get("kind")

        if kind == "experiment":
            # Experiment jobs have fields like name, network_arch, description, etc.
            # These are already in the response, no processing needed
            pass
        elif kind == "dataset":
            # Dataset jobs have fields like dataset_id
            # These are already in the response, no processing needed
            pass

        # For backward compatibility, we can add some computed fields
        # if needed by existing code

        return job_data

    def is_experiment_job(self, job_data: Dict[str, Any]) -> bool:
        """Check if a job is an experiment job.

        Args:
            job_data: Job response data

        Returns:
            True if it's an experiment job, False otherwise
        """
        return job_data.get("kind") == "experiment"

    def is_dataset_job(self, job_data: Dict[str, Any]) -> bool:
        """Check if a job is a dataset job.

        Args:
            job_data: Job response data

        Returns:
            True if it's a dataset job, False otherwise
        """
        return job_data.get("kind") == "dataset"

    def get_job_kind(self, job_data: Dict[str, Any]) -> Optional[str]:
        """Get the kind of job.

        Args:
            job_data: Job response data

        Returns:
            Job kind ("experiment" or "dataset") or None if not specified
        """
        return job_data.get("kind")

    # run_action method removed - v1 backward compatibility not needed in v2-only SDK
    # Use create_job() instead for unified job creation

    # get_job_status method removed - v1 backward compatibility not needed in v2-only SDK
    # Use get_job(job_id) instead for unified job status retrieval

    def cancel_job(self, job_id: str) -> None:
        """Cancel a running job.

        Args:
            job_id: Job ID
        """
        self._make_request("POST", f"jobs/{job_id}:cancel")

    def update_job(
        self,
        job_id: str,
        update_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update a job's metadata.

        Args:
            job_id: Job ID
            update_data: Dictionary containing fields to update. Supported fields depend on job kind:

                For experiment jobs:
                    - name: Experiment name
                    - description: Experiment description
                    - tags: List of tags
                    - version: Version string
                    - logo: Logo URL
                    - ngc_path: NGC path
                    - encryption_key: Encryption key
                    - read_only: Boolean flag
                    - metric: Metric configuration
                    - public: Boolean for public visibility
                    - shared: Boolean for shared access
                    - authorized_party_nca_id: Authorized party ID
                    - docker_env_vars: Docker environment variables
                    - train_datasets: List of training dataset IDs
                    - eval_dataset: Evaluation dataset ID
                    - inference_dataset: Inference dataset ID
                    - calibration_dataset: Calibration dataset ID
                    - base_experiment_ids: List of base experiment IDs
                    - checkpoint_choose_method: Checkpoint selection method
                    - checkpoint_epoch_number: Checkpoint epoch number
                    - automl_settings: AutoML configuration
                    - tensorboard_enabled: Boolean for tensorboard

                For dataset jobs:
                    - tags: List of tags (only field allowed for dataset jobs per backend)

        Returns:
            Updated job metadata

        Raises:
            TaoValidationError: If update_data is empty or invalid
            TaoAPIError: If the update fails

        Note:
            The backend validates which fields can be updated based on job kind.
            Some fields like network_arch and experiment_params are immutable.
        """
        if not update_data or not isinstance(update_data, dict):
            raise TaoValidationError("update_data must be a non-empty dictionary")

        response = self._make_request("PATCH", f"jobs/{job_id}", data=update_data)
        return response.json()

    def delete_job(self, job_id: str) -> Dict[str, Any]:
        """Delete a job. Cancels the job if running and removes the job record.

        Args:
            job_id: Job ID

        Returns:
            Information about the deleted job
        """
        response = self._make_request("DELETE", f"jobs/{job_id}")
        return response.json()

    def pause_job(self, job_id: str) -> None:
        """Pause a running job.

        Args:
            job_id: Job ID
        """
        self._make_request("POST", f"jobs/{job_id}:pause")

    def resume_job(
        self,
        job_id: str,
        specs: Dict[str, Any],
        parent_job_id: Optional[str] = None,
    ) -> None:
        """Resume a paused job.

        Args:
            job_id: Job ID
            specs: Job specifications
            parent_job_id: Parent job ID (optional)
        """
        resume_req = create_job_resume_request(specs, parent_job_id)
        self._make_request("POST", f"jobs/{job_id}:resume", data=resume_req.to_dict())

    def retry_job(self, job_id: str) -> None:
        """Retry a failed job.

        Args:
            job_id: Job ID
        """
        self._make_request("POST", f"jobs/{job_id}:retry")

    # Duplicate _v2 methods removed - main methods are already v2-compliant

    def get_job_logs(self, job_id: str) -> str:
        """Get logs for a job.

        Args:
            job_id: Job ID

        Returns:
            Job logs as string
        """
        response = self._make_request("GET", f"jobs/{job_id}:logs")
        return response.text

    def list_job_files(
        self,
        job_id: str,
        retrieve_logs: bool = True,
        retrieve_specs: bool = True,
    ) -> Dict[str, Any]:
        """List files associated with a job.

        Args:
            job_id: Job ID
            retrieve_logs: Whether to include log files
            retrieve_specs: Whether to include spec files

        Returns:
            Dictionary containing file lists
        """
        params = {
            "retrieve_logs": retrieve_logs,
            "retrieve_specs": retrieve_specs,
        }

        response = self._make_request(
            "GET", f"jobs/{job_id}:list_files", params=params
        )
        return response.json()

    def download_job_files(
        self,
        job_id: str,
        workdir: str,
        file_lists: Optional[List[str]] = None,
        best_model: bool = False,
        latest_model: bool = False,
        tar_files: bool = True,
    ) -> str:
        """Download specific files from a job.

        Args:
            job_id: Job ID
            workdir: Local directory to download files to
            file_lists: List of specific files to download (optional)
            best_model: Whether to include best model file
            latest_model: Whether to include latest model file
            tar_files: Whether to compress files into tar format

        Returns:
            Path to downloaded file(s)
        """
        if file_lists is None:
            file_lists = []

        params = {
            "file_lists": file_lists,
            "best_model": best_model,
            "latest_model": latest_model,
            "tar_files": tar_files,
        }

        # Determine output filename
        temptar = f"{workdir}/{job_id}.tar.gz"
        if not tar_files and len(file_lists) == 1:
            temptar = os.path.join(workdir, job_id, file_lists[0])

        os.makedirs(os.path.dirname(temptar), exist_ok=True)

        response = self._make_request(
            "GET",
            f"jobs/{job_id}:download_selective_files",
            params=params,
            stream=True,
        )

        with open(temptar, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return temptar

    def download_entire_job(self, job_id: str, workdir: str) -> str:
        """Download all files from a job.

        Args:
            job_id: Job ID
            workdir: Local directory to download files to

        Returns:
            Path to downloaded tar file
        """
        temptar = f"{workdir}/{job_id}.tar.gz"
        os.makedirs(os.path.dirname(temptar), exist_ok=True)

        response = self._make_request(
            "GET", f"jobs/{job_id}:download", stream=True
        )

        with open(temptar, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return temptar

    # More duplicate _v2 methods removed - main methods are already v2-compliant

    # Model publishing methods
    def publish_model(
        self,
        job_id: str,
        display_name: str,
        description: str,
        team_name: str,
    ) -> Dict[str, Any]:
        """Publish a model to NGC registry.

        Args:
            job_id: Job ID
            display_name: Display name for the published model
            description: Description for the published model
            team_name: Team name within organization

        Returns:
            Publication response
        """
        publish_req = create_model_publish_request(display_name, description, team_name)
        response = self._make_request(
            "POST", f"jobs/{job_id}:publish_model", data=publish_req.to_dict()
        )
        return response.json()

    def remove_published_model(
        self,
        job_id: str,
        team_name: str,
    ) -> Dict[str, Any]:
        """Remove a published model from NGC registry.

        Args:
            job_id: Job ID
            team_name: Team name within organization

        Returns:
            Removal response
        """
        params = {"team_name": team_name}

        response = self._make_request(
            "DELETE",
            f"jobs/{job_id}:remove_published_model",
            params=params,
        )
        return response.json()

    # Final duplicate _v2 methods removed - main methods are already v2-compliant

    # Inference Microservices methods (new in v2)
    def start_inference_microservice(
        self,
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
    ) -> Dict[str, Any]:
        """Start an inference microservice (v2 API).

        Creates and starts a new inference microservice using the specified configuration.

        Args:
            docker_image: Docker image for inference (required)
            gpu_type: GPU type (required)
            num_gpus: Number of GPUs required (required)
            parent_job_id: Parent job ID (optional)
            kind: Job kind - "experiment" or "dataset" (optional)
            model_path: Path to the model (optional)
            workspace: Workspace ID (optional)
            docker_env_vars: Docker environment variables (optional)
            checkpoint_choose_method: Checkpoint selection method - "latest_model", "best_model", "from_epoch_number" (optional)
            checkpoint_epoch_number: Epoch number for checkpoint selection (optional)
            network_arch: Network architecture (optional)

        Returns:
            Inference microservice information including job ID
        """
        inference_req = create_inference_microservice_request(
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

        response = self._make_request("POST", "inference_microservices:start", data=inference_req.to_dict(), expected_status=(201,))
        return response.json()

    def inference_request(
        self,
        microservice_job_id: str,
        input: Optional[List[str]] = None,
        media: Optional[str] = None,
        model: Optional[str] = None,
        prompt: Optional[str] = None,
        enable_lora: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Make an inference request to a running inference microservice (v2 API).

        Args:
            microservice_job_id: Inference microservice job ID
            input: Base64-encoded images/videos with data URI format (optional)
            media: Cloud path to media file (e.g., aws://bucket/path/to/video.mp4) (optional)
            model: Model identifier (e.g. nvidia/nvdino-v2) (optional)
            prompt: Text prompt for VLM inference (optional)
            enable_lora: Enable LoRA for inference (optional)

        Returns:
            Inference results
        """
        inference_req = create_inference_request(
            input=input,
            media=media,
            model=model,
            prompt=prompt,
            enable_lora=enable_lora,
        )

        response = self._make_request("POST", f"inference_microservices/{microservice_job_id}:inference", data=inference_req.to_dict())
        return response.json()

    def get_inference_microservice_status(self, microservice_job_id: str) -> Dict[str, Any]:
        """Get inference microservice status (v2 API).

        Args:
            microservice_job_id: Inference microservice job ID

        Returns:
            Inference microservice status
        """
        response = self._make_request("GET", f"inference_microservices/{microservice_job_id}:status")
        return response.json()

    def stop_inference_microservice(self, microservice_job_id: str) -> Dict[str, Any]:
        """Stop an inference microservice (v2 API).

        Args:
            microservice_job_id: Inference microservice job ID

        Returns:
            Stop response
        """
        response = self._make_request("DELETE", f"inference_microservices/{microservice_job_id}:stop")
        return response.json()

    # Air-gapped model loading (updated endpoint in v2)
    def load_airgapped_model(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """Load an air-gapped model.

        Args:
            model_data: Model loading configuration

        Returns:
            Model loading response
        """
        load_req = create_model_load_request(model_data)
        response = self._make_request("POST", "jobs:load_airgapped", data=load_req.to_dict())
        return response.json()
