import plotly.graph_objects as go
from typing import Dict, Any, Tuple, List, Union
from steer_core.Mixins.Coordinates import CoordinateMixin


class PlotterMixin:
    
    SCATTER_X_AXIS = dict(
        showgrid=True,
        gridcolor="rgba(128, 128, 128, 0.2)",
        gridwidth=1,
        zeroline=True,
        zerolinecolor="rgba(0, 0, 0, 0.5)",
        zerolinewidth=1,
    )

    SCATTER_Y_AXIS = dict(
        showgrid=True,
        gridcolor="rgba(128, 128, 128, 0.2)",
        gridwidth=1,
        zeroline=True,
        zerolinecolor="rgba(0, 0, 0, 0.5)",
        zerolinewidth=1,
    )

    SCHEMATIC_X_AXIS = dict(
        zeroline=False,
        scaleanchor="y",
        title="X (mm)"
    )

    SCHEMATIC_Y_AXIS = dict(
        zeroline=False,
        title="Y (mm)"
    )

    SCHEMATIC_Z_AXIS = dict(
        zeroline=False,
        title="Z (mm)"
    )

    BOTTOM_LEGEND = dict(
        orientation="h",
        yanchor="top",
        y=-0.3,
        xanchor="center",
        x=0.5,
    )

    @staticmethod
    def create_component_trace(
            components, 
            coord_attr, 
            name, 
            line_width, 
            color_func, 
            unit_conversion_factor,
            order_clockwise: str = None
            ):
        """
        Create a single trace for a component or group of components with NaN separators.
        
        Parameters
        ----------
        components : list or object
            Single component or list of components to process
        coord_attr : str
            Attribute path for coordinates (e.g., '_a_side_coating_coordinates')
        name : str
            Name for the trace
        line_width : float
            Width of the trace line
        color_func : callable
            Function to get color from component
        unit_conversion_factor : float
            Factor to convert coordinates to desired units
        order_clockwise : str or None, optional
            Plane for clockwise ordering ('xy', 'xz', 'yz') or None to disable, by default None
            
        Returns
        -------
        go.Scatter or None
            Plotly scatter trace or None if no valid coordinates
        """
        # Convert single component to list for uniform processing
        if not isinstance(components, list):
            components = [components]
            
        if not components:
            return None
            
        # Extract coordinates using nested getattr for dot notation
        coord_arrays = []
        for component in components:
            coords = component
            # Handle nested attributes like '_current_collector._body_coordinates'
            for attr_part in coord_attr.split('.'):
                coords = getattr(coords, attr_part)
                
            if coords is not None and len(coords) > 0:
                coord_arrays.append(coords)

        if not coord_arrays:
            return None
        
        # Concatenate coordinates with NaN separators
        combined_coords = CoordinateMixin.concat_with_nan_separators(coord_arrays)
        
        # Order coordinates clockwise if requested
        if order_clockwise is not None:
            combined_coords = CoordinateMixin.order_coordinates_clockwise_numpy(combined_coords, plane=order_clockwise)
        
        # Convert to mm and extract y,z coordinates directly (avoid DataFrame overhead)
        y_coords = combined_coords[:, 1] * unit_conversion_factor
        z_coords = combined_coords[:, 2] * unit_conversion_factor
        
        # Create trace
        return go.Scatter(
            x=y_coords,
            y=z_coords,
            mode="lines",
            name=name,
            line={'width': line_width, 'color': "black"},
            fill="toself",
            fillcolor=color_func(components[0]),
            legendgroup=name,
            showlegend=True,
        )

    @staticmethod
    def plot_breakdown_sunburst(
        breakdown_dict: Dict[str, Any],
        title: str = "Breakdown",
        root_label: str = "Total",
        unit: str = "",
        **kwargs,
    ) -> go.Figure:
        """
        Create a sunburst plot for any generic nested breakdown dictionary.

        Parameters
        ----------
        breakdown_dict : Dict[str, Any]
            Nested dictionary where values can be either numbers or nested dictionaries.
            Each nesting level becomes a ring in the sunburst plot.
        title : str, optional
            Title for the plot. Defaults to "Breakdown".
        root_label : str, optional
            Label for the root node. Defaults to "Total".
        unit : str, optional
            Unit string to display in hover text (e.g., "g", "kg", "%"). Defaults to "".

        Returns
        -------
        go.Figure
            Plotly sunburst figure
        """

        def _flatten_breakdown_values(data: Dict[str, Any]) -> List[float]:
            """Recursively flatten all numeric values from nested breakdown dictionary"""
            values = []
            for value in data.values():
                if isinstance(value, dict):
                    values.extend(_flatten_breakdown_values(value))
                elif isinstance(value, (int, float)):
                    values.append(float(value))
            return values

        def _calculate_subtotal(data: Dict[str, Any]) -> float:
            """Calculate the total value for a dictionary (sum of all nested numeric values)"""
            total = 0.0
            for value in data.values():
                if isinstance(value, dict):
                    total += _calculate_subtotal(value)
                elif isinstance(value, (int, float)):
                    total += float(value)
            return total

        def _prepare_sunburst_data(
            data: Dict[str, Any], parent_id: str = "", current_path: str = ""
        ) -> Tuple[List[str], List[str], List[str], List[float]]:
            """Recursively prepare data for sunburst plot with proper hierarchy"""
            ids = []
            labels = []
            parents = []
            values = []

            for key, value in data.items():
                # Create unique ID for this node
                node_id = f"{current_path}/{key}" if current_path else key

                ids.append(node_id)
                labels.append(key)
                parents.append(parent_id)

                if isinstance(value, dict):
                    # This is a nested dictionary - calculate its total value
                    subtotal = _calculate_subtotal(value)
                    values.append(subtotal)

                    # Recursively process nested dictionary
                    (
                        nested_ids,
                        nested_labels,
                        nested_parents,
                        nested_values,
                    ) = _prepare_sunburst_data(
                        value, parent_id=node_id, current_path=node_id
                    )

                    # Add nested data to our lists
                    ids.extend(nested_ids)
                    labels.extend(nested_labels)
                    parents.extend(nested_parents)
                    values.extend(nested_values)

                elif isinstance(value, (int, float)):
                    # This is a leaf node with a numeric value
                    values.append(float(value))

            return ids, labels, parents, values

        # Calculate total value for root node
        total_value = _calculate_subtotal(breakdown_dict)

        # Prepare hierarchical data starting with root
        ids, labels, parents, values = _prepare_sunburst_data(
            breakdown_dict, parent_id=""
        )

        # Add root node at the beginning
        ids.insert(0, root_label)
        labels.insert(0, root_label)
        parents.insert(0, "")
        values.insert(0, total_value)

        # Update parent references to point to root
        for i in range(1, len(parents)):
            if parents[i] == "":
                parents[i] = root_label

        # Create custom hover text with percentages
        hover_text = []
        for i, (label, value) in enumerate(zip(labels, values)):
            if label == root_label:
                unit_str = f" {unit}" if unit else ""
                hover_text.append(f"<b>{root_label}</b><br>{value:.2f}{unit_str}")
            else:
                percentage = (value / total_value * 100) if total_value > 0 else 0
                unit_str = f" {unit}" if unit else ""
                hover_text.append(
                    f"<b>{label}</b><br>{value:.2f}{unit_str}<br>{percentage:.1f}% of total"
                )

        # Create the sunburst plot
        fig = go.Figure(
            go.Sunburst(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                branchvalues="total",
                hovertemplate="%{customdata}<extra></extra>",
                customdata=hover_text,
            )
        )

        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)), font_size=12, **kwargs
        )

        return fig


    
