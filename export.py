"""
Export functionality for the Data Analysis Notebook
Handles exporting notebooks to Jupyter .ipynb format
"""

import streamlit as st
import json
import re


def export_to_ipynb():
    """Export notebook to .ipynb format with execution counts and outputs"""
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    for cell in st.session_state.cells:
        # Properly format source code for Jupyter notebook
        content = cell.get('content', '')
        
        # Normalize line endings and split by newlines
        # Handle different newline formats (\n, \r\n, \r)
        if content:
            # Normalize all line endings to \n
            content = content.replace('\r\n', '\n').replace('\r', '\n')
            
            # If content doesn't have newlines or has very few newlines, try to fix it
            # This handles cases where newlines were lost during storage
            # Check if content is mostly concatenated (few newlines relative to length)
            newline_count = content.count('\n')
            is_mostly_concatenated = (newline_count == 0 and len(content) > 50) or \
                                    (newline_count > 0 and newline_count < len(content) / 100)
            
            if is_mostly_concatenated:
                # Try to intelligently split concatenated code
                # Apply multiple passes to catch all patterns
                
                # Pattern 1: Comments followed by code (most common issue)
                # Match: # comment text followed immediately by code
                content = re.sub(r'(#\s*[^#\n]+?)([a-zA-Z_][a-zA-Z0-9_]*\s*=)', r'\1\n\2', content)
                content = re.sub(r'(#\s*[^#\n]+?)(print\s*\()', r'\1\n\2', content)
                content = re.sub(r'(#\s*[^#\n]+?)(df\.)', r'\1\n\2', content)
                content = re.sub(r'(#\s*[^#\n]+?)(filtered\s*=)', r'\1\n\2', content)
                content = re.sub(r'(#\s*[^#\n]+?)(st\.)', r'\1\n\2', content)
                
                # Pattern 2: Variable assignments followed by other statements
                # Match: variable = value followed by another statement
                content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=]+?)([a-zA-Z_][a-zA-Z0-9_]*\s*=)', r'\1\n\2', content)
                content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=]+?)(print\s*\()', r'\1\n\2', content)
                content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=]+?)(df\.)', r'\1\n\2', content)
                
                # Pattern 3: Method calls followed by statements
                # Match: ) followed by print or df
                content = re.sub(r'(\)\s*)(print\s*\()', r'\1\n\2', content)
                content = re.sub(r'(\)\s*)(df\.)', r'\1\n\2', content)
                content = re.sub(r'(\)\s*)(filtered\.)', r'\1\n\2', content)
                
                # Pattern 4: Method calls like .head() followed by code
                content = re.sub(r'(\.head\(\)\s*)([a-zA-Z_])', r'\1\n\2', content)
                content = re.sub(r'(\.tail\(\)\s*)([a-zA-Z_])', r'\1\n\2', content)
                content = re.sub(r'(\.describe\(\)\s*)([a-zA-Z_])', r'\1\n\2', content)
                
                # Pattern 5: String literals followed by code (less common but possible)
                content = re.sub(r'(["\']\s*)([a-zA-Z_][a-zA-Z0-9_]*\s*=)', r'\1\n\2', content)
                
                # Pattern 6: Multiple print statements in one line
                content = re.sub(r'(print\([^)]*\)\s*)(print\s*\()', r'\1\n\2', content)
                
                # Pattern 7: df operations followed by other operations
                content = re.sub(r'(df\[[^\]]+\]\s*)([a-zA-Z_])', r'\1\n\2', content)
            
            # Split by newlines, preserving empty lines
            source_lines = content.split('\n')
            # Filter out None values and ensure we have strings
            source = [line if line is not None else '' for line in source_lines]
            
            # Ensure we have at least one line
            if not source:
                source = ['']
        else:
            # Empty cell
            source = ['']
        
        nb_cell = {
            "cell_type": "code",
            "execution_count": cell.get('execution_count'),
            "metadata": {},
            "outputs": [],
            "source": source
        }
        
        # Add outputs if cell was executed
        if cell.get('executed') and not cell.get('error'):
            # Add text output
            if cell.get('output'):
                nb_cell["outputs"].append({
                    "output_type": "stream",
                    "name": "stdout",
                    "text": cell['output'].split('\n')
                })
            
            # Add DataFrame/Series as display_data
            if cell.get('dataframe') is not None:
                # Convert DataFrame to HTML for display
                html_output = cell['dataframe'].to_html()
                nb_cell["outputs"].append({
                    "output_type": "display_data",
                    "data": {"text/html": html_output},
                    "metadata": {}
                })
            elif cell.get('series') is not None:
                html_output = cell['series'].to_frame().to_html()
                nb_cell["outputs"].append({
                    "output_type": "display_data",
                    "data": {"text/html": html_output},
                    "metadata": {}
                })
        elif cell.get('error'):
            # Add error output
            nb_cell["outputs"].append({
                "output_type": "error",
                "ename": "Exception",
                "evalue": cell['error'],
                "traceback": cell.get('error_traceback', '').split('\n') if cell.get('error_traceback') else []
            })
        
        notebook["cells"].append(nb_cell)
    
    return json.dumps(notebook, indent=2)

