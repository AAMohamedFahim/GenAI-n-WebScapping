from autoscraper import AutoScraper

url = 'https://azure.microsoft.com/en-in/pricing/details/cognitive-services/openai-service/'

# We can add one or multiple candidates here.
# You can also put urls here to retrieve urls.
wanted_list = ["GPT-4o Global Deployment","Context"]

scraper = AutoScraper()
result = scraper.build(url, wanted_list)
print(result)