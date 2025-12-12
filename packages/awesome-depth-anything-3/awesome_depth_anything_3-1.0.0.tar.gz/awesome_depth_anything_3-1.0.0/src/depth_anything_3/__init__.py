# Copyright (c) 2025 Delanoe Pirard / Aedelon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Awesome Depth Anything 3 - Optimized wrapper for Depth Anything 3.

Provides metric depth estimation, point clouds, camera poses and novel views
from any images.

Example:
    >>> from depth_anything_3 import DepthAnything3
    >>> model = DepthAnything3.from_pretrained("Aedelon/DA3-NestedGiant")
    >>> prediction = model.inference(images)
"""

__version__ = "1.0.0"
__author__ = "Delanoe Pirard"
__license__ = "Apache-2.0"

from depth_anything_3.api import DepthAnything3
from depth_anything_3.specs import Prediction

__all__ = [
    "__version__",
    "DepthAnything3",
    "Prediction",
]
