import os

import pandas as pd
import streamlit as st
from pandasai import SmartDataframe
from pandasai.llm.azure_openai import AzureOpenAI
from pandasai.llm.local_llm import LocalLLM

import dotenv

dotenv.load_dotenv('.env')

deployment = os.environ.get('AZURE_DEPLOYMENT_NAME')
environment = os.environ.get('ENV')

st.set_page_config(page_title="BASF Data Copilot", page_icon="📄", layout="wide")

st.markdown(
    '''<h3>BASF Data Copilot📊</h3>
              <p>Connect your structured data sources and extract insights in real time</p>
              <p>BASF Data copilot is tool that uses AI-powered '
              natural language processing to analyze and provide insights on CSV, Excel data. You can 
              upload CSV files, view the data, and have interactive conversations with the AI model
              to obtain valuable information and answers related to the uploaded data 
              </p>
              </br></br>
            ''', unsafe_allow_html=True)


def chat_with_csv(df, prompt):
    if environment == "BASF":
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
        model = os.getenv("MODEL_NAME")
        llm = LocalLLM(api_key=api_key, api_base=api_base, model=model)
    else:
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
            if st.button("Chat with File"):
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
