import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""
    
    # Custom CSS
    st.markdown("""
    <style>
    /* Main App Styling */
    .stApp {
        background-color: #f9f9f9;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1f77b4;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background-color: #115e92;
        transform: translateY(-2px);
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        background-color: #1f77b4;
    }
    
    /* Cards for content blocks */
    div.block-container {
        border-radius: 10px;
        padding: 1.5rem;
    }
    
    /* Make the tabs more prominent */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f0f0;
        border-radius: 4px 4px 0px 0px;
        border: 1px solid #e0e0e0;
        border-bottom: none;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    /* Improve form elements */
    input, select, textarea {
        border-radius: 5px !important;
        border: 1px solid #ccc !important;
    }
    
    /* Make date picker clearer */
    .stDateInput > div:first-child {
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    
    /* Custom slider styling */
    .stSlider {
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        border-color: #1f77b4 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)
