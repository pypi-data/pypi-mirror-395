# Copyright 2025 Chanyut Boonkhamsaen, Nathalie Dollmann, Jonas David Stephan
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
Save2DDataWithName.py

This module defines a class for saving a combination of id, name, x coordinate and y coordinate.

Author: Chanyut Boonkhamsaen, Nathalie Dollmann, Jonas David Stephan
Date: 2025-07-18
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json

from typing import Dict

class Save2DDataWithName:

    def __init__(self, idx: int, name: str, x: float, y: float):
        """
        Initialize a new save2Ddata instance with an additional "name" attribute.

        Args:
            idx (int): The ID of the data point.
            name (str): The name associated with the data point.
            x (float): The x-coordinate of the data point.
            y (float): The y-coordinate of the data point.

        Raises:
            ValueError: If any of the coordinates are invalid (e.g., None or not numeric).
        """
        if not all(isinstance(coord, (int, float)) for coord in [x, y]):
            raise ValueError("Coordinates x and y must be numeric.")
        if not isinstance(name, str):
            raise ValueError("The name must be a string.")
        self.data: Dict[str, object]={"id": idx, "name": name, "x": x, "y": y}

    def get_data(self) -> Dict[str, object]:
        """
        Retrieve the data point as a dictionary.

        Returns:
            dict: The dictionary representation of the data point.
        """

        return self.data

    def to_json(self) -> str:
        """
        Convert the data point to a JSON string.

        Returns:
            str: The JSON-formatted string representation of the data point.
        """

        return json.dumps(self.data, indent=4)
        