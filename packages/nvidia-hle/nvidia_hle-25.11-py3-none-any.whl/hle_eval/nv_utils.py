# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from pathlib import Path
import time

import requests


def get_oauth_token(force: bool = False):
    """
    Get OAuth token for Azure OpenAI authentication.
    
    This function is used by the judging system to authenticate with Azure OpenAI
    for evaluating model responses using GPT-4o.
    
    Required environment variables:
    - OPENAI_TOKEN_URL: The OAuth token endpoint URL
    - OPENAI_CLIENT_ID: The OAuth client ID
    - OPENAI_CLIENT_SECRET: The OAuth client secret
    - OPENAI_SCOPE: The OAuth scope for authentication
    
    Args:
        force (bool): If True, force refresh the token even if cached
        
    Returns:
        str: The OAuth access token
        
    Raises:
        ValueError: If any required environment variables are missing
    """
    # Get required environment variables
    p_token_url = os.environ.get("OPENAI_TOKEN_URL")
    p_client_id = os.environ.get("OPENAI_CLIENT_ID")
    p_client_secret = os.environ.get("OPENAI_CLIENT_SECRET")
    p_scope = os.environ.get("OPENAI_SCOPE")

    # Check which variables are missing and provide clear error messages
    missing_vars = []
    if p_token_url is None:
        missing_vars.append("OPENAI_TOKEN_URL")
    if p_client_id is None:
        missing_vars.append("OPENAI_CLIENT_ID")
    if p_client_secret is None:
        missing_vars.append("OPENAI_CLIENT_SECRET")
    if p_scope is None:
        missing_vars.append("OPENAI_SCOPE")
    
    if missing_vars:
        error_msg = f"Missing required environment variables for OAuth authentication: {', '.join(missing_vars)}"
        error_msg += "\nPlease set these environment variables to use Azure OpenAI for judging."
        raise ValueError(error_msg)

    file_name = "py_llm_oauth_token.json"
    try:
        base_path = Path(__file__).parent
        file_path = Path.joinpath(base_path, file_name)
    except Exception as e:
        print(f"Error occurred while setting file path: {e}")
        return None

    try:
        # Check if the token is cached
        if not force and os.path.exists(file_path):
            with open(file_path, "r") as f:
                token = json.load(f)
        else:
            # Get a new token from the OAuth server
            response = requests.post(
                p_token_url,
                data={"grant_type": "client_credentials", "client_id": p_client_id,
                      "client_secret": p_client_secret, "scope": p_scope}
            )
            response.raise_for_status()
            token = response.json()
            with open(file_path, "w") as f:
                json.dump(token, f)
    except Exception as e:
        print(f"Error occurred while getting OAuth token: {e}")
        return None

    try:
        # Check if the token is expired
        expires_in = time.time() + token["expires_in"]
        if time.time() > expires_in:
            # Refresh the token
            if os.path.exists(file_path):
                os.remove(file_path)
            token = get_oauth_token()
    except Exception as e:
        print(f"Error occurred while while getting OAuth token: {e}")
        return None

    authToken = token["access_token"]
    return authToken