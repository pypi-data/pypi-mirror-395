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

"""Add click network groups to the cli command"""

import click

import tao_cli.common

from nvidia_tao_core.microservices.enum_constants import _get_network_architectures
from tao_cli.cli_actions.network_click_wrapper import create_click_group


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


@click.group(cls=OrderedGroup)
@click.version_option(package_name="nvidia-tao-client")
@click.pass_context
def cli(ctx):
    """Create base tao click group"""
    pass


# Authentication commands - placed at the top for visibility
cli.add_command(tao_cli.common.login)
cli.add_command(tao_cli.common.logout)
cli.add_command(tao_cli.common.whoami)

# Utility commands
# Note: get-gpu-types moved to network wrapper commands


# Visual separator
@cli.command(name="------ DATA SERVICES -----")
def data_services_separator():
    """ """
    click.echo("This is a visual separator. Data service commands are listed below.")

# Data Services
for ds_network_name in [
    "image",
    "analytics", 
    "annotations", 
    "augmentation", 
    "auto_label"
]:
    click_group = create_click_group(
        ds_network_name, f"{ds_network_name} data service"
    )
    cli.add_command(click_group)


# Visual separator
@cli.command(name="---- NETWORK SERVICES ----")
def networks_separator():
    """ """
    click.echo("This is a visual separator. Network architecture commands are listed below.")

# PYTORCH CV networks - using dynamic list from core but maintaining organization
network_architectures = _get_network_architectures()
for pyt_network_name in sorted(network_architectures):
    click_group = create_click_group(
        pyt_network_name, f"{pyt_network_name} network architecture"
    )
    cli.add_command(click_group)


if __name__ == "__main__":
    cli()
