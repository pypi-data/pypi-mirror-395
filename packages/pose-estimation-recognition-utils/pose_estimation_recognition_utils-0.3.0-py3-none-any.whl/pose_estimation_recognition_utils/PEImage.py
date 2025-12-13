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
PEImage.py

This module defines a class for saving pose estimation data of an image.

Author: Jonas David Stephan
Date: 2025-08-02
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json

from .ImageSkeletonData import ImageSkeletonData


class PEImage:
    """
    Represents skeleton data for an image.

    Attributes:
        origin (str): the name of the tool for pose estimation
        data (ImageSkeletonData): The ImageSkeletonData Object of the image
    """
    def __init__(self, origin: str, data: ImageSkeletonData = None):
        """
        Initialize a new PEImage instance.

        Args:
            origin (str): the name of the tool for pose estimation
            data (ImageSkeletonData): The ImageSkeletonData Object of the image
        """
        self.origin = origin
        self.data = data

    def set_data(self, data: ImageSkeletonData) -> None:
        """
        Adds the ImageSkeletonData to the object.

        Args:
            data (ImageSkeletonData): The ImageSkeletonData Object of the image
        """
        self.data = data

    def get_data(self) -> ImageSkeletonData:
        """
        Retrieve the ImageSkeletonData to the object.

        Returns:
            ImageSkeletonData: The ImageSkeletonData Object of the image.
        """
        return self.data

    def to_json(self) -> str:
        """
        Retrieve the object as JSON string.

        Returns:
             str: The object as JSON string.
        """
        return json.dumps({
            "origin": self.origin,
            "skeletonpoints": json.loads(self.data.to_json())
        }, indent=2)

    def save_in_file(self, filename:str) -> None:
        """
        Writes the object in JSON format into file

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with open(filename, "w") as f:
            f.write(self.to_json())