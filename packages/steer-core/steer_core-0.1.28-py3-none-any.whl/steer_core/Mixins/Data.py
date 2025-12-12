from copy import deepcopy
import numpy as np
from scipy.interpolate import PchipInterpolator


class DataMixin:
    """
    A mixin class to handle data processing and validation for electrode materials.
    Provides methods to calculate properties, check curve directions, and process half-cell curves.
    """

    @staticmethod
    def enforce_monotonicity(array: np.ndarray) -> np.ndarray:
        """
        Enforces a monotonic version of the input array.
        If the array is not monotonic, it is smoothed using cumulative max/min.
        """
        x = np.arange(len(array))
        diff = np.diff(array)

        if np.all(diff >= 0):
            return array  # Already monotonic increasing

        if np.all(diff <= 0):
            return array  # Already monotonic decreasing, reverse it

        # Determine general trend (ascending or descending)
        ascending = array[-1] >= array[0]

        # Sort by x so that PCHIP works (PCHIP requires increasing x)
        # We'll smooth the array using PCHIP, then enforce monotonicity
        interpolator = PchipInterpolator(x, array, extrapolate=False)
        new_array = interpolator(x)

        # Enforce strict monotonicity post-smoothing
        if ascending:
            new_array = np.maximum.accumulate(new_array)
        else:
            new_array = np.minimum.accumulate(new_array)

        return new_array

    @staticmethod
    def sum_breakdowns(components, breakdown_type: str):
        """
        Aggregate breakdown dictionaries across multiple components.
        If a component doesn't have the specified breakdown, use its fallback attribute instead.

        Parameters
        ----------
        components : list
            List of component objects
        breakdown_type : str, optional
            Type of breakdown to aggregate ('mass', 'cost', etc.), by default 'mass'
            
        Returns
        -------
        dict or float
            Aggregated breakdown dictionary with summed values maintaining structure,
            or simple float sum if no components have the specified breakdown
        """
        def add_dicts(dict1, dict2):
            """Recursively add two dictionaries with matching structure."""
            result = dict1.copy()
            
            for key, value in dict2.items():
                if key in result:
                    if isinstance(result[key], dict) and isinstance(value, dict):
                        result[key] = add_dicts(result[key], value)
                    elif isinstance(result[key], (int, float)) and isinstance(value, (int, float)):
                        result[key] += value
                else:
                    result[key] = value
            
            return result
        
        breakdown_attr = f'_{breakdown_type}_breakdown'
        fallback_attr = f'_{breakdown_type}'
        
        aggregated_breakdown = {}
        simple_sum = 0
        has_breakdown_components = False
        
        for component in components:
            if hasattr(component, breakdown_attr):
                breakdown_value = getattr(component, breakdown_attr)
                if breakdown_value is not None:
                    has_breakdown_components = True
                    if not aggregated_breakdown:
                        # Initialize with first component's breakdown
                        aggregated_breakdown = deepcopy(breakdown_value)
                    else:
                        # Add subsequent breakdowns
                        aggregated_breakdown = add_dicts(aggregated_breakdown, breakdown_value)
            elif hasattr(component, fallback_attr):
                # Component only has fallback attribute
                fallback_value = getattr(component, fallback_attr)
                if fallback_value is not None:
                    simple_sum += fallback_value
        
        # If we have breakdown components, add the simple sum to the breakdown
        if has_breakdown_components:
            if simple_sum > 0:
                total_key = f'total_{breakdown_type}'
                if total_key in aggregated_breakdown:
                    aggregated_breakdown[total_key] += simple_sum
                else:
                    aggregated_breakdown[total_key] = simple_sum
            return aggregated_breakdown
        else:
            # No breakdown components, return simple sum
            return simple_sum
        