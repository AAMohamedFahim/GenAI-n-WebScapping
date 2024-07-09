from openai import AzureOpenAI
import os
import dotenv
from cognitive_STT import STT
from cognitive_TTS import TTS


def LLM_response(prompt):
    dotenv.load_dotenv()
    client = AzureOpenAI(
      azure_endpoint = os.environ["Azure_Endpoints"], 
      api_key=os.environ['Azure_Openai_Api'],  
      api_version = "2024-02-01"
      )
    deployment=os.environ['Azure_Deployements']

    # prompt = input("user : ")
    messages = [{"role": "user", "content": "you are the helpfull assistance to assist user dont use punctuation in output"},
                {"role": "assistant", "content": "ok"},
                {"role": "user", "content": prompt}]  

    completion = client.chat.completions.create(model=deployment, messages=messages,temperature=0.3)
    # print(completion)
    return(completion.choices[0].message.content)



def main():
    stt_result = STT()
    llm_response = LLM_response(stt_result)
    
    print(llm_response)
    TTS(llm_response)

if __name__ == "__main__":
    main()
  