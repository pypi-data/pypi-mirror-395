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

"""Login modules"""

from configparser import ConfigParser
from tao_cli.cli_actions.actions import Actions

import click
import json
import os
from pathlib import Path

from tao_sdk import TaoClient


def _get_tao_base_url_from_config():
    """Get TAO_BASE_URL from config file if it exists."""
    
    config_path = Path.home() / ".tao" / "config"
    if config_path.exists():
        try:
            parser = ConfigParser()
            parser.read(config_path)
            
            # Try [CURRENT] section first, then DEFAULT section
            if parser.has_section('CURRENT') and 'TAO_BASE_URL' in parser['CURRENT']:
                return parser['CURRENT']['TAO_BASE_URL']
            elif 'TAO_BASE_URL' in parser['DEFAULT']:
                return parser['DEFAULT']['TAO_BASE_URL']
        except Exception:
            pass
    return None


def _get_tao_base_url_from_environment_variable():
    """Get TAO_BASE_URL from environment variable if it exists."""
    return os.getenv("TAO_BASE_URL")


def _validate_tao_base_url():
    """Custom validation to make tao-base-url required if not available from env var or config file"""
    return False if _get_tao_base_url_from_environment_variable() or _get_tao_base_url_from_config() else True


@click.command()
@click.option(
    "--tao-base-url", 
    prompt="tao_base_url",
    prompt_required=False,
    help="TAO API base URL (required if not set in environment variable or config file)",
    required=_validate_tao_base_url()
)
@click.option(
    "--ngc-org-name", prompt="ngc_org_name", help="Your NGC ORG.", required=True
)
@click.option(
    "--ngc-key", prompt="ngc_key", help="Your NGC Personal KEY.", required=True
)
@click.option(
    "--enable-telemetry",
    is_flag=True,
    help="Enable telemetry collection.",
    default=None,
)
def login(tao_base_url, ngc_org_name, ngc_key, enable_telemetry):
    """User login method"""
    
    # Check if TAO_BASE_URL is already set in environment or config file
    env_base_url = os.getenv("TAO_BASE_URL")
    config_base_url = _get_tao_base_url_from_config()
    
    # Use environment variable first, then config file, if option not provided
    if not tao_base_url:
        if env_base_url:
            tao_base_url = env_base_url
            click.echo(f"Using TAO_BASE_URL from environment: {tao_base_url}")
        elif config_base_url:
            tao_base_url = config_base_url
            click.echo(f"Using TAO_BASE_URL from config file: {tao_base_url}")
    
    client = TaoClient()
    creds = client.login(ngc_key, ngc_org_name, enable_telemetry, tao_base_url)
    click.echo("Login successful! Credentials have been saved to ~/.tao/config")


@click.command()
def logout():
    """User logout method - clears saved credentials"""
    actions = Actions()
    result = actions.logout()
    click.echo(result["message"])


@click.command()
def whoami():
    """Show current authentication status"""
    client = TaoClient()
    if client.is_authenticated():
        click.echo(f"Authenticated as: {client.org_name}")
        click.echo(f"API Base URL: {client.base_url}")
    else:
        click.echo("Not authenticated. Please run 'tao login' to authenticate.")


@click.command()
def get_gpu_types():
    """Get available GPU types"""
    client = TaoClient()
    gpu_types = client.get_gpu_types()
    click.echo(json.dumps(gpu_types, indent=2))
