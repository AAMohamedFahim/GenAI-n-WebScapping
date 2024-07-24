import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import RequestException

def extract_unique_links(url, max_retries=3, timeout=30):
    for attempt in range(max_retries):
        try:
            print(f"Attempting to retrieve {url} (Attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.find_all('a')
            links = [a.get('href') for a in a_tags if a.get('href')]
            unique_links = list(dict.fromkeys(links))
            print(f"Successfully retrieved {len(unique_links)} unique links from {url}")
            return unique_links
        except RequestException as e:
            print(f"Error retrieving {url}. Error: {e}")
            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)
                print(f"Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print(f"Failed to retrieve {url} after {max_retries} attempts.")
    return []

def text_data_extractor(links):
    with open('extracted_text.txt', 'a', encoding='utf-8') as file:
        for link in links:
            if link.startswith('#'):
                link = "https://thumbay.com/"+link
            elif not link.startswith('http'):
                link = "https://thumbay.com/" + link.lstrip('/')
            
            retries = 3
            while retries > 0:
                try:
                    print(f"Attempting to extract text from {link}")
                    response = requests.get(link, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text()
                    clean_text = ' '.join(text.split())
                    
                    file.write(f"Text from {link}:\n{clean_text}\n\n")
                    print(f"Successfully extracted text from {link}")
                    break
                except RequestException as e:
                    print(f"Error retrieving {link}. Error: {e}")
                    retries -= 1
                    if retries > 0:
                        wait_time = 5 * (3 - retries)
                        print(f"Waiting for {wait_time} seconds before retrying...")
                        time.sleep(wait_time)
            
            if retries == 0:
                print(f"Failed to retrieve {link} after multiple attempts.")

def main():
    url = 'https://thumbay.com/'
    
    unique_links_list = extract_unique_links(url)
    print(f"\nTotal number of unique links: {len(unique_links_list)}")
    
    if unique_links_list:
        text_data_extractor(unique_links_list)
        print("Extraction complete. Check 'extracted_text.txt' for the results.")
    else:
        print("No links were extracted. Stopping the process.")

if __name__ == "__main__":
    main()