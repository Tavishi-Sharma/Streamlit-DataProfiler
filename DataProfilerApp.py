import streamlit as st
import pandas as pd
import sys
import os 
from ydata-profiling import ProfileReport
import streamlit.components.v1 as components

st.set_page_config(page_title='Data Profiler',layout='wide')

def get_fileSize(file):
    size_bytes=sys.getsizeof(file)
    size_mb=size_bytes/(1024**2)
    return size_mb

def validate_file(file):
    filename=file.name
    name,ext=os.path.splitext(filename)
    if ext in ('.csv','.xlsx'):
        return ext
    else:
        return False

# Sidebar file uploader
with st.sidebar:
    uploaded_file = st.file_uploader("Upload .csv or .xlsx file")

if uploaded_file is not None:
    ext=validate_file(uploaded_file)
    if ext:
        file_size=get_fileSize(uploaded_file)
        if file_size <= 10:
            if ext=='.csv':
                #time being let load csv
                df=pd.read_csv(uploaded_file)
            else:
                xl_file=pd.ExcelFile(uploaded_file)
                sheet_tuple=tuple(xl_file.sheet_names)
                sheet_name=st.sidebar.selectbox('select the sheet',sheet_tuple)
                df=xl_file.parse(sheet_name)

            st.spinner("Generating report...")

            # Generate report
            profile = ProfileReport(df, title="Data Report", explorative=True)

            # Render HTML report manually
            profile_html = profile.to_html()
            components.html(profile_html, height=1000, scrolling=True)
        else:
            st.error('Maximum 10MB file is allowed.')
    else:
        st.error('Kindly upload only .csv or .xlsx files.')
else:
    st.title('Data Profiler')
    st.info('Upload your data in the left sidebar to generate profiling.')
