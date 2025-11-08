"""
Cell management functions for the Data Analysis Notebook
Handles adding, deleting, and executing notebook cells
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
import traceback
from io import StringIO


def add_cell(content="# Write your code here\n", position=None):
    """Add a new cell to the notebook"""
    new_cell = {
        'id': st.session_state.cell_counter,
        'type': 'code',
        'content': content,
        'output': None,
        'executed': False,
        'execution_count': None,
        'error': None,
        'result': None,  # Store the last expression result
        'figure': None,  # Store plotly figures
        'dataframe': None,  # Store DataFrame results
        'series': None  # Store Series results
    }
    if position is None:
        st.session_state.cells.append(new_cell)
    else:
        st.session_state.cells.insert(position, new_cell)
    st.session_state.cell_counter += 1


def delete_cell(cell_id):
    """Delete a cell from the notebook"""
    st.session_state.cells = [c for c in st.session_state.cells if c['id'] != cell_id]


def execute_cell(cell_id, code):
    """Execute cell code with improved output capture and result storage"""
    for cell in st.session_state.cells:
        if cell['id'] == cell_id:
            try:
                # Increment execution count
                st.session_state.execution_count += 1
                cell['execution_count'] = st.session_state.execution_count
                
                # Capture stdout and stderr
                output_buffer = StringIO()
                error_buffer = StringIO()
                
                # Create execution context with all necessary imports
                exec_globals = {
                    '__builtins__': __builtins__,
                    'pd': pd,
                    'np': np,
                    'px': px,
                    'go': go,
                    'st': st,
                    'df': st.session_state.df,
                    **st.session_state.variables
                }
                
                # Custom print function that captures output
                def custom_print(*args, **kwargs):
                    print(*args, file=output_buffer, **kwargs)
                
                exec_globals['print'] = custom_print
                
                # Redirect stdout and stderr
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = output_buffer
                sys.stderr = error_buffer
                
                try:
                    # Try to execute as expression first (for single-line results)
                    try:
                        result = eval(code, exec_globals)
                        if result is not None:
                            # Store result based on type
                            if isinstance(result, pd.DataFrame):
                                cell['dataframe'] = result
                            elif isinstance(result, pd.Series):
                                cell['series'] = result
                            elif isinstance(result, go.Figure) or hasattr(result, '_grid_ref') or (hasattr(result, '__class__') and 'plotly' in str(type(result))):
                                cell['figure'] = result
                            else:
                                cell['result'] = result
                    except:
                        # Not an expression, execute as statements
                        exec(code, exec_globals)
                finally:
                    # Restore stdout/stderr
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
                
                # Update dataframe if modified
                if 'df' in exec_globals:
                    st.session_state.df = exec_globals['df']
                
                # Check for figures in variables (common pattern: fig = px.bar(...))
                # Only store if not already displayed via st.plotly_chart
                if 'st.plotly_chart' not in code:
                    for key, value in exec_globals.items():
                        if isinstance(value, go.Figure):
                            cell['figure'] = value
                            break
                        elif hasattr(value, '_grid_ref') or (hasattr(value, '__class__') and 'plotly' in str(type(value))):
                            cell['figure'] = value
                            break
                
                # Save variables (excluding built-ins and imports)
                excluded_keys = {'pd', 'np', 'px', 'go', 'st', '__builtins__', 'print', '__name__', '__doc__', '__package__', '__loader__', '__spec__', '__annotations__', '__file__', '__cached__'}
                for key, value in exec_globals.items():
                    if key not in excluded_keys and not key.startswith('_'):
                        st.session_state.variables[key] = value
                
                # Get captured output
                captured_output = output_buffer.getvalue()
                captured_errors = error_buffer.getvalue()
                
                # Combine output
                full_output = captured_output + captured_errors if captured_errors else captured_output
                cell['output'] = full_output if full_output else None
                cell['executed'] = True
                cell['error'] = None
                
                return True, None
                
            except Exception as e:
                # Get full traceback for better error messages
                error_traceback = traceback.format_exc()
                cell['output'] = None
                cell['error'] = str(e)
                cell['error_traceback'] = error_traceback
                cell['executed'] = False
                cell['execution_count'] = None
                return False, str(e)
    return False, "Cell not found"

