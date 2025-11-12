import streamlit as st
import json
import re

def export_to_ipynb():
    """Export Streamlit session cells to a .ipynb notebook format"""
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
        content = cell.get('content', '')

        if content:
            # Normalize line endings
            content = content.replace('\r\n', '\n').replace('\r', '\n')

            # 🔧 Fix chained comments and code separation safely
            content = re.sub(r'#([^#\n]+)#', r'#\1\n#', content)  # split chained comments
            content = re.sub(r'(#.*?)((?:[A-Za-z_]|df|st|print|\())', r'\1\n\2', content)  # newline before code

            # Heuristic check for mostly concatenated content
            newline_count = content.count('\n')
            is_mostly_concatenated = (newline_count == 0 and len(content) > 50) or \
                                     (newline_count > 0 and newline_count < len(content) / 100)

            if is_mostly_concatenated:
                # Add newlines between assignments, print, df, st calls, etc.
                content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=]+?)([a-zA-Z_][a-zA-Z0-9_]*\s*=)', r'\1\n\2', content)
                content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=]+?)(print\s*\()', r'\1\n\2', content)
                content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=]+?)(df\.)', r'\1\n\2', content)
                content = re.sub(r'(\)\s*)(print\s*\()', r'\1\n\2', content)
                content = re.sub(r'(\)\s*)(df\.)', r'\1\n\2', content)
                content = re.sub(r'(\.head\(\)\s*)([a-zA-Z_])', r'\1\n\2', content)
                content = re.sub(r'(\.tail\(\)\s*)([a-zA-Z_])', r'\1\n\2', content)
                content = re.sub(r'(\.describe\(\)\s*)([a-zA-Z_])', r'\1\n\2', content)
                content = re.sub(r'#([^\n#]+)(?=#)', r'#\1\n', content)
                content = re.sub(r'(#.*?)(?=[A-Za-z_]|df|st|print|\()', r'\1\n', content)


            source_lines = content.split('\n')
            source = [line if line is not None else '' for line in source_lines]
            if not source:
                source = ['']
        else:
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
            if cell.get('output'):
                nb_cell["outputs"].append({
                    "output_type": "stream",
                    "name": "stdout",
                    "text": cell['output'].split('\n')
                })
            
            if cell.get('dataframe') is not None:
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
            nb_cell["outputs"].append({
                "output_type": "error",
                "ename": "Exception",
                "evalue": cell['error'],
                "traceback": cell.get('error_traceback', '').split('\n') if cell.get('error_traceback') else []
            })

        notebook["cells"].append(nb_cell)
    
    return json.dumps(notebook, indent=2)
