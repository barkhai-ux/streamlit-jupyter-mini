import streamlit as st

CUSTOM_CSS = """
<style>
    /* Global styles */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1300px;
    }
    
    /* Notebook cell */
    .notebook-cell {
        background: white;
        border: 2px solid #e1e4e8;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: all 0.2s;
    }
    
    .notebook-cell:hover {
        border-color: #0366d6;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }
    
    /* Cell header */
    .cell-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.75rem 1.25rem;
        border-radius: 6px 6px 0 0;
        color: white;
        font-weight: 600;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .cell-number {
        font-family: 'Courier New', monospace;
        background: rgba(255,255,255,0.2);
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
    }
    
    /* Cell controls */
    .cell-controls {
        background: #f6f8fa;
        padding: 0.75rem 1.25rem;
        border-bottom: 1px solid #e1e4e8;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    /* Cell content */
    .cell-content {
        padding: 1.25rem;
    }
    
    .cell-output {
        background: #f6f8fa;
        padding: 1.25rem;
        border-top: 2px solid #e1e4e8;
        border-radius: 0 0 6px 6px;
    }
    
    /* Code editor */
    .stTextArea textarea {
        font-family: 'Courier New', Consolas, 'Monaco', monospace !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        background: #1e1e1e !important;
        border: 1px solid #3c3c3c !important;
        border-radius: 6px !important;
        padding: 12px !important;
        color: #d4d4d4 !important;
        tab-size: 4 !important;
        caret-color: #d4d4d4 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #0366d6 !important;
        box-shadow: 0 0 0 3px rgba(3, 102, 214, 0.1) !important;
        outline: none !important;
    }
    
    /* Fix for text area label */
    .stTextArea label {
        color: #24292e !important;
    }
    
    /* Code syntax highlighting container */
    .code-editor-wrapper {
        position: relative;
        background: #1e1e1e;
        border-radius: 6px;
        border: 1px solid #3c3c3c;
        overflow: hidden;
    }
    
    .code-preview {
        background: #1e1e1e;
        padding: 12px;
        font-family: 'Courier New', Consolas, 'Monaco', monospace;
        font-size: 14px;
        line-height: 1.6;
        color: #d4d4d4;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin: 0;
        border: none;
        min-height: 200px;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
        border: 1px solid #e1e4e8 !important;
        padding: 0.4rem 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 2px solid #e1e4e8;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        margin-bottom: 0.5rem;
    }
    
    /* Success/Error boxes */
    .success-msg {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .error-msg {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .info-msg {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #17a2b8;
        margin: 0.5rem 0;
    }
    
    .warning-msg {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    
    /* Headers */
    h1 {
        color: #24292e !important;
        font-weight: 700 !important;
    }
    
    h2, h3 {
        color: #24292e !important;
        font-weight: 600 !important;
    }
    
    /* Help text */
    .help-text {
        background: #fffbea;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #f9c74f;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    
    /* Cell type badge */
    .cell-type {
        background: rgba(255,255,255,0.3);
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
<script>
    // Syntax highlighting function for Python code
    function highlightPythonCode(code) {
        // Python syntax highlighting colors
        const colors = {
            comment: '#6A9955',      // Green for comments
            string: '#CE9178',      // Orange for strings
            keyword: '#C586C0',     // Purple for keywords
            function: '#DCDCAA',    // Yellow for functions
            number: '#B5CEA8',       // Light green for numbers
            operator: '#D4D4D4',    // White for operators
            default: '#D4D4D4'      // Default text color
        };
        
        // Python keywords
        const keywords = ['def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 
                         'with', 'as', 'import', 'from', 'return', 'yield', 'break', 'continue', 'pass', 
                         'and', 'or', 'not', 'in', 'is', 'None', 'True', 'False', 'lambda', 'global', 
                         'nonlocal', 'assert', 'raise', 'del', 'async', 'await'];
        
        // Escape HTML
        code = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        
        // Highlight comments
        code = code.replace(/(#.*$)/gm, '<span style="color: ' + colors.comment + '">$1</span>');
        
        // Highlight strings (single, double, triple quotes)
        code = code.replace(/(['"])((?:\\.|(?!\1)[^\\])*?)(\1)/g, 
            '<span style="color: ' + colors.string + '">$1$2$3</span>');
        code = code.replace(/(['"]{3})([\s\S]*?)(['"]{3})/g, 
            '<span style="color: ' + colors.string + '">$1$2$3</span>');
        
        // Highlight keywords
        keywords.forEach(keyword => {
            const regex = new RegExp('\\b(' + keyword + ')\\b', 'g');
            code = code.replace(regex, '<span style="color: ' + colors.keyword + '">$1</span>');
        });
        
        // Highlight function definitions and calls
        code = code.replace(/(\b\w+)(\s*)(\()/g, function(match, funcName, space, paren) {
            if (!keywords.includes(funcName)) {
                return '<span style="color: ' + colors.function + '">' + funcName + '</span>' + space + paren;
            }
            return match;
        });
        
        // Highlight numbers
        code = code.replace(/\b(\d+\.?\d*)\b/g, '<span style="color: ' + colors.number + '">$1</span>');
        
        return code;
    }
    
    // Simple syntax highlighting overlay - text is always visible
    function applySyntaxHighlighting() {
        const textareas = document.querySelectorAll('.stTextArea textarea');
        textareas.forEach(textarea => {
            if (textarea.dataset.highlighted === 'true') return;
            textarea.dataset.highlighted = 'true';
            
            const textareaParent = textarea.parentElement;
            if (!textareaParent) return;
            
            // Create wrapper
            const wrapper = document.createElement('div');
            wrapper.style.position = 'relative';
            wrapper.style.background = '#1e1e1e';
            wrapper.style.borderRadius = '6px';
            wrapper.style.overflow = 'hidden';
            
            // Create highlight overlay behind textarea
            const highlightDiv = document.createElement('pre');
            highlightDiv.className = 'code-highlight-overlay';
            highlightDiv.style.cssText = 'position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: 0; padding: 12px; pointer-events: none; white-space: pre-wrap; word-wrap: break-word; font-family: "Courier New", Consolas, "Monaco", monospace; font-size: 14px; line-height: 1.6; overflow: hidden; z-index: 1; background: transparent; border: none;';
            
            // Keep textarea visible with transparent background so overlay shows through
            textarea.style.cssText += 'position: relative; z-index: 2; background: transparent !important; caret-color: #d4d4d4 !important;';
            
            function updateHighlight() {
                const code = textarea.value || '';
                highlightDiv.innerHTML = highlightPythonCode(code);
            }
            
            function syncScroll() {
                highlightDiv.scrollTop = textarea.scrollTop;
                highlightDiv.scrollLeft = textarea.scrollLeft;
            }
            
            textarea.addEventListener('input', updateHighlight);
            textarea.addEventListener('scroll', syncScroll);
            textarea.addEventListener('keyup', updateHighlight);
            textarea.addEventListener('paste', () => setTimeout(updateHighlight, 10));
            
            updateHighlight();
            
            // Wrap textarea
            textareaParent.insertBefore(wrapper, textarea);
            wrapper.appendChild(highlightDiv);
            wrapper.appendChild(textarea);
        });
    }
    
    // Initialize with multiple attempts for Streamlit
    function initHighlighting() {
        try {
            applySyntaxHighlighting();
            setTimeout(applySyntaxHighlighting, 300);
            setTimeout(applySyntaxHighlighting, 800);
        } catch (e) {
            console.error('Syntax highlighting error:', e);
        }
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHighlighting);
    } else {
        initHighlighting();
    }
    
    // Watch for Streamlit reruns
    let timeoutId;
    const observer = new MutationObserver(() => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(initHighlighting, 300);
    });
    observer.observe(document.body, { childList: true, subtree: true });
</script>
"""


def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Data Analysis Notebook",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Interactive notebook for data analysts learning Python"
        }
    )


def initialize_session_state():
    """Initialize all session state variables"""
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'cells' not in st.session_state:
        st.session_state.cells = []
    if 'cell_counter' not in st.session_state:
        st.session_state.cell_counter = 1
    if 'variables' not in st.session_state:
        st.session_state.variables = {}
    if 'file_loaded' not in st.session_state:
        st.session_state.file_loaded = False
    if 'execution_count' not in st.session_state:
        st.session_state.execution_count = 0


CODE_TEMPLATES = {
    "📂 Load Data": {
        "Load CSV File": {
            "code": [
                "df = pd.read_csv('your_file.csv')",
                "",
                "print(f'✓ Loaded {len(df)} rows and {len(df.columns)} columns')",
                "df.head()"
            ],
            "description": "Load your data from a CSV file and preview it"
        },
        "Load Excel File": {
            "code": [
                "# Load data from Excel file",
                "df = pd.read_excel('your_file.xlsx')",
                "",
                "# Show first 5 rows",
                "print(f'✓ Loaded {len(df)} rows and {len(df.columns)} columns')",
                "df.head()"
            ],
            "description": "Load your data from an Excel file"
        }
    },
    "🔍 Explore Data": {
        "View First Rows": {
            "code": [
                "# View the first 10 rows of your data",
                "df.head(10)"
            ],
            "description": "See the beginning of your dataset"
        },
        "View Last Rows": {
            "code": [
                "# View the last 10 rows of your data",
                "df.tail(10)"
            ],
            "description": "See the end of your dataset"
        },
        "Basic Information": {
            "code": [
                "# Get basic information about your data",
                "print(f'Number of rows: {len(df)}')",
                "print(f'Number of columns: {len(df.columns)}')",
                "print(f'\\nColumn names:')",
                "print(df.columns.tolist())",
                "print(f'\\nData types:')",
                "print(df.dtypes)"
            ],
            "description": "See shape, columns, and data types"
        },
        "Check Missing Data": {
            "code": [
                "# Check for missing values in each column",
                "missing = df.isnull().sum()",
                "print('Missing values per column:')",
                "print(missing[missing > 0])",
                "print(f'\\nTotal missing: {df.isnull().sum().sum()}')"
            ],
            "description": "Find which columns have missing data"
        },
        "Summary Statistics": {
            "code": [
                "# Get statistical summary of numeric columns",
                "df.describe()"
            ],
            "description": "See mean, min, max, etc. for numbers"
        }
    },
    "📊 Analyze Data": {
        "Count Values": {
            "code": [
                "# Count how many times each value appears",
                "# Change 'column_name' to your actual column",
                "df['column_name'].value_counts()"
            ],
            "description": "Count occurrences of each unique value"
        },
        "Calculate Average": {
            "code": [
                "# Calculate the average (mean) of a column",
                "# Change 'column_name' to your actual column",
                "average = df['column_name'].mean()",
                "print(f'Average: {average:.2f}')"
            ],
            "description": "Find the average of a numeric column"
        },
        "Find Maximum/Minimum": {
            "code": [
                "# Find the highest and lowest values",
                "# Change 'column_name' to your actual column",
                "print(f'Maximum: {df[\"column_name\"].max()}')",
                "print(f'Minimum: {df[\"column_name\"].min()}')"
            ],
            "description": "Find the highest and lowest values"
        },
        "Group and Average": {
            "code": [
                "# Calculate average by group",
                "# Change 'group_column' and 'value_column' to your columns",
                "grouped = df.groupby('group_column')['value_column'].mean()",
                "print(grouped)"
            ],
            "description": "Calculate averages for each category"
        },
        "Correlation Matrix": {
            "code": [
                "# See how numeric columns relate to each other",
                "corr = df.corr(numeric_only=True)",
                "print(corr)"
            ],
            "description": "Find relationships between numbers"
        }
    },
    "🧹 Clean Data": {
        "Remove Missing Values": {
            "code": [
                "# Remove rows with any missing data",
                "df_clean = df.dropna()",
                "print(f'Removed {len(df) - len(df_clean)} rows with missing data')",
                "print(f'New dataset has {len(df_clean)} rows')",
                "df = df_clean"
            ],
            "description": "Delete rows that have empty cells"
        },
        "Fill Missing Values": {
            "code": [
                "# Replace missing values with the average",
                "# Change 'column_name' to your actual column",
                "mean_value = df['column_name'].mean()",
                "df['column_name'].fillna(mean_value, inplace=True)",
                "print(f'✓ Filled missing values with average: {mean_value:.2f}')"
            ],
            "description": "Replace empty cells with average value"
        },
        "Remove Duplicates": {
            "code": [
                "# Remove duplicate rows",
                "original_count = len(df)",
                "df = df.drop_duplicates()",
                "removed = original_count - len(df)",
                "print(f'✓ Removed {removed} duplicate rows')",
                "print(f'New dataset has {len(df)} rows')"
            ],
            "description": "Delete rows that appear more than once"
        },
        "Rename Column": {
            "code": [
                "# Rename a column to a better name",
                "# Change 'old_name' and 'new_name' to your names",
                "df.rename(columns={'old_name': 'new_name'}, inplace=True)",
                "print('✓ Column renamed successfully')",
                "print(f'Columns: {df.columns.tolist()}')"
            ],
            "description": "Give a column a new, clearer name"
        },
        "Delete Column": {
            "code": [
                "# Remove a column you don't need",
                "# Change 'column_name' to the column you want to delete",
                "df.drop('column_name', axis=1, inplace=True)",
                "print('✓ Column deleted')",
                "print(f'Remaining columns: {df.columns.tolist()}')"
            ],
            "description": "Remove a column from your dataset"
        }
    },
    "🔎 Filter Data": {
        "Filter by Value": {
            "code": [
                "# Keep only rows where a condition is true",
                "# Change 'column_name' and 'value' to your needs",
                "filtered = df[df['column_name'] == 'value']",
                "print(f'Found {len(filtered)} matching rows')",
                "filtered.head()"
            ],
            "description": "Show only rows that match a condition"
        },
        "Filter Numbers": {
            "code": [
                "# Keep rows where number is greater than a value",
                "# Change 'column_name' and 50 to your needs",
                "filtered = df[df['column_name'] > 50]",
                "print(f'Found {len(filtered)} rows where value > 50')",
                "filtered.head()"
            ],
            "description": "Filter rows by numeric comparison"
        },
        "Filter Multiple Conditions": {
            "code": [
                "# Filter with multiple conditions (AND)",
                "# Change column names and values to your needs",
                "filtered = df[(df['column1'] > 50) & (df['column2'] == 'value')]",
                "print(f'Found {len(filtered)} matching rows')",
                "filtered.head()"
            ],
            "description": "Filter using two or more conditions"
        },
        "Filter by Text": {
            "code": [
                "# Find rows where text contains certain words",
                "# Change 'column_name' and 'keyword' to your needs",
                "filtered = df[df['column_name'].str.contains('keyword', case=False, na=False)]",
                "print(f'Found {len(filtered)} rows containing \"keyword\"')",
                "filtered.head()"
            ],
            "description": "Search for text within a column"
        }
    },
    "🔧 Transform Data": {
        "Create New Column": {
            "code": [
                "# Create a new column from existing ones",
                "# Example: combine first and last name",
                "df['full_name'] = df['first_name'] + ' ' + df['last_name']",
                "print('✓ New column created')",
                "df.head()"
            ],
            "description": "Add a new column based on other columns"
        },
        "Calculate New Column": {
            "code": [
                "# Create column with calculation",
                "# Example: calculate total price",
                "df['total'] = df['price'] * df['quantity']",
                "print('✓ Calculated new column')",
                "df.head()"
            ],
            "description": "Add a column with mathematical calculation"
        },
        "Sort Data": {
            "code": [
                "# Sort data by a column",
                "# Change 'column_name' to your column",
                "df_sorted = df.sort_values('column_name', ascending=False)",
                "print('✓ Data sorted from highest to lowest')",
                "df_sorted.head()"
            ],
            "description": "Arrange rows in order by a column"
        },
        "Convert to Categories": {
            "code": [
                "# Create categories from numbers",
                "# Example: convert age to age groups",
                "df['age_group'] = pd.cut(df['age'],",
                "                          bins=[0, 18, 30, 50, 100],",
                "                          labels=['0-18', '19-30', '31-50', '50+'])",
                "print('✓ Created age groups')",
                "df['age_group'].value_counts()"
            ],
            "description": "Group numbers into categories (bins)"
        }
    },
    "📈 Visualize Data": {
        "Bar Chart": {
            "code": [
                "# Create a bar chart",
                "# Change column names to your data",
                "fig = px.bar(df,",
                "             x='category_column',",
                "             y='value_column',",
                "             title='My Bar Chart')",
                "st.plotly_chart(fig, use_container_width=True)"
            ],
            "description": "Compare values across categories"
        },
        "Line Chart": {
            "code": [
                "# Create a line chart",
                "# Good for showing trends over time",
                "fig = px.line(df,",
                "              x='date_column',",
                "              y='value_column',",
                "              title='Trend Over Time')",
                "st.plotly_chart(fig, use_container_width=True)"
            ],
            "description": "Show trends and changes over time"
        },
        "Scatter Plot": {
            "code": [
                "# Create a scatter plot",
                "# See relationship between two numbers",
                "fig = px.scatter(df,",
                "                 x='column1',",
                "                 y='column2',",
                "                 title='Relationship Between Two Variables')",
                "st.plotly_chart(fig, use_container_width=True)"
            ],
            "description": "Explore relationships between two numbers"
        },
        "Histogram": {
            "code": [
                "# Create a histogram",
                "# Shows the distribution of values",
                "fig = px.histogram(df,",
                "                   x='column_name',",
                "                   nbins=30,",
                "                   title='Distribution of Values')",
                "st.plotly_chart(fig, use_container_width=True)"
            ],
            "description": "See how values are distributed"
        },
        "Pie Chart": {
            "code": [
                "# Create a pie chart",
                "# Shows proportions of a whole",
                "value_counts = df['category_column'].value_counts()",
                "fig = px.pie(values=value_counts.values,",
                "             names=value_counts.index,",
                "             title='Distribution by Category')",
                "st.plotly_chart(fig, use_container_width=True)"
            ],
            "description": "Show proportions and percentages"
        },
        "Box Plot": {
            "code": [
                "# Create a box plot",
                "# Shows data distribution and outliers",
                "fig = px.box(df,",
                "             y='column_name',",
                "             title='Box Plot')",
                "st.plotly_chart(fig, use_container_width=True)"
            ],
            "description": "Identify outliers and data spread"
        }
    },
    "💾 Save Results": {
        "Save to CSV": {
            "code": [
                "# Save your data to a CSV file",
                "df.to_csv('output_data.csv', index=False)",
                "print('✓ Data saved as output_data.csv')"
            ],
            "description": "Export your data to a CSV file"
        },
        "Save to Excel": {
            "code": [
                "# Save your data to an Excel file",
                "df.to_excel('output_data.xlsx', index=False)",
                "print('✓ Data saved as output_data.xlsx')"
            ],
            "description": "Export your data to an Excel file"
        }
    }
}
