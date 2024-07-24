import requests

def perform_rag(file_path, prompt):
    # The URL of your FastAPI server's RAG endpoint
    url = "http://0.0.0.0:8000/rag"

    # The data to send in the request body
    file_path = input("input file : ")
    prompt = input("prompt : ")
    data = {
        "file_path": file_path,
        "prompt": prompt
    }

    # Make the POST request
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example usage
file_path = "/path/to/your/extracted_text.txt"
prompt = "What are the main topics discussed in the extracted text?"

rag_result = perform_rag(file_path, prompt)

if rag_result:
    print("RAG Results:")
    print(f"User Query: {rag_result['user_query']}")
    print(f"Assistant Response: {rag_result['assistant_response']}")
    print("\nSources:")
    print(rag_result['sources'])