import AzureOpenAI
import os
import dotenv

def LLM_response(prompt):
    dotenv.load_dotenv()
    client = AzureOpenAI(
      azure_endpoint = os.environ["Azure_Endpoints"], 
      api_key=os.environ['Azure_Openai_Api'],  
      api_version = "2024-02-01"
      )
    deployment=os.environ['Azure_Deployements']

    # prompt = input("user : ")
    messages = [{"role": "user", "content": "you are the helpfull assistance to assist user, dont use punctuation in output"},
                {"role": "assistant", "content": "ok"},
                {"role": "user", "content": prompt}]  

    completion = client.chat.completions.create(model=deployment, messages=messages,temperature=0.3)

    return completion.choices[0].message.content
    


# print(LLM_response("hi"))
