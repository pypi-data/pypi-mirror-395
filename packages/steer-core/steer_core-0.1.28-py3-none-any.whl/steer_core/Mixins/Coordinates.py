import numpy as np
import pandas as pd
from typing import Tuple

from shapely import Polygon, minimum_bounding_circle, Point


class CoordinateMixin:
    """
    A class to manage and manipulate 3D coordinates.
    Provides methods for rotation, area calculation, and coordinate ordering.
    """
    @staticmethod
    def get_radius_of_points(coords: np.ndarray) -> float:
        """Calculate the radius of a spiral given its coordinates.

        Parameters
        ----------
        coords : np.ndarray
            Array of shape (N, 2) with columns [x, z]

        Returns
        -------
        float
            Radius of the spiral in meters

        Raises
        ------
        ValueError
            If input coordinates are invalid
        """
        polygon = Polygon(coords)
        circle = minimum_bounding_circle(polygon)
        center = circle.centroid
        first_point = list(circle.exterior.coords)[0]
        radius = Point(center).distance(Point(first_point))
        return radius, (center.x, center.y)

    @staticmethod
    def _calculate_segment_center_line(x_coords: np.ndarray, z_coords: np.ndarray) -> np.ndarray:
        """
        Calculate center line for a single segment of coordinates.
        
        Parameters
        ----------
        x_coords : np.ndarray
            X coordinates for the segment
        z_coords : np.ndarray
            Z coordinates for the segment
            
        Returns
        -------
        np.ndarray
            Array containing start and end points of the center line [[min_x, mean_z], [max_x, mean_z]]
        """
        min_x = np.nanmin(x_coords)
        max_x = np.nanmax(x_coords)
        min_z = np.nanmin(z_coords)
        max_z = np.nanmax(z_coords)
        mean_z = max_z - (max_z - min_z) / 2
        
        return np.array([[min_x, mean_z], [max_x, mean_z]])

    @staticmethod
    def get_xz_center_line(coordinates: np.ndarray) -> np.ndarray:
        """
        Generate center line(s) for coordinate data, handling both single and multi-segment polygons.
        
        Parameters
        ----------
        coordinates : np.ndarray
            Array of 3D coordinates with shape (N, 3) where columns are [x, y, z].
            NaN values in x or z coordinates indicate breaks between polygon segments.
            
        Returns
        -------
        np.ndarray
            For single polygon: Array with shape (2, 2) containing start and end points.
            For multiple segments: Array with center lines for each segment separated by [NaN, NaN].
            For empty coordinates: Empty array with shape (0, 2).
        """
        if coordinates.size == 0:
            return np.array([]).reshape(0, 2)
            
        x_coords = coordinates[:, 0]
        z_coords = coordinates[:, 2]
        
        x_is_nan = np.isnan(x_coords)
        
        if np.any(x_is_nan):
            # Handle multiple segments separated by NaN values
            result_points = []
            
            # Find NaN indices to split the segments
            nan_indices = np.where(x_is_nan)[0]
            start_idx = 0
            
            # Process each segment
            for nan_idx in nan_indices:
                if nan_idx > start_idx:
                    segment_x = x_coords[start_idx:nan_idx]
                    segment_z = z_coords[start_idx:nan_idx]
                    
                    # Calculate center line for this segment if it has valid points
                    if len(segment_x) > 0 and not np.all(np.isnan(segment_x)):
                        segment_line = CoordinateMixin._calculate_segment_center_line(segment_x, segment_z)
                        result_points.extend(segment_line.tolist())
                        result_points.append([np.nan, np.nan])  # Add separator
                
                start_idx = nan_idx + 1
            
            # Handle the last segment if it exists
            if start_idx < len(x_coords):
                segment_x = x_coords[start_idx:]
                segment_z = z_coords[start_idx:]
                
                if len(segment_x) > 0 and not np.all(np.isnan(segment_x)):
                    segment_line = CoordinateMixin._calculate_segment_center_line(segment_x, segment_z)
                    result_points.extend(segment_line.tolist())
            
            # Remove trailing NaN separator if it exists
            if result_points and np.isnan(result_points[-1][0]):
                result_points.pop()
            
            return np.array(result_points) if result_points else np.array([]).reshape(0, 2)
        
        else:
            # Single polygon - use helper function
            return CoordinateMixin._calculate_segment_center_line(x_coords, z_coords)

    @staticmethod
    def rotate_coordinates(
        coords: np.ndarray, 
        axis: str, 
        angle: float, 
        center: tuple = None
    ) -> np.ndarray:
        """
        Rotate a (N, 3) NumPy array of 3D coordinates around the specified axis.
        Can handle coordinates with None values (preserves None positions).

        :param coords: NumPy array of shape (N, 3), where columns are x, y, z
        :param axis: Axis to rotate around ('x', 'y', or 'z')
        :param angle: Angle in degrees
        :param center: Point to rotate around as (x, y, z) tuple. If None, rotates around origin.
        :return: Rotated NumPy array of shape (N, 3)
        """
        if coords.shape[1] != 3:
            raise ValueError(
                "Input array must have shape (N, 3) for x, y, z coordinates"
            )

        # Validate center parameter
        if center is not None:
            if not isinstance(center, (tuple, list)) or len(center) != 3:
                raise ValueError(
                    "Center must be a tuple or list of 3 coordinates (x, y, z)"
                )
            if not all(isinstance(coord, (int, float)) for coord in center):
                raise TypeError("All center coordinates must be numbers")
            center = np.array(center, dtype=float)

        # Check if we have None values
        has_nones = (
            np.any(pd.isna(coords[:, 0]))
            if hasattr(pd, "isna")
            else np.any(coords[:, 0] == None)
        )

        if has_nones:
            # Create a copy to preserve original
            result = coords.copy()

            # Find non-None rows
            x_is_none = (
                pd.isna(coords[:, 0]) if hasattr(pd, "isna") else (coords[:, 0] == None)
            )
            valid_mask = ~x_is_none

            if np.any(valid_mask):
                # Extract valid coordinates and convert to float
                valid_coords = coords[valid_mask].astype(float)

                # Apply rotation to valid coordinates
                rotated_valid = CoordinateMixin._rotate_around_center(
                    valid_coords, axis, angle, center
                )

                # Put rotated coordinates back in result
                result[valid_mask] = rotated_valid

            return result

        else:
            # No None values - use rotation with center
            return CoordinateMixin._rotate_around_center(
                coords.astype(float), axis, angle, center
            )

    @staticmethod
    def _rotate_around_center(
        coords: np.ndarray, axis: str, angle: float, center: np.ndarray = None
    ) -> np.ndarray:
        """
        Rotate coordinates around a specified center point.

        :param coords: NumPy array of shape (N, 3) with valid coordinates
        :param axis: Axis to rotate around ('x', 'y', or 'z')
        :param angle: Angle in degrees
        :param center: Center point as np.array of shape (3,). If None, rotates around origin.
        :return: Rotated coordinates
        """
        if center is None:
            # Rotate around origin - use existing method
            return CoordinateMixin._rotate_valid_coordinates(coords, axis, angle)

        # Translate coordinates to center at origin
        translated_coords = coords - center

        # Rotate around origin
        rotated_coords = CoordinateMixin._rotate_valid_coordinates(
            translated_coords, axis, angle
        )

        # Translate back to original position
        return rotated_coords + center

    @staticmethod
    def build_square_array(
        x: float, y: float, x_width: float, y_width: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Build a NumPy array representing a square or rectangle defined by its bottom-left corner (x, y)
        and its width and height.

        Parameters
        ----------
        x : float
            The x-coordinate of the bottom-left corner of the square.
        y : float
            The y-coordinate of the bottom-left corner of the square.
        x_width : float
            The width of the square.
        y_width : float
            The height of the square.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            Tuple containing x and y coordinate arrays defining the square/rectangle
        """
        x_coords = np.array([x, x, x + x_width, x + x_width, x])
        y_coords = np.array([y, y + y_width, y + y_width, y, y])
        return x_coords, y_coords

    @staticmethod
    def build_circle_array(
        center_x: float, center_y: float, radius: float, num_points: int = 64, anticlockwise: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Build a NumPy array representing a circle defined by its center and radius.

        Parameters
        ----------
        center_x : float
            The x-coordinate of the circle center.
        center_y : float
            The y-coordinate of the circle center.
        radius : float
            The radius of the circle.
        num_points : int, optional
            Number of points to use for the circle approximation, by default 64
        anticlockwise : bool, optional
            If True, points are ordered anticlockwise; if False, clockwise, by default True

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            Tuple containing x and y coordinate arrays defining the circle
        """
        # Generate angles from 0 to 2π
        angles = np.linspace(0, 2 * np.pi, num_points + 1)
        
        # Reverse angles for clockwise direction
        if not anticlockwise:
            angles = angles[::-1]
        
        # Calculate x and y coordinates
        x_coords = center_x + radius * np.cos(angles)
        y_coords = center_y + radius * np.sin(angles)
        
        return x_coords, y_coords

    @staticmethod
    def order_coordinates_clockwise(df: pd.DataFrame, plane="xy") -> pd.DataFrame:

        axis_1 = plane[0]
        axis_2 = plane[1]

        cx = df[axis_1].mean()
        cy = df[axis_2].mean()

        angles = np.arctan2(df[axis_2] - cy, df[axis_1] - cx)

        df["angle"] = angles

        df_sorted = (
            df.sort_values(by="angle").drop(columns="angle").reset_index(drop=True)
        )

        return df_sorted

    @staticmethod
    def order_coordinates_clockwise_numpy(
        coords: np.ndarray, 
        plane: str = "xy"
    ) -> np.ndarray:
        """
        Order 3D coordinates in clockwise direction based on a specified plane.
        Handles multiple coordinate blocks separated by NaN rows.
        
        Parameters
        ----------
        coords : np.ndarray
            Array of 3D coordinates with shape (N, 3) where columns are [x, y, z].
            NaN rows indicate separations between coordinate blocks.
        plane : str, optional
            Plane to use for ordering ('xy', 'xz', 'yz'), by default 'xy'
            
        Returns
        -------
        np.ndarray
            Sorted coordinates array with same shape as input, with each block
            sorted clockwise and separated by NaN rows
            
        Raises
        ------
        ValueError
            If coords array doesn't have shape (N, 3) or plane is invalid
        """
        if len(coords.shape) != 2 or coords.shape[1] != 3:
            raise ValueError("coords must be a 2D array with 3 columns (x, y, z)")
        
        if coords.shape[0] < 2:
            return coords.copy()
        
        # Map plane string to column indices
        plane_mapping = {
            'xy': (0, 1),  # x, y columns
            'xz': (0, 2),  # x, z columns  
            'yz': (1, 2)   # y, z columns
        }
        
        if plane not in plane_mapping:
            raise ValueError(f"plane must be one of {list(plane_mapping.keys())}, got '{plane}'")
        
        # Check if we have NaN rows (multiple coordinate blocks)
        x_coords = coords[:, 0]
        x_is_nan = np.isnan(x_coords)
        
        if not np.any(x_is_nan):
            # Single block - use original logic
            return CoordinateMixin._sort_single_coordinate_block(coords, plane)
        
        # Multiple blocks - extract and sort each block
        segments = CoordinateMixin._extract_coordinate_blocks(coords)
        sorted_blocks = []
        
        for block in segments:
            if len(block) > 1:  # Only sort if block has more than 1 coordinate
                sorted_block = CoordinateMixin._sort_single_coordinate_block(block, plane)
                sorted_blocks.append(sorted_block)
            elif len(block) == 1:  # Single coordinate, keep as is
                sorted_blocks.append(block)
        
        return CoordinateMixin._concatenate_coordinate_blocks_with_nans(sorted_blocks)

    @staticmethod
    def concat_with_nan_separators(arrays: list) -> np.ndarray:
        """
        Efficiently concatenate numpy arrays with NaN separators.
        
        Parameters
        ----------
        arrays : list
            List of numpy arrays to concatenate
            
        Returns
        -------
        np.ndarray
            Concatenated array with NaN separators
        """
        if not arrays:
            return np.array([])
            
        if len(arrays) == 1:
            return arrays[0]
        
        # Calculate total size needed
        total_rows = sum(arr.shape[0] for arr in arrays) + len(arrays) - 1
        n_cols = arrays[0].shape[1]
        
        # Pre-allocate result array
        result = np.empty((total_rows, n_cols))
        
        current_row = 0
        for i, arr in enumerate(arrays):
            # Copy array data
            result[current_row:current_row + arr.shape[0]] = arr
            current_row += arr.shape[0]
            
            # Add NaN separator (except after last array)
            if i < len(arrays) - 1:
                result[current_row] = np.nan
                current_row += 1
        
        return result

    @staticmethod
    def _sort_single_coordinate_block(
        coords: np.ndarray, 
        plane: str
    ) -> np.ndarray:
        """
        Sort a single coordinate block clockwise.
        
        Parameters
        ----------
        coords : np.ndarray
            Array of 3D coordinates with shape (N, 3)
        plane : str
            Plane to use for ordering ('xy', 'xz', 'yz')
            
        Returns
        -------
        np.ndarray
            Sorted coordinates array
        """
        plane_mapping = {
            'xy': (0, 1),  # x, y columns
            'xz': (0, 2),  # x, z columns  
            'yz': (1, 2)   # y, z columns
        }
        
        axis_1_idx, axis_2_idx = plane_mapping[plane]
        
        # Extract the relevant coordinates for the specified plane
        axis_1_coords = coords[:, axis_1_idx]
        axis_2_coords = coords[:, axis_2_idx]
        
        # Calculate center point
        cx = np.nanmean(axis_1_coords)
        cy = np.nanmean(axis_2_coords)
        
        # Calculate angles from center to each point
        angles = np.arctan2(axis_2_coords - cy, axis_1_coords - cx)
        
        # Sort by angle to get clockwise ordering
        sorted_indices = np.argsort(angles)
        
        return coords[sorted_indices]

    @staticmethod
    def _extract_coordinate_blocks(coords: np.ndarray) -> list:
        """
        Extract coordinate blocks separated by NaN rows.
        
        Parameters
        ----------
        coords : np.ndarray
            Array of 3D coordinates with NaN row separators
            
        Returns
        -------
        list
            List of coordinate block arrays
        """
        blocks = []
        x_coords = coords[:, 0]
        x_is_nan = np.isnan(x_coords)
        nan_indices = np.where(x_is_nan)[0]
        start_idx = 0
        
        # Process each block between NaN rows
        for nan_idx in nan_indices:
            if nan_idx > start_idx:
                block = coords[start_idx:nan_idx]
                if len(block) > 0:
                    blocks.append(block)
            start_idx = nan_idx + 1
        
        # Handle the last block if it exists
        if start_idx < len(coords):
            block = coords[start_idx:]
            if len(block) > 0:
                blocks.append(block)
            
        return blocks

    @staticmethod
    def _concatenate_coordinate_blocks_with_nans(blocks: list) -> np.ndarray:
        """
        Concatenate coordinate blocks with NaN row separators.
        
        Parameters
        ----------
        blocks : list
            List of coordinate block arrays
            
        Returns
        -------
        np.ndarray
            Concatenated array with NaN separators
        """
        if not blocks:
            return np.array([]).reshape(0, 3)
        
        result_parts = []
        
        for i, block in enumerate(blocks):
            result_parts.append(block)
            
            # Add NaN separator between blocks (except for the last one)
            if i < len(blocks) - 1:
                nan_row = np.full((1, 3), np.nan)
                result_parts.append(nan_row)
        
        return np.vstack(result_parts)

    @staticmethod
    def _rotate_valid_coordinates(
        coords: np.ndarray, axis: str, angle: float
    ) -> np.ndarray:
        """
        Rotate coordinates without None values using rotation matrices.
        """
        angle_rad = np.radians(angle)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        if axis == "x":
            R = np.array([[1, 0, 0], [0, cos_a, -sin_a], [0, sin_a, cos_a]])
        elif axis == "y":
            R = np.array([[cos_a, 0, sin_a], [0, 1, 0], [-sin_a, 0, cos_a]])
        elif axis == "z":
            R = np.array([[cos_a, -sin_a, 0], [sin_a, cos_a, 0], [0, 0, 1]])
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'.")

        return coords @ R.T

    @staticmethod
    def _calculate_single_area(x: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate the area of a single closed shape using the shoelace formula.
        """
        if len(x) < 3 or len(y) < 3:
            return 0.0

        # Convert to float arrays to avoid object dtype issues
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        # Ensure the shape is closed by appending the first point to the end
        if (x[0], y[0]) != (x[-1], y[-1]):
            x = np.append(x, x[0])
            y = np.append(y, y[0])

        # Calculate the area using the shoelace formula
        area = 0.5 * np.abs(np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:]))

        return float(area)

    @staticmethod
    def get_area_from_points(x: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate the area of a closed shape defined by the coordinates in x and y using the shoelace formula.
        Can handle multiple shapes separated by None values.
        """
        # Convert to numpy arrays and handle object dtype
        x = np.asarray(x)
        y = np.asarray(y)

        # Check if we have None values (multiple shapes)
        x_is_none = pd.isna(x) if hasattr(pd, "isna") else (x == None)

        if np.any(x_is_none):
            total_area = 0.0

            # Find None indices to split the shapes
            none_indices = np.where(x_is_none)[0]
            start_idx = 0

            # Process each shape segment
            for none_idx in none_indices:
                if none_idx > start_idx:
                    # Extract segment coordinates
                    segment_x = x[start_idx:none_idx]
                    segment_y = y[start_idx:none_idx]

                    # Calculate area for this segment if it has enough points
                    if len(segment_x) >= 3:
                        area = CoordinateMixin._calculate_single_area(
                            segment_x, segment_y
                        )
                        total_area += area

                start_idx = none_idx + 1

            # Handle the last segment if it exists
            if start_idx < len(x):
                segment_x = x[start_idx:]
                segment_y = y[start_idx:]
                if len(segment_x) >= 3:
                    area = CoordinateMixin._calculate_single_area(segment_x, segment_y)
                    total_area += area

            return total_area

        else:
            # Single shape - use original logic
            return CoordinateMixin._calculate_single_area(x, y)

    @staticmethod
    def extrude_footprint(
        x: np.ndarray, 
        y: np.ndarray, 
        datum: np.ndarray, 
        thickness: float
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Extrude a 2D footprint to 3D, handling both single and multi-segment polygons.
        
        Parameters
        ----------
        x : np.ndarray
            Array of x coordinates. NaN values indicate segment separators.
        y : np.ndarray
            Array of y coordinates. NaN values indicate segment separators.
        datum : np.ndarray
            Datum point for extrusion (shape (3,))
        thickness : float
            Thickness of the extrusion
            
        Returns
        -------
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
            Arrays of x, y, z coordinates and side labels, with NaN separators between segments
        """
        if not np.isnan(x).any() and not np.isnan(y).any():
            return CoordinateMixin._extrude_single_footprint(x, y, datum, thickness)
        
        # Process segmented coordinates
        segments = CoordinateMixin._extract_coordinate_segments(x, y)
        extruded_sections = []
        
        for segment_x, segment_y in segments:
            if len(segment_x) > 0 and not np.all(np.isnan(segment_x)):
                result = CoordinateMixin._extrude_single_footprint(
                    segment_x, segment_y, datum, thickness
                )
                extruded_sections.append(result)
        
        return CoordinateMixin._concatenate_with_separators(extruded_sections)

    @staticmethod
    def _extract_coordinate_segments(x: np.ndarray, y: np.ndarray, unify_xy: bool = False) -> list:
        """
        Extract coordinate segments separated by NaN values.
        
        Parameters
        ----------
        x : np.ndarray
            X coordinates with NaN separators
        y : np.ndarray
            Y coordinates with NaN separators
            
        Returns
        -------
        list
            List of (segment_x, segment_y) tuples
        """
        segments = []
        x_is_nan = np.isnan(x)
        nan_indices = np.where(x_is_nan)[0]
        start_idx = 0
        
        # Process each segment between NaN values
        for nan_idx in nan_indices:
            if nan_idx > start_idx:
                segments.append((x[start_idx:nan_idx], y[start_idx:nan_idx]))
            start_idx = nan_idx + 1
        
        # Handle the last segment if it exists
        if start_idx < len(x):
            segments.append((x[start_idx:], y[start_idx:]))
            
        if unify_xy:
            unified_segments = []
            for i in range(len(segments)):
                segment_x, segment_y = segments[i]
                xy_array = np.column_stack((segment_x, segment_y))
                unified_segments.append(xy_array)
            return np.array(unified_segments)
        else:
            return segments

    @staticmethod
    def _concatenate_with_separators(sections: list) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Concatenate extruded sections with NaN separators.
        
        Parameters
        ----------
        sections : list
            List of (x_ext, y_ext, z_ext, side_ext) tuples
            
        Returns
        -------
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
            Concatenated arrays with NaN separators
        """
        if not sections:
            return np.array([]), np.array([]), np.array([]), np.array([])
        
        x_parts, y_parts, z_parts, side_parts = [], [], [], []
        
        for i, (x_ext, y_ext, z_ext, side_ext) in enumerate(sections):
            x_parts.append(x_ext)
            y_parts.append(y_ext)
            z_parts.append(z_ext)
            side_parts.append(side_ext)
            
            # Add NaN separators between segments (except for the last one)
            if i < len(sections) - 1:
                x_parts.append(np.array([np.nan]))
                y_parts.append(np.array([np.nan]))
                z_parts.append(np.array([np.nan]))
                side_parts.append(np.array([None], dtype=object))
        
        return (
            np.concatenate(x_parts),
            np.concatenate(y_parts), 
            np.concatenate(z_parts),
            np.concatenate(side_parts)
        )

    @staticmethod
    def _extrude_single_footprint(
        x: np.ndarray, 
        y: np.ndarray, 
        datum: np.ndarray, 
        thickness: float
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Extrude the 2D footprint to 3D and label each point with its side ('a' or 'b'), with 'a' being the top side and 'b' the bottom side.

        Parameters
        ----------
        x : np.ndarray
            Array of x coordinates (length N)
        y : np.ndarray
            Array of y coordinates (length N)
        datum : np.ndarray
            Datum point for extrusion (shape (3,))
        thickness : float
            Thickness of the extrusion

        Returns
        -------
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
            Arrays of x, y, z, and side for both A and B sides (each of length 2N)
        """
        z_a = datum[2] + thickness / 2
        z_b = datum[2] - thickness / 2

        # Repeat x and y coordinates for both sides
        x_full = np.concatenate([x, x])
        y_full = np.concatenate([y, y])
        z_full = np.concatenate([np.full_like(x, z_a), np.full_like(x, z_b)])
        side_full = np.array(["a"] * len(x) + ["b"] * len(x))

        return x_full, y_full, z_full, side_full

    @staticmethod
    def get_coordinate_intersection(
            coords1: np.ndarray,
            coords2: np.ndarray
    ) -> float:
        """Calculate the intersection area between two sets of coordinates"""
        polygon1 = Polygon(coords1)
        polygon2 = Polygon(coords2)
        intersection = polygon1.intersection(polygon2)
        return intersection.area

    @staticmethod
    def insert_gaps_with_nans(
        data: np.ndarray, 
        column_index: int, 
        tolerance_multiplier: float = 2.0
    ) -> np.ndarray:
        """
        Insert rows of NaNs when gaps in a specified column exceed a tolerance threshold.
        
        Parameters
        ----------
        data : np.ndarray
            Input array with shape (N, M) where N is number of rows and M is number of columns
        column_index : int
            Index of the column to analyze for gaps (0-based indexing)
        tolerance_multiplier : float, optional
            Multiplier for average gap to determine tolerance threshold, by default 2.0
            
        Returns
        -------
        np.ndarray
            Array with NaN rows inserted where gaps exceed the tolerance
            
        Raises
        ------
        ValueError
            If column_index is out of bounds for the array
        IndexError
            If data array is empty or has insufficient dimensions
            
        Examples
        --------
        >>> data = np.array([[1, 10], [2, 20], [5, 50], [6, 60]])
        >>> result = CoordinateMixin.insert_gaps_with_nans(data, column_index=0)
        >>> # Will insert NaN row between [2, 20] and [5, 50] if gap of 3 exceeds tolerance
        """
        if data.size == 0:
            return data.copy()
            
        if len(data.shape) != 2:
            raise ValueError("Input array must be 2-dimensional")
            
        if column_index < 0 or column_index >= data.shape[1]:
            raise ValueError(f"column_index {column_index} is out of bounds for array with {data.shape[1]} columns")
        
        if data.shape[0] < 2:
            return data.copy()
        
        # Extract the column values
        column_values = data[:, column_index]
        
        # Remove NaN values for gap calculation
        valid_values = column_values[~np.isnan(column_values)]
        
        if len(valid_values) < 2:
            return data.copy()
        
        # Calculate gaps between consecutive values
        gaps = np.diff(valid_values)
        
        # Calculate average gap and tolerance
        average_gap = np.mean(np.abs(gaps))
        tolerance = average_gap * tolerance_multiplier
        
        # Find positions where gaps exceed tolerance in original array
        result_rows = []
        
        for i in range(len(data)):
            result_rows.append(data[i])
            
            # Check if we should insert a gap after this row
            if i < len(data) - 1:
                current_val = column_values[i]
                next_val = column_values[i + 1]
                
                # Only check gap if both values are not NaN
                if not (np.isnan(current_val) or np.isnan(next_val)):
                    gap = abs(next_val - current_val)
                    if gap > tolerance:
                        # Insert a row of NaNs
                        nan_row = np.full(data.shape[1], np.nan)
                        result_rows.append(nan_row)
        
        return np.array(result_rows)

    @staticmethod
    def remove_skip_coat_area(
        x_coords: np.ndarray,
        y_coords: np.ndarray,
        weld_tab_positions: np.ndarray,
        skip_coat_width: float,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Remove skip coat areas around weld tab positions from coordinates.

        Parameters
        ----------
        x_coords : np.ndarray
            Array of x coordinates defining the boundary
        y_coords : np.ndarray
            Array of y coordinates defining the boundary
        weld_tab_positions : np.ndarray
            Array of x positions where weld tabs are located
        skip_coat_width : float
            Width of the skip coat area around each weld tab

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            Modified x and y coordinate arrays with np.nan separators between segments
        """
        if len(x_coords) == 0 or len(y_coords) == 0:
            return np.array([], dtype=float), np.array([], dtype=float)

        x_min, x_max = np.min(x_coords), np.max(x_coords)
        y_min, y_max = np.min(y_coords), np.max(y_coords)

        # Filter weld tab positions to only include those within bounds
        valid_positions = weld_tab_positions[
            (weld_tab_positions + skip_coat_width >= x_min)
            & (weld_tab_positions - skip_coat_width <= x_max)
        ]

        # If no valid positions, return original rectangle
        if len(valid_positions) == 0:
            rect_x = [x_min, x_max, x_max, x_min, x_min]
            rect_y = [y_min, y_min, y_max, y_max, y_min]
            return np.array(rect_x, dtype=float), np.array(rect_y, dtype=float)

        # Sort weld tab cut positions
        cuts = np.sort(valid_positions)
        half_width = skip_coat_width / 2

        # Build kept horizontal segments by removing [cut - half, cut + half] around each cut
        segments = []
        start = x_min

        for cut in cuts:
            end = cut - half_width
            if end > start:
                segments.append((start, end))
            start = cut + half_width

        # Add final segment if there's remaining space
        if start < x_max:
            segments.append((start, x_max))

        # Build rectangles for each kept segment with np.nan separators
        x_result = []
        y_result = []

        for i, (segment_start, segment_end) in enumerate(segments):
            # Create rectangle coordinates: bottom-left -> bottom-right -> top-right -> top-left -> close
            rect_x = [
                segment_start,
                segment_end,
                segment_end,
                segment_start,
                segment_start,
            ]
            rect_y = [y_min, y_min, y_max, y_max, y_min]

            x_result.extend(rect_x)
            y_result.extend(rect_y)

            # Add np.nan separator (except for the last segment)
            if i < len(segments) - 1:  # Fixed: use index comparison
                x_result.append(np.nan)
                y_result.append(np.nan)

        return np.array(x_result, dtype=float), np.array(y_result, dtype=float)


