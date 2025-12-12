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

"""A deterministic seed generator for reproducible random number generation."""

import random
from typing import Optional

class SeedGenerator:
    """A deterministic seed generator for reproducible random number generation.
    
    This implementation guarantees consistent results across different machines,
    Python versions, and platforms by using integer-based seed generation.
    """
    def __init__(self, base_seed: int = 42):
        self.base_seed = base_seed
        self.rng = random.Random(base_seed)
    
    def get_seed(self, index: int, sub_index: Optional[int] = None) -> int:
        # Use integer operations instead of string formatting
        # This ensures consistent behavior across platforms
        if sub_index is not None:
            # Combine seeds using prime numbers and bit operations
            # to minimize collisions and maintain reproducibility
            combined_seed = self.base_seed
            combined_seed = (combined_seed * 2147483647) + index  # Use prime number
            combined_seed = (combined_seed * 2147483647) + (sub_index if sub_index is not None else 0)
        else:
            combined_seed = (self.base_seed * 2147483647) + index
        
        self.rng.seed(combined_seed)
        return self.rng.randint(0, 2**32 - 1) 