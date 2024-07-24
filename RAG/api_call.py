import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Define the URLs for the endpoints
extract_links_url = "http://127.0.0.1:8000/extract_links"
extract_text_url = "http://127.0.0.1:8000/extract_text"
rag_url = "http://127.0.0.1:8000/rag"

# Step 1: Extract links from a given URL
url_to_extract = {"url": "https://www.space.com/marvel-movies-in-order"}

response = requests.post(extract_links_url, json=url_to_extract)
print("Response from extract_links:")
print(response.text)  # Print the response text for debugging

if response.status_code != 200:
    raise Exception(f"Error extracting links: {response.text}")  # Use response.text instead of response.json()
unique_links = response.json()["unique_links"]

# Step 2: Extract text from the extracted links
response = requests.post(extract_text_url, json=unique_links)
print("Response from extract_text:")
print(response.text)  # Print the response text for debugging

if response.status_code != 200:
    raise Exception(f"Error extracting text: {response.text}")  # Use response.text instead of response.json()
extracted_data = response.json()["extracted_data"]
file_saved = response.json()["file_saved"]

# Step 3: Use the extracted text in the RAG process
rag_request = {
    "file_path": file_saved,
    "prompt": "Your query here"
}

response = requests.post(rag_url, json=rag_request)
print("Response from RAG process:")
print(response.text)  # Print the response text for debugging

if response.status_code != 200:
    raise Exception(f"Error in RAG process: {response.text}")  # Use response.text instead of response.json()
rag_response = response.json()

# Print the response from the RAG process
print(json.dumps(rag_response, indent=2))
