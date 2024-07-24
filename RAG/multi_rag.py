from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
import os


load_dotenv()

llm = AzureOpenAI(
    model="gpt-4o",
    deployment_name=os.environ['Azure_Deployements_LLM'],
    api_key=os.environ["Azure_Openai_Api"],
    azure_endpoint=os.environ['Azure_Endpoints'],
    api_version="2024-02-01",
)
embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name=os.environ['Azure_Deployements_EMB'],
    api_key=os.environ["Azure_Openai_Api"],
    azure_endpoint=os.environ['Azure_Endpoints'],
    api_version="2024-02-01",
)
Settings.llm = llm
Settings.embed_model = embed_model

def RAG():

    documents = SimpleDirectoryReader(
        input_files=["data/extracted_text12112.txt"]
    ).load_data()
    index = VectorStoreIndex.from_documents(documents)


    query = input("Prompt : ")
    query_engine = index.as_query_engine()
    answer = query_engine.query(query)

    print(answer.get_formatted_sources())
    print("\n\n---------------------------")
    print("User : ", query)
    print("Assistant : ", answer)
    print("---------------------------\n\n")
    
def main():
    while True:
        opt = int(input("Enter 1 to start convertation : "))
        if opt == 1:
            pass
        else:
            break
        RAG()

if __name__ == "__main__":
    main()