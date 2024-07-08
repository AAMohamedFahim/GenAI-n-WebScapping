from openai import AzureOpenAI
import streamlit as st
import os
# import dotenv

def LLM_response(prompt):
    # dotenv.load_dotenv()
    client = AzureOpenAI(
      azure_endpoint = st.secrets["AZURE_ENDPOINT"], 
      api_key=st.secrets['AZURE_API'],  
      api_version = "2024-02-01"
      )
    deployment=st.secrets['AZURE_DEP']

    # prompt = input("user : ")
    messages = [{"role": "user", "content": "you are the helpfull assistance to assist user, dont use punctuation in output"},
                {"role": "assistant", "content": "ok"},
                {"role": "user", "content": prompt}]  

    completion = client.chat.completions.create(model=deployment, messages=messages,temperature=0.3)

    return completion.choices[0].message.content
    


# print(LLM_response("hi"))
