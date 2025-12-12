import unittest
import plotly.graph_objects as go
from steer_core.Mixins.TypeChecker import ValidationMixin


class TestValidationMixin(unittest.TestCase):
    """Test cases for ValidationMixin validation methods."""

    def test_validate_plotly_trace_with_valid_traces(self):
        """Test validate_plotly_trace with valid Plotly trace objects."""
        # Test various Plotly trace types
        valid_traces = [
            go.Scatter(x=[1, 2, 3], y=[1, 2, 3]),
            go.Bar(x=['A', 'B', 'C'], y=[1, 2, 3]),
            go.Histogram(x=[1, 2, 3, 4, 5]),
            go.Box(y=[1, 2, 3, 4, 5]),
            go.Heatmap(z=[[1, 2], [3, 4]]),
            go.Pie(values=[1, 2, 3], labels=['A', 'B', 'C']),
            go.Scatter3d(x=[1, 2], y=[1, 2], z=[1, 2]),
        ]
        
        for trace in valid_traces:
            with self.subTest(trace=type(trace).__name__):
                result = ValidationMixin.validate_plotly_trace(trace, "test_trace")
                self.assertTrue(result, f"Should return True for {type(trace).__name__}")

    def test_validate_plotly_trace_with_invalid_objects(self):
        """Test validate_plotly_trace with non-Plotly objects."""
        invalid_objects = [
            "string",
            123,
            [1, 2, 3],
            {"key": "value"},
            None,
            object(),
        ]
        
        for obj in invalid_objects:
            with self.subTest(obj=type(obj).__name__):
                # Should return False for non-Plotly objects
                result = ValidationMixin.validate_plotly_trace(obj, "test_object")
                self.assertFalse(result, f"Should return False for {type(obj).__name__}")

    def test_validate_plotly_trace_with_objects_without_module(self):
        """Test validate_plotly_trace with objects that don't have __module__ attribute."""
        # Create an object without __module__ using a custom class
        class MockObjectNoModule:
            def __getattribute__(self, name):
                if name == '__module__':
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '__module__'")
                return super().__getattribute__(name)
        
        mock_obj = MockObjectNoModule()
        
        # Verify that hasattr returns False for __module__
        self.assertFalse(hasattr(mock_obj, '__module__'), "Mock object should not have __module__ attribute")
        
        result = ValidationMixin.validate_plotly_trace(mock_obj, "mock_object")
        self.assertFalse(result, "Should return False for objects without __module__")

    def test_validate_plotly_trace_with_wrong_module(self):
        """Test validate_plotly_trace with objects from different modules."""
        import pandas as pd
        import numpy as np
        
        # Test with objects from other modules
        other_module_objects = [
            pd.DataFrame({'x': [1, 2, 3]}),
            np.array([1, 2, 3]),
        ]
        
        for obj in other_module_objects:
            with self.subTest(obj=type(obj).__name__):
                result = ValidationMixin.validate_plotly_trace(obj, "other_module_object")
                self.assertFalse(result, f"Should return False for {type(obj).__name__} from different module")

    def test_validate_plotly_trace_edge_cases(self):
        """Test validate_plotly_trace with edge cases."""
        # Test with object that has __module__ but it's None
        class MockObjectWithNoneModule:
            __module__ = None
        
        mock_obj = MockObjectWithNoneModule()
        result = ValidationMixin.validate_plotly_trace(mock_obj, "mock_object_none_module")
        self.assertFalse(result, "Should return False when __module__ is None")
        
        # Test with object that has __module__ but it's empty string
        class MockObjectWithEmptyModule:
            __module__ = ""
        
        mock_obj_empty = MockObjectWithEmptyModule()
        result = ValidationMixin.validate_plotly_trace(mock_obj_empty, "mock_object_empty_module")
        self.assertFalse(result, "Should return False when __module__ is empty string")


if __name__ == '__main__':
    unittest.main()
