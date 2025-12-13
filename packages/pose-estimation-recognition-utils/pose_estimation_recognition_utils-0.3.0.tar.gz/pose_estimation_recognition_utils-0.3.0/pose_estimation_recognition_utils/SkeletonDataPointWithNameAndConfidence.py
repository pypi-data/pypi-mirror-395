# Copyright 2025 Jonas David Stephan
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
"""
SkeletonDataPointWithNameAndConfidence.py

This module defines a class to represent a single data point in a 3D skeleton model with confidence.

Author: Jonas David Stephan
Date: 2025-12-06
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""
from .SkeletonDataPointWithName import SkeletonDataPointWithName

class SkeletonDataPointWithNameAndConfidence(SkeletonDataPointWithName):

    def __init__(self, idx: int, name: str, x: float, y: float, z: float, confidence: float):
        """
        Initialize a new SkeletonDataPointWithNameAndConfidence instance.

        Args:
            idx (int): The ID of the data point.
            name (str): The name associated with the data point.
            x (float): The x-coordinate of the data point.
            y (float): The y-coordinate of the data point.
            z (float): The z-coordinate of the data point.
            confidence (float): The confidence value of the data point.

        Raises:
            ValueError: If confidence is invalid.
        """
        super().__init__(idx, name, x, y, z)
        if not isinstance(confidence, (int, float)):
            raise ValueError("Confidence must be numeric.")
        self.data["confidence"]=float(confidence)