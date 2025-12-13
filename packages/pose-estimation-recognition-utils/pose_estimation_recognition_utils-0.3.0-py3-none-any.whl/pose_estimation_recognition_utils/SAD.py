# Copyright 2025 Nathalie Dollmann, Jonas David Stephan
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
SAD.py

This module defines a class for the implementation of SAD algorithm.

Author: Nathalie Dollmann, Jonas David Stephan
Date: 2025-07-18
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

from typing import List, Union

from .SkeletonDataPoint import SkeletonDataPoint
from .SkeletonDataPointWithName import SkeletonDataPointWithName
from .Save2DData import Save2DData
from .Save2DDataWithName import Save2DDataWithName
from .Save2DDataWithConfidence import Save2DDataWithConfidence
from .Save2DDataWithNameAndConfidence import Save2DDataWithNameAndConfidence

class SAD:

    def __init__(self, distance: float, focal_length: float, cx_left: float, cy_left: float):
        """
        Initialize a new SAD instance.

        Args:
            distance (float): distance between camera centers in millimeters
            focal_length (float): focal length of cameras in pixels
            cx_left (float): x-coordinate of the principal point (optical center) for the left camera in pixels
            cy_left (float): y-coordinate of the principal point (optical center) for the left camera in pixels
        """
        self.focal_length = focal_length
        self.fB = focal_length * distance
        self.cx_left = cx_left
        self.cy_left = cy_left

    def merge_pixel(self, pixel_list_left: List[Union[Save2DData, Save2DDataWithName, Save2DDataWithConfidence, Save2DDataWithNameAndConfidence]],
                    pixel_list_right: List[Union[Save2DData, Save2DDataWithName, Save2DDataWithConfidence, Save2DDataWithNameAndConfidence]]) -> List[Union[SkeletonDataPoint, SkeletonDataPointWithName]]:
        """ 
        Convert 2D pixel coordinates from left and right stereo images to 3D coordinates.
        
        This method computes the 3D position (x, y, z) for each corresponding point pair
        using the disparity between left and right image coordinates. The z-coordinate
        represents depth from the camera.        

        Args:
            pixel_list_left (list): list of 2D data points from the left camera image
            pixel_list_right (list): lsit of corresponding 2D data points from the right camera image

        Returns:
            list: list of 3D data points (SkeletonDataPoint or SkeletonDataPointWithName) containing the calculated (x, y, z) coordinates in real-world units.
        """
        
        back = []
        l = len(pixel_list_left)
        for i in range(l):
            x_left = pixel_list_left[i].data['x']
            x_right = pixel_list_right[i].data['x']
            
            if x_left != 0 and x_right != 0:
                difference = x_left - x_right
                z = self.fB / difference
            
                y_left = pixel_list_left[i].data['y']
                x = ((x_left - self.cx_left) * z) / self.focal_length
                y = ((y_left - self.cy_left) * z) / self.focal_length
                
                if isinstance(pixel_list_left[i], Save2DData):
                    back.append(SkeletonDataPoint(pixel_list_left[i].data['id'], x, y, z))
                else:
                    back.append(SkeletonDataPointWithName(pixel_list_left[i].data['id'], pixel_list_left[i].data['name'], x, y, z))
            else:
                if isinstance(pixel_list_left[i], Save2DData):
                    back.append(SkeletonDataPoint(pixel_list_left[i].data['id'], 0, 0, 0))
                else:
                    back.append(SkeletonDataPointWithName(pixel_list_left[i].data['id'], pixel_list_left[i].data['name'], 0, 0, 0))

        return back