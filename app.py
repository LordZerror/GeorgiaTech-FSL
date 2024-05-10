# import warnings
# from sec_downloader import Downloader
# import sec_parser as sp
# import re
# import pathlib
# import textwrap
# import google.generativeai as genai
# import os
# from IPython.display import display
# from IPython.display import Markdown
# from dotenv import load_dotenv
# import time

# load_dotenv()

# GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

# genai.configure(api_key=GOOGLE_API_KEY)

# model = genai.GenerativeModel('gemini-pro')

# def clean_text(text):
#     x = re.sub(r"\s+", " ", text)
#     return x

# dl = Downloader("Kaushal Patil", "kaushalcode16@gmail.com")
# html = dl.get_filing_html(ticker="AAPL", form="10-K")
# parser = sp.Edgar10QParser()

# with warnings.catch_warnings():
#     warnings.filterwarnings("ignore", message="Invalid section type for")
#     elements: list = parser.parse(html)
    
# tree: sp.SemanticTree = sp.TreeBuilder().build(elements)

# demo_output: str = sp.render(tree)
# text = '\n'.join(demo_output.split('\n'))

# data = {}

# for i in tree.nodes:
#     ls = i.children
#     # print(ls)
#     head = clean_text(i.text)
#     if len(ls) > 0:
#         data[i.text] = [clean_text(x.text) for x in ls]

# list_of_prompts = []

# for header, ls in data.items():
#     prompt = f'''
#     You are a top-class Financial Analyst who reads the SEC 10k fillings of various companies to generate concise reports about the same for normal readers to read upon 
#     Here, you will be provided an excerpt of SEC 10k fillings report with header and body containing the content under that header 
#     Header = {header}
#     Data = {ls}
    
#     Now with thd help of this content develop a CONCISE REPORT containing the content that is IMPORTANT and RELEVANT to the company's working understandable to common man or else if it is generic content avoid generating the report    
#     If you are generating the text, please try using the exact text from the given context
#     '''
#     list_of_prompts.append(prompt)
    
# import time
# responses = []
# count = 1
# for i in list_of_prompts:
#     try:
#         response = model.generate_content(i).text
#         time.sleep(5) # to avoid any additional fee from gemini
#         responses.append(response)
#         print(f'Prompt Done: {count}')
#         count += 1
#     except Exception as e:
#         print(f'Exception: {e}')

import streamlit as st
import warnings
from sec_downloader import Downloader
import sec_parser as sp
import re
import pathlib
import textwrap
import google.generativeai as genai
import os
from IPython.display import display
from IPython.display import Markdown
from dotenv import load_dotenv
import time

load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def clean_text(text):
    x = re.sub(r"\s+", " ", text)
    return x

# Streamlit app definition
st.title("SEC Filing Summarizer")

# User input for ticker symbol and filing type
ticker_symbol = st.text_input("Enter Ticker Symbol (e.g., AAPL):")
filing_type = st.selectbox("Select Filing Type:", ["10-K", "10-Q"])

# Download and parse filing if user clicks button
if st.button("Summarize Filing"):
    with st.spinner("Downloading and processing..."):
        try:
            dl = Downloader("Kaushal Patil", "kaushalcode16@gmail.com")
            html = dl.get_filing_html(ticker=ticker_symbol, form=filing_type)
            parser = sp.Edgar10QParser()

            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="Invalid section type for")
                elements: list = parser.parse(html)
                tree: sp.SemanticTree = sp.TreeBuilder().build(elements)

            demo_output: str = sp.render(tree)
            text = '\n'.join(demo_output.split('\n'))

            data = {}

            for i in tree.nodes:
                ls = i.children
                # print(ls)
                head = clean_text(i.text)
                if len(ls) > 0:
                    data[i.text] = [clean_text(x.text) for x in ls]

            list_of_prompts = []
            
            headers = list(data.keys())

            for header, ls in data.items():
                prompt = f'''
                You are a top-class Financial Analyst who reads the SEC {filing_type} fillings of various companies to generate concise reports about the same for normal readers to read upon 
                Here, you will be provided an excerpt of SEC {filing_type} fillings report with header and body containing the content under that header 
                Header = {header}
                Data = {ls}
                
                Now with the help of this content develop a CONCISE REPORT containing the content that is IMPORTANT and RELEVANT to the company's working understandable to common man or else if it is generic content avoid generating the report    
                If you are generating the text, please try using the exact text from the given context
                '''
                list_of_prompts.append(prompt)
            
            responses = []
            count = 0
            for i in list_of_prompts:
                try:
                    response = model.generate_content(i).text
                    time.sleep(5) # to avoid any additional fee from gemini
                    responses.append(i)
                    st.write(f'Summary for section: {headers[count]}')
                    st.success(response)
                except Exception as e:
                    st.error(f'Error processing section {headers[count]}: {e}')
                count += 1
        except Exception as e:
            st.error(f"Error downloading or parsing filing: {e}")