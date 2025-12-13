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
SkeletonLoader.py

This module provides functions to load and filter skeleton data from a JSON file, string, or object for image data.

Author: Jonas David Stephan
Date: 2025-01-28
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""
import numpy as np
import json

from typing import List, Set, Tuple

from pose_estimation_recognition_utils import ImageSkeletonData


def load_image_skeleton(file_path: str, points_to_include: str) -> np.ndarray:
    """
    Loads skeleton data from a JSON file and filters the points based on specified ranges and individual points for video data.

    Args:
        file_path (str): Path to the JSON file containing the skeleton data.
        points_to_include (str): A string specifying the ranges and individual point IDs to include.
                                 Ranges and individual points are separated by commas.
                                 For example: "1-22,100-150,200".

    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    with open(file_path, "r") as file:
        file_content = file.read()
        return load_image_skeleton_from_string(file_content, points_to_include)
    

def load_image_skeleton_all_points(file_path: str, points_to_include: str) -> np.ndarray:
    """
    Loads skeleton data from a JSON file and filters the points based on specified ranges and individual points for video data.

    Args:
        file_path (str): Path to the JSON file containing the skeleton data.
        points_to_include (str): A string specifying the ranges and individual point IDs to include.
                                 Ranges and individual points are separated by commas.
                                 For example: "1-22,100-150,200".

    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    with open(file_path, "r") as file:
        file_content = file.read()
        return load_image_skeleton_from_string_all_points(file_content, points_to_include)


def load_image_skeleton_from_string(string: str, points_to_include: str) -> np.ndarray:
    """
        Loads skeleton data from a string and filters the points based on specified ranges and individual points for image data.

        Args:
            string: JSON from file or Divider containing the skeleton data.
            points_to_include (str): A string specifying the ranges and individual point IDs to include.
                                     Ranges and individual points are separated by commas.
                                     For example: "1-22,100-150,200".

        Returns:
            np.ndarray: A numpy array containing the filtered skeleton data.
        """

    content = json.loads(string)

    points: Set[int] = set()
    ranges: List[Tuple[int, int]] = []

    for part in points_to_include.split(','):
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        else:
            points.add(int(part))

    def should_include_point(point_id):
        if point_id in points:
            return True
        for start_id, end_id in ranges:
            if start_id <= point_id <= end_id:
                return True
        return False

    point_array = []
    for point in content['skeletonpoints']:
        if should_include_point(point['id']):
            skeleton_array = np.array([point['x'], point['y'], point['z']])
            point_array.append(skeleton_array)

    return np.array(point_array)


def load_image_skeleton_from_string_all_points(string: str, points_to_include: str) -> np.ndarray:
    """
        Loads skeleton data from a string and filters the points based on specified ranges and individual points for image data. Fill unwanted points with zeros.

        Args:
            string: JSON from file or Divider containing the skeleton data.
            points_to_include (str): A string specifying the ranges and individual point IDs to include.
                                     Ranges and individual points are separated by commas.
                                     For example: "1-22,100-150,200".

        Returns:
            np.ndarray: A numpy array containing the filtered skeleton data.
        """

    content = json.loads(string)

    points: Set[int] = set()
    ranges: List[Tuple[int, int]] = []

    for part in points_to_include.split(','):
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        else:
            points.add(int(part))

    def should_include_point(point_id):
        if point_id in points:
            return True
        for start_id, end_id in ranges:
            if start_id <= point_id <= end_id:
                return True
        return False

    point_array = []
    for point in content['skeletonpoints']:
        if should_include_point(point['id']):
            skeleton_array = np.array([point['x'], point['y'], point['z']])
            point_array.append(skeleton_array)
        else:
            skeleton_array = np.array([0, 0, 0])
            point_array.append(skeleton_array)

    return np.array(point_array)


def load_image_skeleton_object(skeleton_object: ImageSkeletonData, points_to_include: str) -> np.ndarray:
    """
    Loads skeleton data from an object and filters the points based on specified ranges and individual points for image data.

    Args:
        skeleton_object (ImageSkeletonData): A list of frames, where each frame contains data points representing skeleton points.
        points_to_include (str): A string specifying the ranges and individual point IDs to include.
                                 Ranges and individual points are separated by commas.
                                 For example: "1-22,100-150,200".

    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    points: Set[int] = set()
    ranges: List[Tuple[int, int]] = []

    for part in points_to_include.split(','):
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        else:
            points.add(int(part))

    def should_include_point(point_id):
        if point_id in points:
            return True
        for start_id, end_id in ranges:
            if start_id <= point_id <= end_id:
                return True
        return False

    point_array = []
    for point in skeleton_object.get_data_points():
        if should_include_point(point.data['id']):
            skeleton_array = np.array([point.data['x'], point.data['y'], point.data['z']])
            point_array.append(skeleton_array)

    return np.array(point_array)


def load_image_skeleton_object_all_points(skeleton_object: ImageSkeletonData, points_to_include: str) -> np.ndarray:
    """
    Loads skeleton data from an object and filters the points based on specified ranges and individual points for image data. Fill unwanted points with zeros.

    Args:
        skeleton_object (ImageSkeletonData): A list of frames, where each frame contains data points representing skeleton points.
        points_to_include (str): A string specifying the ranges and individual point IDs to include.
                                 Ranges and individual points are separated by commas.
                                 For example: "1-22,100-150,200".

    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    points: Set[int] = set()
    ranges: List[Tuple[int, int]] = []

    for part in points_to_include.split(','):
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        else:
            points.add(int(part))

    def should_include_point(point_id):
        if point_id in points:
            return True
        for start_id, end_id in ranges:
            if start_id <= point_id <= end_id:
                return True
        return False

    point_array = []
    for point in skeleton_object.get_data_points():
        if should_include_point(point.data['id']):
            skeleton_array = np.array([point.data['x'], point.data['y'], point.data['z']])
            point_array.append(skeleton_array)
        else:
            skeleton_array = np.array([0, 0, 0])
            point_array.append(skeleton_array)

    return np.array(point_array)
