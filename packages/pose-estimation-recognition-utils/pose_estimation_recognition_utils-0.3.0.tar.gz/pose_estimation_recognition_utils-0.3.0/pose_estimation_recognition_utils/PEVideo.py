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
PEVideo.py

This module defines a class for saving pose estimation data of a video.

Author: Jonas David Stephan, Nathalie Dollmann
Date: 2025-08-04
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json

from .VideoSkeletonData import VideoSkeletonData
from typing import List


class PEVideo:
    """
    Represents skeleton data for a video.

    Attributes:
        origin (str): the name of the tool for pose estimation
        data (list): list of the VideoSkeletonData
    """
    def __init__(self, origin: str, data=None):
        """
        Initialize a new PEVideo instance.

        Args:
            origin (str): the name of the tool for pose estimation
            data (list): list of the VideoSkeletonData
        """
        if data is None:
            data=[]
        self.origin = origin
        self.data = data

    def set_data(self, data: List[VideoSkeletonData]) -> None:
        """
        Adds the VideoSkeletonData to the object.

        Args:
            data (list): list of the VideoSkeletonData
        """
        self.data = data

    def get_data(self) -> List[VideoSkeletonData]:
        """
        Retrieve the VideoSkeletonData to the object.

        Returns:
            VideoSkeletonData: The VideoSkeletonData Object of the video.
        """
        return self.data
    
    def add_frame(self, frame: VideoSkeletonData):
        """
        Adds the frame to the data list.

        Args:
            frame (VideoSkeletonData): video skeleton object of a frame
        """
        self.data.append(frame)

    def to_json(self) -> str:
        """
        Retrieve the object as JSON string.

        Returns:
             str: The object as JSON string.
        """
        return json.dumps({
            "origin": self.origin,
            "frames": [json.loads(frame.to_json()) for frame in self.data]
        }, indent=2)

    def save_in_file(self, filename:str) -> None:
        """
        Writes the object in JSON format into file

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with open(filename, "w") as f:
            f.write(self.to_json())