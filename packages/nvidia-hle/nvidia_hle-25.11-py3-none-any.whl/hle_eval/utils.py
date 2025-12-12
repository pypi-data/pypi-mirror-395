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

import os
import time
import httpx

from hle_eval.nv_utils import get_oauth_token

# API setting constants
API_RETRY_SLEEP = 10
API_ERROR_OUTPUT = "$ERROR$"


async def chat_completion_async_openai(model, messages, temperature, top_p, max_new_tokens, max_retries, api_dict=None):
    try:
        import openai
    except ImportError:
        raise ImportError("Please install openai package to evaluate openai models")

    if api_dict:
        client = openai.AsyncOpenAI(
            base_url=api_dict["api_base"],
            api_key=api_dict["api_key"] if api_dict["api_key"] is not None else "",
            timeout=api_dict["timeout"],
        )
    else:
        client = openai.AsyncOpenAI()
    
    for _ in range(max_retries):
        try:
            completion = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_completion_tokens=max_new_tokens,
            )
            break
        except openai.RateLimitError as e:
            print(type(e), e)
            time.sleep(API_RETRY_SLEEP)
        except openai.BadRequestError as e:
            print(type(e), e)
            break
        except openai.OpenAIError as e:
            print(type(e), e)
            break
        except KeyError:
            print(type(e), e)
            break

        time.sleep(API_RETRY_SLEEP) # Sleep after every request
    
    return completion


async def chat_completion_async_nvidia_api(model, messages, temperature, top_p, max_new_tokens, max_retries, api_dict=None):
    headers={
        "content-type": "application/json", 
        }
    if api_dict['api_key'] is not None:
        headers["Authorization"] = f"Bearer {api_dict['api_key']}"

    payload = {
        "messages": messages,
        "model": model,
        "max_tokens": max_new_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "stream": False,
    }
    
    for _ in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    api_dict["api_base"], headers=headers, json=payload, timeout=api_dict["timeout"])
            break
        except Exception as e:
            print(f"**API REQUEST ERROR** Reason: {e}.")

    if response.status_code != 200:
        print(response.json())
        print(f"**API REQUEST ERROR** Reason: status code {response.status_code}.")
    return response


async def chat_completion_async_openai_azure(model, messages, temperature, top_p, max_new_tokens, max_retries, api_dict=None):
    try:
        import openai
        from openai import AsyncAzureOpenAI
    except ImportError:
        raise ImportError("Please install openai package to evaluate openai azure models")

    client = AsyncAzureOpenAI(
        azure_endpoint=api_dict["api_base"],
        api_key=get_oauth_token(force=True),
        timeout=api_dict["timeout"],
    )

    for _ in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                n=1,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_new_tokens,
            )
            break
        except openai.AuthenticationError:
            new_api_key = get_oauth_token(force=True)
            client = AsyncAzureOpenAI(
                azure_endpoint=api_dict["api_base"],
                api_key=new_api_key,
                timeout=api_dict["timeout"],
            )
        except openai.RateLimitError as e:
            print(type(e), e)
            time.sleep(API_RETRY_SLEEP)
        except openai.BadRequestError as e:
            print(type(e), e)
            break
        except openai.OpenAIError as e:
            print(type(e), e)
            break
        except KeyError:
            print(type(e), e)
            break
    
    return response


# Used only for judging
async def chat_parse_async_openai_azure(model, messages, temperature, max_new_tokens, response_format, max_retries=5, api_dict=None):
    try:
        import openai
        from openai import AsyncAzureOpenAI
    except ImportError:
        raise ImportError("Please install openai package to evaluate openai azure models")

    if api_dict:
        client = AsyncAzureOpenAI(
            azure_endpoint=api_dict["api_base"],
            api_key=get_oauth_token(force=True),
            timeout=300.0,
        )
    else:
        client = AsyncAzureOpenAI(
            api_key=get_oauth_token(force=True),
            timeout=300.0,
        )

    response = None
    for _ in range(max_retries):
        try:
            response = await client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                temperature=temperature,
                max_completion_tokens=max_new_tokens,
                response_format=response_format, 
            )
            break
        except openai.AuthenticationError:
            new_api_key = get_oauth_token(force=True)
            if api_dict:
                client = AsyncAzureOpenAI(
                    azure_endpoint=api_dict["api_base"],
                    api_key=new_api_key,
                    timeout=300.0,
                )
            else:
                client = AsyncAzureOpenAI(
                    api_key=new_api_key,
                    timeout=300.0,
                )
        except openai.RateLimitError as e:
            print(type(e), e)
            time.sleep(API_RETRY_SLEEP)
        except openai.BadRequestError as e:
            print(type(e), e)
            break
        except openai.OpenAIError as e:
            print(type(e), e)
            break
        except KeyError:
            print(type(e), e)
            break
    
    return response