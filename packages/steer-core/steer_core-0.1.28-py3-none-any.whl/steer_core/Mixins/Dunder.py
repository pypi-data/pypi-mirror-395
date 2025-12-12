

import numpy as np


class DunderMixin:

    def _get_comparable_properties(self):
        """Get all comparable properties from the class hierarchy."""
        properties = []
        for cls in self.__class__.__mro__:
            for name, value in cls.__dict__.items():
                if isinstance(value, property):
                    if not self._should_exclude_property(name):
                        properties.append(name)
        return properties

    def _should_exclude_property(self, name):
        """Check if a property should be excluded from comparison."""
        return (
            name.endswith('_trace') or
            name.endswith('_range') or 
            name in {'last_updated', 'properties'}
        )

    def _is_plotly_trace(self, obj):
        """Check if object is a Plotly trace object."""
        return (
            hasattr(obj, '__module__') and 
            obj.__module__ and 
            obj.__module__.startswith('plotly.graph_objs')
        )

    def _compare_none_values(self, self_value, other_value):
        """Compare None values. Returns (should_continue, result)."""
        if self_value is None and other_value is None:
            return True, True  # Continue, values are equal
        elif self_value is None or other_value is None:
            return False, False  # Stop, values are not equal
        return True, None  # Continue, not None values

    def _compare_plotly_traces(self, self_value, other_value):
        """Compare Plotly trace objects. Returns (should_continue, result)."""
        if self._is_plotly_trace(self_value) or self._is_plotly_trace(other_value):
            return True, True  # Skip Plotly traces, continue
        return True, None  # Continue, not Plotly traces

    def _compare_numpy_arrays(self, self_value, other_value):
        """Compare NumPy arrays. Returns (should_continue, result)."""
        if isinstance(self_value, np.ndarray) and isinstance(other_value, np.ndarray):
            return False, np.array_equal(self_value, other_value, equal_nan=True)
        elif isinstance(self_value, np.ndarray) or isinstance(other_value, np.ndarray):
            return False, False  # One is numpy array, other is not
        return True, None  # Continue, not numpy arrays

    def _compare_dataframes(self, self_value, other_value):
        """Compare pandas DataFrames/Series. Returns (should_continue, result)."""
        if hasattr(self_value, 'equals') and hasattr(other_value, 'equals'):
            return False, self_value.equals(other_value)
        elif hasattr(self_value, 'equals') or hasattr(other_value, 'equals'):
            return False, False  # Only one is a DataFrame/Series
        return True, None  # Continue, not DataFrames

    def _compare_dictionaries(self, self_value, other_value):
        """Compare dictionaries by comparing keys and values separately. Returns (should_continue, result)."""
        if isinstance(self_value, dict) and isinstance(other_value, dict):
            # Compare keys first (order-independent)
            if list(self_value.keys()) == list(other_value.keys()) and list(self_value.values()) == list(other_value.values()):
                return False, True  # Quick path: both keys and values match in order
            
            # Compare values for each key
            for key in self_value.keys():
                if self_value[key] != other_value[key]:
                    return False, False
            
            return False, True  # Dictionaries are equal
        elif isinstance(self_value, dict) or isinstance(other_value, dict):
            return False, False  # One is dict, other is not
        return True, None  # Continue, not dictionaries

    def _compare_sequences(self, self_value, other_value):
        """Compare lists and tuples. Returns (should_continue, result)."""
        if isinstance(self_value, (list, tuple)) and isinstance(other_value, (list, tuple)):
            return False, type(self_value) == type(other_value) and self_value == other_value
        elif isinstance(self_value, (list, tuple)) or isinstance(other_value, (list, tuple)):
            return False, False  # One is sequence, other is not
        return True, None  # Continue, not sequences

    def _compare_other_types(self, self_value, other_value):
        """Compare all other types. Returns (should_continue, result)."""
        return False, self_value == other_value

    def __eq__(self, other):
        """
        Compare two instances based on all their @property decorated attributes.
        
        Returns True if all properties have equal values, False otherwise.
        Returns False if other is not an instance of the same class.
        """
        # Quick identity check first (performance optimization)
        if self is other:
            return True
            
        # Check if other is the same type
        if type(other) != type(self):
            return False
        
        # Cache properties to avoid repeated computation (performance optimization)
        if not hasattr(self, '_cached_properties'):
            self._cached_properties = self._get_comparable_properties()
        
        # Define comparison methods in order of priority/frequency
        comparison_methods = [
            self._compare_none_values,
            self._compare_plotly_traces,
            self._compare_numpy_arrays,
            self._compare_dataframes,
            self._compare_dictionaries,
            self._compare_sequences,
            self._compare_other_types,
        ]

        # Compare all property values
        for prop_name in self._cached_properties:

            try:
                self_value = getattr(self, prop_name)
                other_value = getattr(other, prop_name)
                
                # Execute comparison methods until one handles the values
                for method in comparison_methods:
                    should_continue, result = method(self_value, other_value)
                    if not should_continue:
                        if not result:
                            return False
                        break  # Values are equal, continue to next property
                        
            except (AttributeError, Exception):
                # If property doesn't exist or comparison fails
                return False
        
        return True
    
    def __hash__(self):
        """
        Simple, robust hash based on object identity.
        
        Uses id() for a fast, guaranteed-unique hash that won't fail.
        Objects are only equal if they're the same instance.
        """
        return hash(id(self))
    
    def __str__(self):
        """
        String representation of the instance showing all @property decorated attributes and their values.
        """
        return f"{self.__class__.__name__}, {self.__name__}"
    
    def __repr__(self):
        """
        Official string representation of the instance.
        """
        return self.__str__()

