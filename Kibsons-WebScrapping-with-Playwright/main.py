from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import time
import json
import os


def extract_all_catogory_links():
    #Starting a site
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.kibsons.com/en/",timeout=60000)
    except:
        pass
    finally:
        #parsing a HTML content
        html = HTMLParser(page.content())
        #Selecting Catogory Section
        # print(html)
        all_cat = html.css("div.category-container > div")
        if all_cat == []:
            print("page not loaded succesfully!")
        #closing a page and browser
        # print(all_cat)
        page.close()
        playwright.stop()
    
    
    # time.sleep(5)#Wait to load
    # print(all_cat)
    link_list = []
    for catogory in all_cat:
        a_tag = catogory.css_first("figure.category-image a")
        link_list.append(a_tag.attributes.get('href'))
        # href = a_tag.attributes.get("href")
        # print(href)
    # print(link_list)
    return link_list


def prod_details_extractor(link,filepath,catogory):
    #json maker
    def check_json(response,filepath,catogory,prod_detail):
        
        termination_condition = {
        "status": 1,
        "message": "Success",
        "data": {
            "products": [],
            "filters": {}
        }
        }
        if "productsv26" in response.url:
            # print({'url' : response.url , 'body' : response.json()},"\n\n\n")

            if response.json() == termination_condition:
                pass
            else:
                prod_detail.append(response.json())
                
                                
                
                
            # else:
    prod_detail = []
    # link ="https://www.kibsons.com/en/viewall/quick-meals"
    end_count = 0  
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.on("response",lambda response: check_json(response,filepath,catogory,prod_detail))
    page.goto(link,timeout=0)
   
    last_height = page.evaluate("document.body.scrollHeight")
    
    while True:
        page.keyboard.press("End")
        time.sleep(5)  
        
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            end_count += 1
            if end_count<=3:
                pass
            else:
                break
        last_height = new_height
    page.close()
    playwright.stop() 
    cleaning_data(prod_detail)      
    
def cleaning_data(prod_detail):
    prod_count = 0
    filename = "data.json"
    # with open(filename, 'a') as file:
    #     file.write("\n")  
    #     json.dump(prod_detail, file,indent=1)
    #     file.write("\n")
        
    # print(len(prod_detail))
    for i in prod_detail:
        sub_prod_detail = i['data']['products']
        for j in sub_prod_detail:
            prod_count = prod_count+1
            prod_cnt = "product " + str(prod_count)
            prod_dict = [{
                prod_cnt : [{"prod_name" : j['product_filter'],
                    "prod_price" : j['stockRate'],
                    "min_order" : j['stockMinimumOrder'],
                    "prod_brand" : j["brandDesc"],
                    "prod_cat" : j['categories'][0]['category_filter'],
                    "prod_quantity" : j["stockShortDetail"],
                    "prod_origin" : j["originDesc"]}  
                ]}]
            
            with open(filename, 'r') as file:
                data = json.load(file)

            # New products to add
            # new_products = [
            #     {"name": "Product 3", "price": 300},
            #     {"name": "Product 4", "price": 400}
            # ]

            # Step 2: Append new products to the Product_Detail list
            data["Product_Detail"].extend(prod_dict)
            
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)



def main():
    
    # global prod_count 
    # prod_count = 0
    print("Start Exctracting Links Of Catogory....")
    cat_urls = extract_all_catogory_links()
    
    modified_cat_urls = []
    # prod_detail = []

    # Iterate over the original URLs and modify them
    for url in cat_urls:
        # Insert /viewall between /en and the rest of the path
        parts = url.split('/')
        modified_url = f'/{parts[1]}/viewall/{parts[2]}'
        modified_cat_urls.append(modified_url)  
        print(modified_url)
    # print(modified_cat_urls)
    print("Creating Json File...")
    filepath = "./data.json"
    if os.path.exists(filepath):
        os.remove(filepath)
        
    else:
        with open(filepath, 'w') as file: 
                print(f"File '{filepath}' created successfully.")
                json.dump({"Product_Detail" : []}, file,indent=1)
    for url in modified_cat_urls:
        link = "https://www.kibsons.com" + url
        print(f"Scraping '{link}' Page...")
        catogory = link.split('/')[-1]
        prod = prod_details_extractor(link,filepath,catogory)
        # prod_detail.append(prod)
        print(f"successfully scraped {link}")
    print(f"successfully scraped")
            
        
    # cleaning_data(prod)

                  
if __name__ == "__main__":
    main()
