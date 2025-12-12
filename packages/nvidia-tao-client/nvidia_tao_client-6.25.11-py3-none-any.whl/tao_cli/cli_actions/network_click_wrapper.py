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

"""TAO-Client wrapper to add networks to the click CLI support"""

import click
import json
import ast

from tao_cli.cli_actions.actions import Actions
from nvidia_tao_core.microservices.enum_constants import _get_valid_config_json_param_for_network, ExperimentNetworkArch


# Import OrderedGroup to preserve command order in network groups
class OrderedGroup(click.Group):
    """Custom Click group that preserves command order instead of sorting alphabetically"""

    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name, commands, **attrs)
        self.commands_in_order = []

    def add_command(self, cmd, name=None):
        """Add command and track order"""
        result = super().add_command(cmd, name)
        command_name = name or cmd.name
        if command_name not in self.commands_in_order:
            self.commands_in_order.append(command_name)
        return result

    def list_commands(self, ctx):
        """Return commands in the order they were added, not alphabetically"""
        return self.commands_in_order

click_obj = Actions()


def create_click_group(group_name, help_text):
    """Wrapper class to create click groups for DNN networks"""

    @click.group(name=group_name, help=help_text, cls=OrderedGroup)
    def wrapper():
        f"""Create {group_name} click group"""
        pass


    # ===============================================================================
    # WORKSPACE-RELATED COMMANDS (use /workspaces API endpoints)
    # ===============================================================================

    @wrapper.command(name="----- WORKSPACES ------")
    def workspaces_separator():
        """ """
        click.echo("This section contains workspace-related commands.")

    @wrapper.command()
    @click.option("--name", prompt="name", help="Name of the workspace", required=True)
    @click.option(
        "--cloud-type",
        prompt="cloud_type",
        help="Cloud storage type.",
        required=True,
        default=None,
        type=click.Choice(["aws", "huggingface", "azure"]),
    )
    @click.option(
        "--cloud-specific-details", help="Cloud-specific storage details.", required=True, default=None
    )
    def create_workspace(name, cloud_type, cloud_specific_details):
        """Create a workspace and return the id"""
        id = click_obj.create_workspace(name, cloud_type, cloud_specific_details)
        click.echo(f"{id}")

    @wrapper.command(name="list-workspaces")
    @click.option("--cloud-type", help="Filter by cloud type", type=click.Choice(["aws", "azure", "gcp"]))
    @click.option("--name", help="Filter by workspace name")
    @click.option("--format", "output_format", help="Output format", type=click.Choice(["json", "table"]), default="table")
    def list_workspaces(cloud_type, name, output_format):
        """List workspaces"""
        filter_params = {}
        if cloud_type:
            filter_params["cloud_type"] = cloud_type
        if name:
            filter_params["name"] = name

        workspaces = click_obj.list_workspaces(filter_params)

        if output_format == "json":
            click.echo(json.dumps(workspaces, indent=2))
        else:
            # Table format
            if not workspaces:
                click.echo("No workspaces found.")
                return

            # Display workspaces in a table-like format
            click.echo(f"{'ID':<36} {'Name':<30} {'Cloud Type':<15} {'Status':<15} {'Created At':<20}")
            click.echo("-" * 120)
            for workspace in workspaces:
                workspace_id = workspace.get("id", "N/A")[:35]
                workspace_name = workspace.get("name", "N/A")[:29]
                cloud_type = workspace.get("cloud_type", "N/A")
                status = workspace.get("status", "N/A")
                created_at = workspace.get("created_date", "N/A")[:19]  # Truncate timestamp

                click.echo(f"{workspace_id:<36} {workspace_name:<30} {cloud_type:<15} {status:<15} {created_at:<20}")

    @wrapper.command(name="delete-workspace")
    @click.option("--workspace-id", required=True, help="Workspace ID to delete")
    @click.option("--confirm", is_flag=True, help="Confirm deletion without prompting")
    def delete_workspace(workspace_id, confirm):
        """Delete a workspace (cancels all related jobs and removes workspace)"""
        if not confirm:
            if not click.confirm(f"Are you sure you want to delete workspace {workspace_id}? This will cancel all related jobs and cannot be undone."):
                click.echo("Workspace deletion cancelled.")
                return

        result = click_obj.delete_workspace(workspace_id)
        click.echo(f"Workspace {workspace_id} deleted successfully.")
        if result:
            click.echo(f"Details: {json.dumps(result, indent=2)}")

    @wrapper.command(name="get-workspace-metadata")
    @click.option("--workspace-id", required=True, help="Workspace ID")
    def get_workspace_metadata(workspace_id):
        """Get workspace metadata"""
        metadata = click_obj.get_workspace_metadata(workspace_id)
        click.echo(json.dumps(metadata, indent=2))

    @wrapper.command()
    @click.option("--backup-file-name", prompt="backup_file_name", help="Name of the workspace", default="mongodb_backup.gz")
    @click.option(
        "--workspace-id",
        prompt="workspace_id",
        help="Workspace ID.",
        required=True,
        default=None,
    )
    def backup_workspace(backup_file_name, workspace_id):
        """Backup mongo database to a mongodump file on workspace"""
        response = click_obj.backup_workspace(backup_file_name, workspace_id)
        click.echo(response)

    @wrapper.command()
    @click.option("--backup-file-name", prompt="backup_file_name", help="Name of the workspace", default="mongodb_backup.gz")
    @click.option(
        "--workspace-id",
        prompt="workspace_id",
        help="Workspace ID.",
        required=True,
        default=None,
    )
    def restore_workspace(backup_file_name, workspace):
        """Restore a workspace from a mongodump file"""
        response = click_obj.restore_workspace(backup_file_name, workspace)
        click.echo(response)


    # ===============================================================================
    # DATASET-RELATED COMMANDS (use /datasets API endpoints)
    # ===============================================================================

    @wrapper.command(name="------ DATASETS ------")
    def datasets_separator():
        """ """
        click.echo("This section contains dataset-related commands.")

    @wrapper.command()
    @click.option(
        "--dataset-type",
        prompt="dataset_type",
        type=click.Choice(_get_valid_config_json_param_for_network(group_name, "dataset_type")),
        help="The dataset type.",
        required=True,
    )
    @click.option(
        "--dataset-format",
        prompt="dataset_format",
        type=click.Choice(_get_valid_config_json_param_for_network(group_name, "formats")),
        help="The dataset format.",
        required=True,
    )
    @click.option("--workspace-id", help="Workspace ID.", required=False, default=None)
    @click.option(
        "--cloud-file-path",
        help="Path to dataset within cloud storage",
        required=False,
        default=None,
    )
    @click.option("--url", help="Public dataset url", required=False, default=None)
    @click.option(
        "--use-for",
        help="Is the dataset used for training/evaluation/testing",
        required=False,
    )
    def create_dataset(
        dataset_type, dataset_format, workspace_id, cloud_file_path, url, use_for
    ):
        """Create a dataset and return the id"""
        id = click_obj.create_dataset(
            dataset_type, dataset_format, workspace_id, cloud_file_path, url, use_for
        )
        click.echo(f"{id}")

    @wrapper.command()
    @click.option("--filter-params", help="filter_params")
    def list_datasets(filter_params):
        """Return the list of datasets"""
        datasets = click_obj.list_datasets(filter_params)
        click.echo(json.dumps(datasets, indent=2))

    @wrapper.command()
    @click.option("--dataset-id", prompt="dataset_id", help="Dataset ID", required=True)
    def delete_dataset(dataset_id):
        """Delete a dataset"""
        result = click_obj.delete_dataset(dataset_id)
        click.echo(f"Dataset {dataset_id} deleted successfully.")
        if result:
            click.echo(f"Details: {json.dumps(result, indent=2)}")

    @wrapper.command(name="update-dataset")
    @click.option("--dataset-id", required=True, help="Dataset ID to update")
    @click.option("--update-data", required=True, help="Update data as JSON dictionary")
    def update_dataset(dataset_id, update_data):
        """Update a dataset's metadata

        Examples:

        Update name and description:
        --update-data '{"name": "New Dataset Name", "description": "Updated description"}'

        Update multiple fields:
        --update-data '{"name": "Dataset v2", "version": "2.0", "tags": ["production"]}'

        Update cloud file path (triggers re-pull):
        --update-data '{"cloud_file_path": "s3://bucket/new-path/dataset"}'

        Update docker environment variables:
        --update-data '{"docker_env_vars": {"ENV_VAR": "value"}}'

        Note: Fields 'type' and 'format' are immutable and cannot be changed.
        """
        try:
            result = click_obj.update_dataset(
                dataset_id=dataset_id,
                update_data=update_data
            )
            click.echo(f"Dataset {dataset_id} updated successfully.")
            click.echo(json.dumps(result, indent=2))
        except Exception as e:
            click.echo(f"Error updating dataset: {str(e)}")
            raise

    @wrapper.command(name="get-dataset-metadata")
    @click.option("--dataset-id", required=True, help="Dataset ID")
    def get_dataset_metadata(dataset_id):
        """Get dataset metadata"""
        metadata = click_obj.get_dataset_metadata(dataset_id)
        click.echo(json.dumps(metadata, indent=2))


    # ===============================================================================
    # JOB-RELATED COMMANDS (use /jobs API endpoints)
    # ===============================================================================

    @wrapper.command(name="-------- JOBS --------")
    def jobs_separator():
        """ """
        click.echo("This section contains job-related commands.")

    @wrapper.command(name="create-job")
    @click.option(
        "--kind",
        required=True,
        type=click.Choice(["experiment", "dataset"]),
        help="Job kind (experiment or dataset)"
    )
    @click.option("--name", help="Job/Experiment name (required for experiments)")
    @click.option("--encryption-key", help="Encryption key (required for experiments)")
    @click.option("--workspace-id", help="Workspace ID (required for experiments)")
    @click.option("--dataset-id", help="Dataset ID (required for datasets)")
    @click.option(
        "--action",
        required=True,
        type=click.Choice(_get_valid_config_json_param_for_network(group_name, "actions")),
        help="Action to perform"
    )
    @click.option("--specs", required=True, help="Action specifications (JSON)")
    @click.option("--description", help="Job description (optional)")
    @click.option("--tags", help="Tags as JSON array (optional)")
    @click.option("--base-experiment-ids", help="Base experiment IDs as JSON array (optional)")
    @click.option("--parent-job-id", help="Parent job ID (optional)")
    @click.option("--platform-id", help="Platform ID for NVCF backend (optional)")
    @click.option("--automl-settings", help="AutoML configuration (JSON, optional)")
    @click.option("--train-datasets", help="Training dataset IDs as JSON array (optional)")
    @click.option("--eval-dataset", help="Evaluation dataset ID (optional)")
    @click.option("--inference-dataset", help="Inference dataset ID (optional)")
    @click.option("--calibration-dataset", help="Calibration dataset ID (optional)")
    @click.option("--docker-env-vars", help="Docker environment variables as JSON string (optional)")
    def create_job(kind, name, encryption_key, workspace_id, dataset_id, action, specs,
                   description, tags, base_experiment_ids, parent_job_id, platform_id,
                   automl_settings, train_datasets, eval_dataset, inference_dataset, calibration_dataset, docker_env_vars):
        """Create a unified job (experiment or dataset)"""
        # Use the unified create_job method
        job_id = click_obj.create_job(
            kind=kind,
            action=action,
            specs=specs,
            name=name,
            network_arch=group_name.replace('-', '_') if kind == "experiment" else None,
            encryption_key=encryption_key,
            workspace=workspace_id,
            dataset_id=dataset_id,
            parent_job_id=parent_job_id,
            platform_id=platform_id,
            description=description,
            tags=tags,
            base_experiment_ids=base_experiment_ids,
            automl_settings=automl_settings,
            train_datasets=train_datasets,
            eval_dataset=eval_dataset,
            inference_dataset=inference_dataset,
            calibration_dataset=calibration_dataset,
            docker_env_vars=docker_env_vars
        )
        click.echo(f"{job_id}")


    @wrapper.command(name="list-jobs")
    @click.option("--kind", help="Filter by job type (experiment/dataset)", type=click.Choice(["experiment", "dataset"]))
    @click.option("--status", help="Filter by job status")
    @click.option("--action", help="Filter by action type")
    @click.option("--all-networks", is_flag=True, help="Show jobs from all network architectures (default: only current network)")
    @click.option("--format", "output_format", help="Output format", type=click.Choice(["json", "table"]), default="table")
    def list_jobs(kind, status, action, all_networks, output_format):
        """List jobs"""
        filter_params = {}
        if kind:
            filter_params["kind"] = kind
        if status:
            filter_params["status"] = status
        if action:
            filter_params["action"] = action

        # By default, filter by the current network architecture unless --all-networks is specified
        if not all_networks:
            filter_params["network_arch"] = group_name.replace('-', '_')
        jobs = click_obj.list_jobs(filter_params)

        if output_format == "json":
            click.echo(json.dumps(jobs, indent=2))
        else:
            # Table format
            if not jobs:
                click.echo("No jobs found.")
                return

            # Display jobs in a table-like format
            click.echo(f"{'ID':<36} {'Kind':<10} {'Status':<15} {'Action':<15} {'Name/Dataset ID':<30}")
            click.echo("-" * 110)
            for job in jobs:
                job_id = job.get("id", "N/A")[:35]
                job_kind = job.get("kind", "N/A")
                job_status = job.get("status", "N/A")
                job_action = job.get("action", "N/A")

                # Get name for experiments or dataset_id for datasets
                if job_kind == "experiment":
                    name_or_id = job.get("name", "N/A")
                else:
                    name_or_id = job.get("dataset_id", "N/A")

                click.echo(f"{job_id:<36} {job_kind:<10} {job_status:<15} {job_action:<15} {name_or_id[:29]:<30}")

    @wrapper.command(name="delete-job")
    @click.option("--job-id", required=True, help="Job ID to delete")
    @click.option("--confirm", is_flag=True, help="Confirm deletion without prompting")
    def delete_job(job_id, confirm):
        """Delete a job (cancels if running and removes job record)"""
        if not confirm:
            if not click.confirm(f"Are you sure you want to delete job {job_id}? This action cannot be undone."):
                click.echo("Job deletion cancelled.")
                return

        result = click_obj.delete_job(job_id)
        click.echo(f"Job {job_id} deleted successfully.")
        if result:
            click.echo(f"Details: {json.dumps(result, indent=2)}")

    @wrapper.command(name="update-job")
    @click.option("--job-id", required=True, help="Job ID to update")
    @click.option("--update-data", required=True, help="Update data as JSON dictionary (e.g., '{\"tags\": [\"tag1\"], \"description\": \"New desc\"}')")
    def update_job(job_id, update_data):
        """Update a job's metadata

        Examples:

        Update tags only:
        --update-data '{"tags": ["production", "v2"]}'

        Update multiple fields:
        --update-data '{"name": "New Name", "description": "Updated description", "tags": ["tag1"]}'

        Update experiment datasets:
        --update-data '{"train_datasets": ["dataset-id-1", "dataset-id-2"], "eval_dataset": "dataset-id-3"}'

        Enable AutoML:
        --update-data '{"automl_settings": {"automl_enabled": true, "automl_max_recommendations": 10}}'

        Note: Supported fields depend on job kind (experiment vs dataset).
        Dataset jobs can only update tags. Experiment jobs support many more fields.
        """
        try:
            result = click_obj.update_job(
                job_id=job_id,
                update_data=update_data
            )
            click.echo(json.dumps(result, indent=2))
        except Exception as e:
            click.echo(f"Error updating job: {str(e)}")
            raise

    @wrapper.command(name="get-job-status")
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    def get_job_status(job_id):
        """Get job status"""
        data = click_obj.get_job_status(job_id)
        click.echo(json.dumps(data, indent=2))

    @wrapper.command(name="get-job-metadata")
    @click.option("--job-id", required=True, help="Job ID")
    def get_job_metadata(job_id):
        """Get job metadata"""
        metadata = click_obj.get_job_metadata(job_id)
        click.echo(json.dumps(metadata, indent=2))

    @wrapper.command(name="get-job-schema")
    @click.option("--action", prompt="action", help="Job Action", required=True, type=click.Choice(_get_valid_config_json_param_for_network(group_name, "actions")))
    @click.option("--base-experiment-id", help="Base Experiment ID (for experiment jobs)", required=False)
    @click.option("--network-arch", help="Network architecture (defaults to current network if not provided)", required=False, type=click.Choice(ExperimentNetworkArch))
    @click.option("--dataset-id", help="Dataset ID (for dataset jobs)", required=False)
    def get_job_schema(action, network_arch, base_experiment_id, dataset_id):
        """Return default schema of a job action"""
        # Default to current network if network_arch not provided
        if not network_arch and not base_experiment_id and not dataset_id:
            network_arch = group_name
        data = click_obj.get_job_schema(action, network_arch, base_experiment_id, dataset_id)
        click.echo(json.dumps(data, indent=2))

    @wrapper.command(name="get-gpu-types")
    def get_gpu_types():
        """Get available GPU types"""
        gpu_types = click_obj.client.get_gpu_types()
        click.echo(json.dumps(gpu_types, indent=2))

    @wrapper.command(name="get-job-logs")
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    def get_job_logs(job_id):
        """Get the logs of a job"""
        click_obj.get_job_logs(job_id)

    @wrapper.command(name="list-job-files")
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    @click.option(
        "--retrieve-logs",
        prompt="retrieve_logs",
        help="To list log files of the jobs",
        required=True,
        type=bool,
    )
    @click.option(
        "--retrieve-specs",
        prompt="retrieve_specs",
        help="To list spec files of the jobs",
        required=True,
        type=bool,
    )
    def list_job_files(job_id, retrieve_logs, retrieve_specs):
        """List the files, specs and logs of a job"""
        file_list = click_obj.list_job_files(
            job_id, bool(retrieve_logs), bool(retrieve_specs)
        )
        click.echo(f"{json.dumps(file_list, indent=2)}")

    @wrapper.command(name="download-job-files")
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    @click.option(
        "--workdir",
        prompt="workdir",
        help="Local path to download the files onto",
        required=True,
    )
    @click.option(
        "--files",
        prompt="files",
        help="List of files to be downloaded from the list_job_files output",
        required=True,
    )
    @click.option(
        "--best-model",
        prompt="best_model",
        help="To add best model in terms of accuracy to the download list",
        required=True,
        type=bool,
    )
    @click.option(
        "--latest-model",
        prompt="latest_model",
        help="To add latest model in terms of accuracy to the download list",
        required=True,
        type=bool,
    )
    @click.option(
        "--tar-files",
        prompt="tar_files",
        help="If the downloaded file should be tar file or not - no need for tars for single file download",
        required=True,
        type=bool,
    )
    def download_job_files(
        job_id, workdir, files, best_model, latest_model, tar_files
    ):
        """Download job files based on the arguments passed"""
        files = ast.literal_eval(files)
        download_path = click_obj.download_job_files(
            job_id, workdir, files, best_model, latest_model, tar_files
        )
        click.echo(download_path)

    @wrapper.command()
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    @click.option(
        "--workdir",
        prompt="workdir",
        help="Local path to download the files onto",
        required=True,
    )
    def download_entire_job(job_id, workdir):
        """Download all files w.r.t to the job"""
        download_path = click_obj.download_entire_job(job_id, workdir)
        click.echo(download_path)

    @wrapper.command()
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    def pause_job(job_id):
        """Pause a running job, train only"""
        click_obj.pause_job(job_id)
        click.echo(f"{job_id}")

    @wrapper.command()
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    def cancel_job(job_id):
        """Cancel a running job"""
        click_obj.cancel_job(job_id)
        click.echo(f"{job_id}")

    @wrapper.command()
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    @click.option("--parent_job_id", help="Parent job.", required=False, default=None)
    @click.option("--specs", prompt="specs", help="specs", required=True)
    def resume_job(job_id, parent_job_id, specs):
        """Resume a paused job"""
        click_obj.resume_job(job_id, parent_job_id, specs)
        click.echo(f"{job_id}")

    @wrapper.command()
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    @click.option(
        "--display-name",
        prompt="display_name",
        help="Display name for model to be published.",
        required=True,
    )
    @click.option(
        "--description",
        prompt="description",
        help="Description for model to be published",
        required=True,
    )
    @click.option("--team", prompt="team", help="team name within org", required=True)
    def publish_model(job_id, display_name, description, team):
        """Publish model"""
        data = click_obj.publish_model(
            job_id, display_name, description, team
        )
        click.echo(f"{data}")

    @wrapper.command()
    @click.option("--job-id", prompt="job_id", help="Job ID", required=True)
    @click.option("--team", prompt="team", help="team name within org", required=True)
    def remove_published_model(job_id, team):
        """Remove published model"""
        data = click_obj.remove_published_model(job_id, team)
        click.echo(f"{data}")

    @wrapper.command(name="get-automl-defaults")
    @click.option("--base-experiment-id", help="Base Experiment ID (for experiment jobs)", required=False)
    @click.option("--network-arch", help="Network architecture (defaults to current network if not provided)", required=False, type=click.Choice(ExperimentNetworkArch))
    @click.option("--action", help="Job Action", required=False, type=click.Choice(_get_valid_config_json_param_for_network(group_name, "actions")))
    def get_automl_defaults(base_experiment_id, network_arch, action):
        """Return default automl parameters"""
        if not network_arch and not base_experiment_id:
            network_arch=group_name.replace('-', '_')
        data = click_obj.get_automl_defaults(base_experiment_id, network_arch, action)
        click.echo(json.dumps(data, indent=2))

    @wrapper.command(name="get-automl-param-details")
    @click.option("--network-arch", help="Network architecture", required=False, type=click.Choice(ExperimentNetworkArch))
    @click.option("--parameters", help="Comma-separated parameter names (e.g., train.optm_decay_type,train.epoch)", required=True)
    def get_automl_param_details(network_arch, parameters):
        """Get AutoML parameter details for specific parameters"""
        if not network_arch:
            network_arch = group_name.replace('-', '_')
        data = click_obj.get_automl_param_details(network_arch, parameters)
        click.echo(json.dumps(data, indent=2))

    @wrapper.command()
    @click.option("--filter-params", help="filter_params")
    def list_base_experiments(filter_params):
        """Return the list of base experiments"""
        artifacts = click_obj.list_base_experiments(filter_params)
        click.echo(json.dumps(artifacts, indent=2))


    # ===============================================================================
    # INFERENCE MICROSERVICE-RELATED COMMANDS (use /inference_microservices API endpoints)
    # ===============================================================================

    @wrapper.command(name="---- INFERENCE MS ----")
    def inference_microservice_separator():
        """INFERENCE MICROSERVICE COMMANDS"""
        pass

    @wrapper.command(name="start-inference-microservice")
    @click.option("--docker-image", required=True, help="Docker image for inference")
    @click.option("--gpu-type", required=True, help="GPU type (e.g., h100, a100)")
    @click.option("--num-gpus", required=True, type=int, help="Number of GPUs required")
    @click.option("--parent-job-id", help="Parent job ID (optional)")
    @click.option("--kind", type=click.Choice(["experiment", "dataset"]), help="Job kind (optional)")
    @click.option("--model-path", help="Path to the model (optional)")
    @click.option("--workspace-id", help="Workspace ID (optional)")
    @click.option("--docker-env-vars", help="Docker environment variables as JSON string (optional)")
    @click.option("--checkpoint-choose-method", type=click.Choice(["latest_model", "best_model", "from_epoch_number"]), help="Checkpoint selection method (optional)")
    @click.option("--checkpoint-epoch-number", help="Epoch number for checkpoint selection as JSON string (optional)")
    @click.option("--network-arch", help="Network architecture (optional)")
    def start_inference_microservice(docker_image, gpu_type, num_gpus, parent_job_id, kind, model_path, workspace_id, docker_env_vars, checkpoint_choose_method, checkpoint_epoch_number, network_arch):
        """Start an inference microservice"""
        result = click_obj.start_inference_microservice(
            docker_image=docker_image,
            gpu_type=gpu_type,
            num_gpus=num_gpus,
            parent_job_id=parent_job_id,
            kind=kind,
            model_path=model_path,
            workspace=workspace_id,
            docker_env_vars=docker_env_vars,
            checkpoint_choose_method=checkpoint_choose_method,
            checkpoint_epoch_number=checkpoint_epoch_number,
            network_arch=network_arch,
        )
        microservice_id = result.get("id")
        click.echo(f"Inference microservice started with ID: {microservice_id}")
        click.echo(json.dumps(result, indent=2))

    @wrapper.command(name="inference-request")
    @click.option("--microservice-job-id", required=True, help="Inference microservice job ID")
    @click.option("--input", help="Base64-encoded images/videos with data URI format as JSON array (optional)")
    @click.option("--media", help="Cloud path to media file (e.g., aws://bucket/path/to/video.mp4) (optional)")
    @click.option("--model", help="Model identifier (e.g. nvidia/nvdino-v2) (optional)")
    @click.option("--prompt", help="Text prompt for VLM inference (optional)")
    @click.option("--enable-lora", help="Enable LoRA for inference (true/false) (optional)")
    def inference_request(microservice_job_id, input, media, model, prompt, enable_lora):
        """Make an inference request to a running microservice"""
        result = click_obj.inference_request(
            microservice_job_id=microservice_job_id,
            input=input,
            media=media,
            model=model,
            prompt=prompt,
            enable_lora=enable_lora,
        )
        click.echo("Inference completed successfully:")
        click.echo(json.dumps(result, indent=2))

    @wrapper.command(name="get-inference-microservice-status")
    @click.option("--microservice-job-id", required=True, help="Inference microservice job ID")
    def get_inference_microservice_status(microservice_job_id):
        """Get inference microservice status"""
        status = click_obj.get_inference_microservice_status(microservice_job_id)
        click.echo(json.dumps(status, indent=2))

    @wrapper.command(name="stop-inference-microservice")
    @click.option("--microservice-job-id", required=True, help="Inference microservice job ID")
    def stop_inference_microservice(microservice_job_id):
        """Stop an inference microservice"""
        result = click_obj.stop_inference_microservice(microservice_job_id)
        click.echo(f"Inference microservice {microservice_job_id} stopped successfully.")
        if result:
            click.echo(json.dumps(result, indent=2))

    # Commands are automatically added to the wrapper in the order they are defined below
    # No need for explicit wrapper.add_command() calls - the @wrapper.command() decorator handles this

    return wrapper
