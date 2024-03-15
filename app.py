import os

import pandas as pd
import streamlit as st
from pandasai import SmartDataframe
from pandasai.llm.azure_openai import AzureOpenAI
import dotenv

dotenv.load_dotenv('.env')

deployment = os.environ.get('AZURE_DEPLOYMENT_NAME')

st.set_page_config(page_title="PandasAI UI", page_icon="📄", layout="wide")

st.markdown(
    '<p style="display:inline-block;font-size:40px;font-weight:bold;">📊csvGPT </p>'
    ' <p style="display:inline-block;font-size:16px;">csvGPT is tool that uses AI-powered '
    'natural language processing to analyze and provide insights on CSV data. Users can '
    'upload CSV files, view the data, and have interactive conversations with the AI model '
    'to obtain valuable information and answers related to the uploaded data <br><br></p>',
    unsafe_allow_html=True
)


def chat_with_csv(df, prompt):
    llm = AzureOpenAI(deployment_name=deployment)
    smart_df = SmartDataframe(df, config={"llm": llm})
    answer = smart_df.chat(prompt)
    return answer


input_file = st.file_uploader("Upload your file", type=['csv', 'xlsx'])
if input_file is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("File Uploaded Successfully")
        if input_file.name.endswith(".csv"):
            data = pd.read_csv(input_file)
        elif input_file.name.endswith(".xlsx"):
            data = pd.read_excel(input_file)
        st.dataframe(data, use_container_width=True)

    with col2:
        st.info("Chat Below")
        input_text = st.text_area("Enter your query")

        if input_text is not None:
            if st.button("Chat with CSV"):
                st.info("Your Query: " + input_text)
                result = chat_with_csv(data, input_text)
                st.success(result)


hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""

# Apply CSS code to hide header, footer, and menu
st.markdown(hide_st_style, unsafe_allow_html=True)
