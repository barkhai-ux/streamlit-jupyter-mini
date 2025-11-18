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


def normalize_code_content(content):
    """Normalize and properly format code content with correct line breaks"""
    if not content:
        return ['']
    
    # Normalize line endings first
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split into lines first
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            processed_lines.append('')
            continue
            
        # Handle multiple statements on one line separated by semicolons
        if ';' in line:
            parts = line.split(';')
            for part in parts:
                part = part.strip()
                if part:
                    processed_lines.append(part)
            continue
        
        # Handle comment blocks stuck together
        if '#' in line and line.count('#') > 1:
            # Split multiple comments on the same line
            comment_parts = re.split(r'(?<=[^#])#', line)
            if len(comment_parts) > 1:
                for i, part in enumerate(comment_parts):
                    part = part.strip()
                    if i == 0 and part:
                        processed_lines.append(part)
                    elif part:
                        processed_lines.append('#' + part)
                continue
        
        # Handle common patterns where code gets concatenated
        patterns = [
            # Comment immediately followed by code
            (r'(#[^#\n]+)([a-zA-Z_][a-zA-Z0-9_].*)', r'\1\n\2'),
            # Print statement followed by other code
            (r'(print\([^)]*\))([a-zA-Z_][a-zA-Z0-9_].*)', r'\1\n\2'),
            # DataFrame operation followed by other code
            (r'(df\.[a-zA-Z_][a-zA-Z0-9_]*\([^)]*\))([a-zA-Z_][a-zA-Z0-9_].*)', r'\1\n\2'),
            # Assignment followed by other code
            (r'([a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=\n]+)([a-zA-Z_][a-zA-Z0-9_].*)', r'\1\n\2'),
        ]
        
        original_line = line
        for pattern, replacement in patterns:
            line = re.sub(pattern, replacement, line)
            if line != original_line:
                break
        
        # If the line is still very long and has multiple operations, try to split
        if len(line) > 100 and any(op in line for op in ['.', '=', '(', ')', '[', ']']):
            # Try to split on common Python operators and method calls
            line = re.sub(r'(\.[a-zA-Z_][a-zA-Z0-9_]*\()', r'\n\1', line)
            line = re.sub(r'(\))([a-zA-Z_][a-zA-Z0-9_])', r'\1\n\2', line)
        
        # Split the processed line if it contains newlines
        if '\n' in line:
            sub_lines = line.split('\n')
            for sub_line in sub_lines:
                sub_line = sub_line.strip()
                if sub_line:
                    processed_lines.append(sub_line)
        else:
            processed_lines.append(line)
    
    # Remove empty lines at the end
    while processed_lines and not processed_lines[-1]:
        processed_lines.pop()
    
    return processed_lines if processed_lines else ['']


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
        
        # Use the new normalization function
        source_lines = normalize_code_content(content)
        
        nb_cell = {
            "cell_type": "code",
            "execution_count": cell.get('execution_count'),
            "metadata": {},
            "outputs": [],
            "source": source_lines
        }
        
        # Handle execution output and errors
        if cell.get('executed') and not cell.get('error'):
            if cell.get('output'):
                # Normalize output lines as well
                output_lines = cell['output'].replace('\r\n', '\n').replace('\r', '\n').split('\n')
                nb_cell["outputs"].append({
                    "output_type": "stream",
                    "name": "stdout",
                    "text": output_lines
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
            error_lines = cell['error'].replace('\r\n', '\n').replace('\r', '\n').split('\n')
            nb_cell["outputs"].append({
                "output_type": "error",
                "ename": "Exception",
                "evalue": cell['error'],
                "traceback": error_lines
            })
        
        notebook["cells"].append(nb_cell)
    
    # FIXED: Return proper JSON string
    return json.dumps(notebook, indent=2)
