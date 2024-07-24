from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import RequestException
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
import os
import logging

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI
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

class RAGRequest(BaseModel):
    file_path: str
    prompt: str

class URL(BaseModel):
    url: str

@app.post("/rag")
async def rag(request: RAGRequest):
    if not os.path.exists(request.file_path):
        logger.error(f"File not found: {request.file_path}")
        raise HTTPException(status_code=404, detail=f"File not found: {request.file_path}")

    try:
        documents = SimpleDirectoryReader(
            input_files=[request.file_path]
        ).load_data()
        index = VectorStoreIndex.from_documents(documents)
        
        query_engine = index.as_query_engine()
        answer = query_engine.query(request.prompt)
        
        return {
            "sources": answer.get_formatted_sources(),
            "user_query": request.prompt,
            "assistant_response": str(answer)
        }
    except Exception as e:
        logger.exception("Error occurred in RAG process")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/extract_links")
async def extract_links(url: URL):
    def extract_unique_links(url, max_retries=3, timeout=30):
        for attempt in range(max_retries):
            try:
                response = requests.get(url.url, timeout=timeout)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                a_tags = soup.find_all('a')
                links = [a.get('href') for a in a_tags if a.get('href')]
                unique_links = list(dict.fromkeys(links))
                return unique_links
            except RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed to retrieve {url.url} after {max_retries} attempts.")
                    raise HTTPException(status_code=500, detail=f"Failed to retrieve {url.url} after {max_retries} attempts.")
        return []

    unique_links = extract_unique_links(url.url)
    return {"unique_links": unique_links}

@app.post("/extract_text")
async def extract_text(urls: List[str]):
    def text_data_extractor(links):
        extracted_texts = []
        for link in links:
            if link.startswith('#'):
                link = "https://thumbay.com/"+link
            elif not link.startswith('http'):
                link = "https://thumbay.com/" + link.lstrip('/')
            
            retries = 3
            while retries > 0:
                try:
                    response = requests.get(link, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text()
                    clean_text = ' '.join(text.split())
                    extracted_texts.append({"url": link, "text": clean_text})
                    break
                except RequestException as e:
                    retries -= 1
                    logger.warning(f"Retry {3 - retries} for {link} failed: {e}")
                    if retries > 0:
                        wait_time = 5 * (3 - retries)
                        time.sleep(wait_time)
            
            if retries == 0:
                extracted_texts.append({"url": link, "text": "Failed to retrieve text after multiple attempts."})

        return extracted_texts

    extracted_data = text_data_extractor(urls)
    
    # Save extracted text to a file
    output_file = "extracted_text.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for item in extracted_data:
            f.write(f"URL: {item['url']}\n")
            f.write(f"Text: {item['text']}\n\n")
    
    return {"extracted_data": extracted_data, "file_saved": output_file}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
