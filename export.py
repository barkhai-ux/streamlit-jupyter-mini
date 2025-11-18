import streamlit as st
import json

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
        # Use content_list if available, otherwise split content by newlines
        if 'content_list' in cell and cell['content_list']:
            source = cell['content_list']
        else:
            content = cell.get('content', '')
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
