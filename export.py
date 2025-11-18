import streamlit as st
import json
import re
import ast


def export_to_ipynb():
    """Simple export function that works with list-based code storage"""
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
    
    for cell in st.session_state.get('cells', []):
        content = cell.get('content', '')
        
        # If content is stored as list, use it directly
        if isinstance(content, list):
            source = content
        else:
            # Fallback: split by newlines
            source = content.split('\n') if content else ['']
        
        nb_cell = {
            "cell_type": "code",
            "execution_count": cell.get('execution_count'),
            "metadata": {},
            "outputs": [],
            "source": source
        }
        
        notebook["cells"].append(nb_cell)
    
    return json.dumps(notebook, indent=2)
