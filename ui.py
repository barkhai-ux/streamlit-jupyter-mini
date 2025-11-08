import streamlit as st
import pandas as pd
from cell_manager import add_cell, delete_cell, execute_cell
from export import export_to_ipynb
from config import CODE_TEMPLATES


def render_sidebar():
    with st.sidebar:
        st.title("Quick Start")
        
        st.markdown("### 📁 Step 1: Upload Data")
        uploaded_file = st.file_uploader(
            "Choose your file", 
            type=['csv', 'xlsx', 'xls'], 
            help="Upload a CSV or Excel file to get started"
        )

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    st.session_state.df = pd.read_csv(uploaded_file)
                else:
                    st.session_state.df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ Loaded: {st.session_state.df.shape[0]} rows × {st.session_state.df.shape[1]} columns")
                
                with st.expander("📋 View Column Names"):
                    for col in st.session_state.df.columns:
                        st.text(f"• {col}")
                
                if not st.session_state.file_loaded:
                    file_code = f"""# Your data has been loaded!
# Rows: {st.session_state.df.shape[0]}, Columns: {st.session_state.df.shape[1]}

# Show first 5 rows
df.head()"""
                    add_cell(content=file_code, position=0)
                    st.session_state.file_loaded = True
                    st.rerun()

            except Exception as e:
                st.markdown(
                    f'<div class="error-msg">❌ Error loading file<br>{str(e)}</div>', 
                    unsafe_allow_html=True
                )
        
        st.markdown("---")
        
        st.markdown("### 📚 Step 2: Add Code")
        st.markdown("Choose a template to add to your notebook:")
        
        template_category = st.selectbox(
            "Select category:",
            list(CODE_TEMPLATES.keys()),
            help="Choose what you want to do with your data"
        )
        
        if template_category:
            template_options = list(CODE_TEMPLATES[template_category].keys())
            selected_template = st.selectbox(
                "Select action:",
                template_options,
                help="Pick a specific operation"
            )
            
            if selected_template:
                template_info = CODE_TEMPLATES[template_category][selected_template]
                st.info(f"ℹ️ {template_info['description']}")
                
                if st.button("➕ Add to Notebook", use_container_width=True, type="primary"):
                    add_cell(content=template_info['code'])
                    st.success("✅ Added to notebook!")
                    st.rerun()
        
        st.markdown("---")
        
        st.markdown("### 💾 Step 3: Save Work")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.cells:
                ipynb_content = export_to_ipynb()
                st.download_button(
                    label="📥 .ipynb",
                    data=ipynb_content,
                    file_name="notebook.ipynb",
                    mime="application/json",
                    use_container_width=True,
                    help="Download as Jupyter notebook"
                )
        
        with col2:
            if st.session_state.df is not None:
                csv = st.session_state.df.to_csv(index=False)
                st.download_button(
                    label="📊 CSV",
                    data=csv,
                    file_name="data.csv",
                    mime="text/csv",
                    use_container_width=True,
                    help="Download processed data"
                )
        


def render_cell(cell, idx):
    """Render a single notebook cell"""
    st.markdown('<div class="notebook-cell">', unsafe_allow_html=True)
    
    exec_count = f"[{cell.get('execution_count', '')}]" if cell.get('execution_count') else "[ ]"
    st.markdown(f'''
        <div class="cell-header">
            <div>
                <span class="cell-number">{exec_count}</span>
                <span class="cell-type">Code Cell</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="cell-controls">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 6])
    
    run_btn = col1.button("▶️ Run", key=f"run_{cell['id']}", help="Execute this cell", use_container_width=True)
    add_btn = col2.button("➕ Add", key=f"add_{cell['id']}", help="Add cell below", use_container_width=True)
    copy_btn = col3.button("📋 Copy", key=f"copy_{cell['id']}", help="Duplicate this cell", use_container_width=True)
    delete_btn = col4.button("🗑️ Delete", key=f"del_{cell['id']}", help="Delete this cell", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="cell-content">', unsafe_allow_html=True)
    
    cell_code = st.text_area(
        "Code",
        value=cell['content'],
        height=200,
        key=f"code_{cell['id']}",
        label_visibility="collapsed",
        help="Edit your Python code here"
    )
    
    cell['content'] = cell_code
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if cell['executed']:
        st.markdown('<div class="cell-output">', unsafe_allow_html=True)
        
        if cell.get('dataframe') is not None:
            st.dataframe(cell['dataframe'], use_container_width=True)
        
        if cell.get('series') is not None:
            st.dataframe(cell['series'], use_container_width=True)
        
        if cell.get('figure') is not None and 'st.plotly_chart' not in cell.get('content', ''):
            try:
                st.plotly_chart(cell['figure'], use_container_width=True)
            except Exception as plot_error:
                st.warning(f"⚠️ Could not display chart: {plot_error}")
        
        if cell.get('output'):
            st.text(cell['output'])
        elif cell.get('dataframe') is None and cell.get('series') is None and cell.get('figure') is None:
            st.markdown('<div class="success-msg">✓ Executed successfully</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if cell.get('error'):
        st.markdown('<div class="cell-output">', unsafe_allow_html=True)
        error_msg = cell['error']
        if cell.get('error_traceback'):
            with st.expander("🔍 Full Error Details", expanded=False):
                st.code(cell['error_traceback'], language='python')
        st.markdown(f'<div class="error-msg">❌ <strong>Error:</strong><br>{error_msg}</div>', unsafe_allow_html=True)
        st.markdown('<div class="warning-msg">💡 <strong>Tip:</strong> Make sure column names match your data exactly (check spelling and capitalization)</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if run_btn:
        execute_cell(cell['id'], cell_code)
        st.rerun()
    
    if add_btn:
        add_cell(position=idx + 1)
        st.rerun()
    
    if copy_btn:
        add_cell(content=cell['content'], position=idx + 1)
        st.rerun()
    
    if delete_btn:
        if len(st.session_state.cells) > 1:
            delete_cell(cell['id'])
            st.rerun()
        else:
            st.warning("⚠️ Cannot delete the last cell")


def render_main_content():
    """Render the main content area with cells"""
    if not st.session_state.cells:
        st.markdown('<div class="help-text">👋 <strong>Welcome!</strong> Get started by uploading data in the sidebar, then add your first code cell using the templates.</div>', unsafe_allow_html=True)
        
        if st.button("➕ Add Your First Cell", type="primary"):
            add_cell()
            st.rerun()
    else:
        for idx, cell in enumerate(st.session_state.cells):
            render_cell(cell, idx)
        
        st.markdown("---")
        if st.button("➕ Add New Cell at Bottom", type="secondary", use_container_width=False):
            add_cell()
            st.rerun()


def render_header():
    """Render the page header with title and action buttons"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📓 Data Analysis Notebook")
        st.markdown("*A beginner-friendly environment to analyze data with Python*")

    with col2:
        col2a, col2b = st.columns(2)
        with col2a:
            if st.button("▶️ Run All", use_container_width=True, help="Execute all cells in order"):
                from cell_manager import execute_cell
                for cell in st.session_state.cells:
                    execute_cell(cell['id'], cell['content'])
                st.rerun()
        with col2b:
            if st.button("🔄 Clear All", use_container_width=True, help="Clear all cells"):
                st.session_state.cells = []
                st.session_state.variables = {}
                st.session_state.execution_count = 0
                st.rerun()


