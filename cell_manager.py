import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
import traceback
from io import StringIO


def add_cell(content="# Write your code here\n", position=None):
    new_cell = {
        'id': st.session_state.cell_counter,
        'type': 'code',
        'content': content,
        'output': None,
        'executed': False,
        'execution_count': None,
        'error': None,
        'result': None, 
        'figure': None,  
        'dataframe': None,  
        'series': None  
    }
    if position is None:
        st.session_state.cells.append(new_cell)
    else:
        st.session_state.cells.insert(position, new_cell)
    st.session_state.cell_counter += 1


def delete_cell(cell_id):
    st.session_state.cells = [c for c in st.session_state.cells if c['id'] != cell_id]


def execute_cell(cell_id, code):
    for cell in st.session_state.cells:
        if cell['id'] == cell_id:
            try:
                st.session_state.execution_count += 1
                cell['execution_count'] = st.session_state.execution_count
                
                output_buffer = StringIO()
                error_buffer = StringIO()
                
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
                
                def custom_print(*args, **kwargs):
                    print(*args, file=output_buffer, **kwargs)
                
                exec_globals['print'] = custom_print
                
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = output_buffer
                sys.stderr = error_buffer
                
                # Check if code uses st.plotly_chart
                uses_streamlit_chart = 'st.plotly_chart' in code
                
                try:
                    try:
                        result = eval(code, exec_globals)
                        if result is not None:
                            if isinstance(result, pd.DataFrame):
                                cell['dataframe'] = result
                            elif isinstance(result, pd.Series):
                                cell['series'] = result
                            elif isinstance(result, (go.Figure, px._figure_py.Figure)) or hasattr(result, '_grid_ref'):
                                # Only capture figure if st.plotly_chart is NOT used
                                if not uses_streamlit_chart:
                                    cell['figure'] = result
                            else:
                                cell['result'] = result
                    except:
                        exec(code, exec_globals)
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
                
                # Update df in session state
                if 'df' in exec_globals:
                    st.session_state.df = exec_globals['df']

                # Only auto-capture figures if st.plotly_chart is NOT in the code
                if not uses_streamlit_chart:
                    for key, value in exec_globals.items():
                        if isinstance(value, (go.Figure, px._figure_py.Figure)):
                            cell['figure'] = value
                            break
                        elif hasattr(value, '_grid_ref'):
                            cell['figure'] = value
                            break
                
                # Update variables
                excluded_keys = {'pd', 'np', 'px', 'go', 'st', '__builtins__', 'print', '__name__', '__doc__', '__package__', '__loader__', '__spec__', '__annotations__', '__file__', '__cached__'}
                for key, value in exec_globals.items():
                    if key not in excluded_keys and not key.startswith('_'):
                        st.session_state.variables[key] = value
                
                captured_output = output_buffer.getvalue()
                captured_errors = error_buffer.getvalue()
                
                full_output = captured_output + captured_errors if captured_errors else captured_output
                cell['output'] = full_output if full_output else None
                cell['executed'] = True
                cell['error'] = None
                
                return True, None
                
            except Exception as e:
                error_traceback = traceback.format_exc()
                cell['output'] = None
                cell['error'] = str(e)
                cell['error_traceback'] = error_traceback
                cell['executed'] = False
                cell['execution_count'] = None
                return False, str(e)
    return False, "Cell not found"
