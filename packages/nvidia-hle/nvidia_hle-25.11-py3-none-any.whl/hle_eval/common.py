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
import asyncio
import json
from diskcache import Cache
from pathlib import Path
from tqdm import tqdm

async def map_with_progress(
    func: callable,
    items: list[list],
    async_limit: int = 10,
    cache_dir: str = "./",
    table_name: str = "predictions"
):
    """
    Asynchronously apply a function to each element of a list with progress tracking and diskcache caching.

    Parameters:
    - func: Callable function to apply to each element.
    - items: List of inputs to process.
    - async_limit: Number of concurrent tasks.
    - cache_dir: Path to the cache directory for diskcache.

    Returns:
    - List of results.
    """
    semaphore = asyncio.Semaphore(async_limit)

    if os.path.exists(cache_dir):
        print(f"Found existing cache directory: {cache_dir}, cached predictions will be used if available")
    os.makedirs(cache_dir, exist_ok=True)

    cache = Cache(Path(cache_dir) / "cache")
    
    async def worker(idx, item):
        cache_key = f"{table_name}_{idx}"

        async with semaphore:
            # Try to get from cache with error handling
            try:
                if cache_key in cache:
                    cached_result = cache[cache_key]
                    if cached_result is not None:
                        return cached_result
            except (ValueError, TypeError, KeyError, Exception) as e:
                # Cache entry is corrupted or incompatible, skip it
                print(f"Cache read error for key {cache_key}: {e}")
                pass

            # Execute the function
            result = await func(*item)
            
            # Store result in cache with error handling
            try:
                cache[cache_key] = result
            except (TypeError, ValueError) as e:
                print(f"Cache write error for key {cache_key}: {e}")
                # Continue without caching if serialization fails
            
            return result

    tasks = [worker(idx, item) for idx, item in enumerate(items)]
    
    results = []
    for future in tqdm(asyncio.as_completed(tasks), total=len(items)):
        results.append(await future)
    
    cache.close()
    return results
