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

"""TAO-Client base actions module"""

import json
import os
import time

from tao_sdk.client import TaoClient

timeout = 3600 * 24


class Actions:
    """Base class which defines API functions for general actions using TaoClient SDK"""

    def __init__(self):
        """Initialize the actions base class with TaoClient SDK"""

        # Initialize TaoClient SDK - it will load saved credentials from environment variables
        self.client = TaoClient()

        # Keep these for backward compatibility during transition
        self.org_name = self.client.org_name
        self.token = self.client.token
        self.base_url = self.client.base_url
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _get_json_headers(self):
        """Get headers with Content-Type for JSON requests as required by v2 API"""
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        return headers

    # Authentication methods
    def login(self, ngc_key, ngc_org_name, enable_telemetry=None, tao_base_url=None):
        """Login to TAO API and save credentials"""
        return self.client.login(ngc_key, ngc_org_name, enable_telemetry, tao_base_url)

    def is_authenticated(self):
        """Check if client has valid authentication credentials"""
        return self.client.is_authenticated()

    def logout(self):
        """Clear saved authentication credentials from config file"""
        # Use the SDK logout method which clears the config file
        result = self.client.logout()

        # Clear current instance credentials for backward compatibility
        self.token = "invalid"
        self.headers = {"Authorization": "Bearer invalid"}

        return result

    # Workspace specific actions
    def create_workspace(self, name, cloud_type, cloud_details):
        """Create a workspace and return the id"""
        # Check authentication before API call
        self.client.require_authentication()

        cloud_details_dict = json.loads(cloud_details) if cloud_details else None
        result = self.client.create_workspace(
            name=name,
            cloud_type=cloud_type,
            cloud_specific_details=cloud_details_dict
        )
        return result


    # Backup a workspace
    def backup_workspace(self, backup_file_name, workspace):
        """Backup a workspace"""
        return self.client.backup_workspace(workspace, backup_file_name)


    # Restore a workspace
    def restore_workspace(self, backup_file_name, workspace):
        """Restore a workspace"""
        return self.client.restore_workspace(workspace, backup_file_name)

    # Delete a workspace
    def delete_workspace(self, workspace_id):
        """Delete a workspace (v2 unified endpoint)"""
        return self.client.delete_workspace(workspace_id)

    def list_workspaces(self, filter_params=None):
        """List workspaces using the v2 endpoint"""
        return self.client.list_workspaces(filter_params)


    # Dataset specific actions
    def create_dataset(
        self, dataset_type, dataset_format, workspace, cloud_file_path, url, use_for
    ):
        """Create a dataset and return the id"""
        use_for_list = json.loads(use_for) if use_for else None
        result = self.client.create_dataset(
            dataset_type=dataset_type,
            dataset_format=dataset_format,
            workspace_id=workspace,
            cloud_file_path=cloud_file_path,
            url=url,
            use_for=use_for_list
        )
        return result

    # Experiment specific actions

    def list_base_experiments(self, params=""):
        """List the available base experiments (v2 unified endpoint)"""
        filter_params = json.loads(params) if isinstance(params, str) and params else {}
        return self.client.list_base_experiments(filter_params)

    def list_datasets(self, filter_params=None):
        """List datasets using v2 unified endpoint"""
        if isinstance(filter_params, str) and filter_params:
            filter_params = json.loads(filter_params)
        return self.client.list_datasets(filter_params)

    def update_dataset(self, dataset_id, update_data):
        """Update a dataset's metadata (v2 unified endpoint)"""
        # Parse JSON string if needed
        if isinstance(update_data, str):
            update_data = json.loads(update_data)

        return self.client.update_dataset_metadata(
            dataset_id=dataset_id,
            update_info=update_data
        )

    def delete_dataset(self, dataset_id):
        """Delete a dataset using v2 unified endpoint"""
        self.client.delete_dataset(dataset_id)
        return {"message": "Dataset deleted successfully"}


    def get_dataset_metadata(self, dataset_id):
        """Get metadata of a dataset (v2 unified endpoint)"""
        return self.client.get_dataset_metadata(dataset_id)

    def get_workspace_metadata(self, workspace_id):
        """Get metadata of a workspace (v2 unified endpoint)"""
        return self.client.get_workspace_metadata(workspace_id)

    def get_job_metadata(self, job_id):
        """Get metadata of a job (v2 unified endpoint)"""
        return self.client.get_job_metadata(job_id)

    def get_job_schema(self, action, network_arch=None, base_experiment_id=None, dataset_id=None):
        """Return schema dictionary for the job action (v2 unified endpoint)"""
        return self.client.get_job_schema(
            action=action,
            network_arch=network_arch,
            base_experiment_id=base_experiment_id,
            job_id=dataset_id  # dataset_id maps to job_id for dataset jobs
        )

    def get_automl_defaults(self, base_experiment_id, network_arch, action):
        """Return automl parameters enabled for a network (v2 unified endpoint)"""
        return self.client.get_automl_defaults(base_experiment_id, network_arch, action)

    def get_automl_param_details(self, network_arch, parameters):
        """Get AutoML parameter details for specific parameters"""
        return self.client.get_automl_param_details(network_arch, parameters)

    def get_job_status(self, job_id):
        """Get status for a job (v2 unified endpoint)"""
        return self.client.get_job_metadata(job_id)

    def publish_model(
        self, job_id, display_name, description, team_name
    ):
        """Publish model to ngc registry (v2 unified endpoint)"""
        return self.client.publish_model(job_id, display_name, description, team_name)

    def remove_published_model(self, job_id, team_name):
        """Remove published model from ngc registry (v2 unified endpoint)"""
        return self.client.remove_published_model(job_id, team_name)

    def create_job(self, kind, action, specs, name=None, network_arch=None, encryption_key=None,
                   workspace=None, dataset_id=None, parent_job_id=None, platform_id=None,
                   description=None, tags=None, base_experiment_ids=None, automl_settings=None,
                   train_datasets=None, eval_dataset=None, inference_dataset=None, calibration_dataset=None, docker_env_vars=None):
        """Create a unified job (experiment or dataset) and return the id"""
        # Helper function to safely parse JSON strings
        def safe_json_parse(value):
            if not value or not isinstance(value, str):
                return None
            value = value.strip()
            if not value or value.lower() == 'null':
                return None
            try:
                return json.loads(value)
            except (json.JSONDecodeError, ValueError):
                return None

        # Parse JSON strings if needed
        parsed_specs = json.loads(specs) if isinstance(specs, str) else specs
        parsed_tags = safe_json_parse(tags)
        parsed_base_experiment_ids = safe_json_parse(base_experiment_ids)
        parsed_automl_settings = safe_json_parse(automl_settings)
        parsed_train_datasets = safe_json_parse(train_datasets)
        parsed_docker_env_vars = json.loads(docker_env_vars) if isinstance(docker_env_vars, str) and docker_env_vars else None
        # Prepare arguments for SDK create_job method
        job_kwargs = {
            "kind": kind,
            "action": action,
            "specs": parsed_specs,
            "parent_job_id": parent_job_id,
            "platform_id": platform_id,
            "tags": parsed_tags,
        }

        if kind == "experiment":
            # Add experiment-specific fields
            job_kwargs.update({
                "name": name,
                "network_arch": network_arch,
                "encryption_key": encryption_key,
                "workspace": workspace,
                "docker_env_vars": parsed_docker_env_vars,
                "description": description,
                "base_experiment_ids": parsed_base_experiment_ids,
                "train_datasets": parsed_train_datasets,
                "eval_dataset": eval_dataset,
                "inference_dataset": inference_dataset,
                "calibration_dataset": calibration_dataset,
            })
            # Add AutoML config if provided
            if parsed_automl_settings:
                job_kwargs["automl_settings"] = parsed_automl_settings
        elif kind == "dataset":
            # Add dataset-specific fields
            job_kwargs["dataset_id"] = dataset_id
        else:
            raise ValueError(f"Invalid job kind: {kind}. Must be 'experiment' or 'dataset'")

        # Use SDK unified create_job method
        result = self.client.create_job(**job_kwargs)
        return result

    # Backward compatibility methods - delegate to unified create_job
    def run_experiment_job(self, name, network_arch, encryption_key, workspace, action, specs,
                          parent_job_id=None, platform_id=None, description=None, tags=None,
                          base_experiment_ids=None, automl_settings=None):
        """Create an experiment job and return the id (backward compatibility - use create_job instead)"""
        return self.create_job(
            kind="experiment",
            action=action,
            specs=specs,
            name=name,
            network_arch=network_arch,
            encryption_key=encryption_key,
            workspace=workspace,
            parent_job_id=parent_job_id,
            platform_id=platform_id,
            description=description,
            tags=tags,
            base_experiment_ids=base_experiment_ids,
            automl_settings=automl_settings,
        )

    def run_dataset_job(self, dataset_id, action, specs, parent_job_id=None, platform_id=None, tags=None):
        """Create a dataset job and return the id (backward compatibility - use create_job instead)"""
        return self.create_job(
            kind="dataset",
            action=action,
            specs=specs,
            dataset_id=dataset_id,
            parent_job_id=parent_job_id,
            platform_id=platform_id,
            tags=tags,
        )

    def cancel_job(self, job_id):
        """Cancel a running job (v2 unified endpoint)"""
        return self.client.cancel_job(job_id)

    def update_job(self, job_id, update_data):
        """Update a job's metadata (v2 unified endpoint)"""
        # Parse JSON string if needed
        if isinstance(update_data, str):
            update_data = json.loads(update_data)

        return self.client.update_job(
            job_id=job_id,
            update_data=update_data
        )

    def delete_job(self, job_id):
        """Delete a job (v2 unified endpoint)"""
        return self.client.delete_job(job_id)

    def pause_job(self, job_id):
        """Pause a running job (v2 unified endpoint)"""
        return self.client.pause_job(job_id)

    def resume_job(self, job_id, parent_job_id, specs):
        """Resume a paused job (v2 unified endpoint)"""
        specs_dict = json.loads(specs) if isinstance(specs, str) else specs
        return self.client.resume_job(job_id, specs_dict, parent_job_id)

    def list_jobs(self, filter_params=None):
        """List jobs using the unified v2 endpoint"""
        return self.client.list_jobs(filter_params)

    def list_job_files(self, job_id, retrieve_logs, retrieve_specs):
        """List files of a job (v2 unified endpoint)"""
        return self.client.list_job_files(job_id, retrieve_logs, retrieve_specs)

    def download_job_files(
        self,
        job_id,
        workdir,
        file_lists=None,
        best_model=False,
        latest_model=False,
        tar_files=True,
    ):
        """Download a job with the files passed (v2 unified endpoint)"""
        if file_lists is None:
            file_lists = []
        return self.client.download_job_files(
            job_id, workdir, file_lists, best_model, latest_model, tar_files
        )

    def download_entire_job(self, job_id, workdir):
        """Download a job (v2 unified endpoint)"""
        return self.client.download_entire_job(job_id, workdir)

    def get_job_logs(self, job_id):
        """Return logs of a running job (v2 unified endpoint)"""
        from tao_sdk.exceptions import TaoAPIError
        try:
            logs = self.client.get_job_logs(job_id)
            if "Logs for the job are not available yet" in logs:
                print("Logs for the job are not available yet")
                return
            print(logs, end='')
        except TaoAPIError as e:
            # Handle case when logs are not available yet
            if "Logs for the job are not available yet" in str(e):
                print("Logs for the job are not available yet")
                return
            # Re-raise if it's a different error
            raise

    # Inference Microservice methods (v2 API)
    def start_inference_microservice(
        self,
        docker_image,
        gpu_type,
        num_gpus,
        parent_job_id=None,
        kind=None,
        model_path=None,
        workspace=None,
        docker_env_vars=None,
        checkpoint_choose_method=None,
        checkpoint_epoch_number=None,
        network_arch=None,
    ):
        """Start an inference microservice"""
        # Parse JSON strings if needed
        parsed_docker_env_vars = json.loads(docker_env_vars) if isinstance(docker_env_vars, str) and docker_env_vars else None
        parsed_checkpoint_epoch_number = json.loads(checkpoint_epoch_number) if isinstance(checkpoint_epoch_number, str) and checkpoint_epoch_number else None

        return self.client.start_inference_microservice(
            docker_image=docker_image,
            gpu_type=gpu_type,
            num_gpus=int(num_gpus),
            parent_job_id=parent_job_id,
            kind=kind,
            model_path=model_path,
            workspace=workspace,
            docker_env_vars=parsed_docker_env_vars,
            checkpoint_choose_method=checkpoint_choose_method,
            checkpoint_epoch_number=parsed_checkpoint_epoch_number,
            network_arch=network_arch,
        )

    def inference_request(
        self,
        microservice_job_id,
        input=None,
        media=None,
        model=None,
        prompt=None,
        enable_lora=None,
    ):
        """Make an inference request to a running microservice"""
        # Parse JSON strings if needed
        parsed_input = json.loads(input) if isinstance(input, str) and input else None
        parsed_enable_lora = json.loads(enable_lora.lower()) if isinstance(enable_lora, str) and enable_lora else None

        return self.client.inference_request(
            microservice_job_id=microservice_job_id,
            input=parsed_input,
            media=media,
            model=model,
            prompt=prompt,
            enable_lora=parsed_enable_lora,
        )

    def get_inference_microservice_status(self, microservice_job_id):
        """Get inference microservice status"""
        return self.client.get_inference_microservice_status(microservice_job_id)

    def stop_inference_microservice(self, microservice_job_id):
        """Stop an inference microservice"""
        return self.client.stop_inference_microservice(microservice_job_id)
