import streamlit as st
import json
import re
import ast


def is_valid_python(code):
    """Check if code string is valid Python syntax"""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


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
        content = cell.get('content', '')

        if content:
            # Normalize line endings
            content = content.replace('\r\n', '\n').replace('\r', '\n')
            
            # Store original for fallback
            original_content = content

            # Fix stuck comments: # comment1# comment2# comment3
            # This handles cases like "# Your data has been loaded!# Rows: 900"
            while '#' in content and content.count('#') > 1:
                new_content = re.sub(r'(#[^#\n]+)#', r'\1\n#', content)
                if new_content == content:  # No more changes
                    break
                content = new_content
            
            # Fix comment immediately followed by code (no space)
            # Handles: "# Show first 5 rowsdf.head()"
            content = re.sub(r'(#[^\n]+)([a-zA-Z_])', r'\1\n\2', content)

            # Heuristic check for mostly concatenated content
            newline_count = content.count('\n')
            is_mostly_concatenated = (
                (newline_count == 0 and len(content) > 50)
                or (newline_count > 0 and newline_count < len(content) / 100)
            )

            if is_mostly_concatenated:
                # Comment followed by code patterns
                content = re.sub(r'(#[^\n]+)\s+([a-zA-Z_][a-zA-Z0-9_]*\s*=)', r'\1\n\2', content)
                content = re.sub(r'(#[^\n]+)\s+(print\s*\()', r'\1\n\2', content)
                content = re.sub(r'(#[^\n]+)\s+(df\.)', r'\1\n\2', content)
                content = re.sub(r'(#[^\n]+)\s+(filtered\s*=)', r'\1\n\2', content)
                content = re.sub(r'(#[^\n]+)\s+(st\.)', r'\1\n\2', content)

                # Assignment followed by assignment
                content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=\n]+)\s+([a-zA-Z_][a-zA-Z0-9_]*\s*=)', r'\1\n\2', content)
                
                # Assignment followed by function calls
                content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=\n]+)\s+(print\s*\()', r'\1\n\2', content)
                content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=\n]+)\s+(df\.)', r'\1\n\2', content)
                
                # Closing paren followed by code
                content = re.sub(r'(\))\s+(print\s*\()', r'\1\n\2', content)
                content = re.sub(r'(\))\s+(df\.)', r'\1\n\2', content)
                content = re.sub(r'(\))\s+(filtered\.)', r'\1\n\2', content)
                
                # Pandas methods followed by code
                content = re.sub(r'(\.head\(\))\s+([a-zA-Z_])', r'\1\n\2', content)
                content = re.sub(r'(\.tail\(\))\s+([a-zA-Z_])', r'\1\n\2', content)
                content = re.sub(r'(\.describe\(\))\s+([a-zA-Z_])', r'\1\n\2', content)
                
                # String literal followed by assignment
                content = re.sub(r'(["\'])\s+([a-zA-Z_][a-zA-Z0-9_]*\s*=)', r'\1\n\2', content)
                
                # Consecutive print statements
                content = re.sub(r'(print\([^)]*\))\s+(print\s*\()', r'\1\n\2', content)
                
                # DataFrame indexing followed by code
                content = re.sub(r'(df\[[^\]]+\])\s+([a-zA-Z_])', r'\1\n\2', content)
            
            # Validate the formatted code
            if not is_valid_python(content) and is_valid_python(original_content):
                content = original_content
            
            # Clean up excessive blank lines
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # Split into lines for JSON structure
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
        
        # Handle execution output and errors
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
