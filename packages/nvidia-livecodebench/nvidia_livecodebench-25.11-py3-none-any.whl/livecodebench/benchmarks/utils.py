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

from datetime import datetime
from datasets import Dataset

def parse_date(date):
    """Ensure the date is converted to a datetime object and normalized to 'YYYY-MM-DD'."""
    if not date:
        return None
    if isinstance(date, datetime):
        return date.date()  # Convert datetime to date for consistent comparison
    try:
        return datetime.strptime(date[:10], "%Y-%m-%d").date()  # Handle both 'YYYY-MM-DD' and 'YYYY-MM-DDTHH:MM:SS'
    except ValueError:
        raise ValueError(f"Invalid date format: {date}")

def filter_dataset_by_date(dataset: Dataset, start_date: str = None, end_date: str = None) -> Dataset:
    """
    Filters the Hugging Face dataset based on the given date range.
    
    Args:
        dataset (Dataset): The Hugging Face dataset to be filtered.
        start_date (str, optional): The start date in the format "YYYY-MM-DD". Defaults to None.
        end_date (str, optional): The end date in the format "YYYY-MM-DD". Defaults to None.
        
    Returns:
        Dataset: A filtered Hugging Face dataset.
    """
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    return dataset.filter(
        lambda example: (
            (not start_date or parse_date(example["contest_date"]) >= start_date) and
            (not end_date or parse_date(example["contest_date"]) <= end_date)
        )
    )
