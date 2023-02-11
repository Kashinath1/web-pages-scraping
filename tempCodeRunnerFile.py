import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

requests.packages.urllib3.disable_warnings()

# Read the URLs from the Excel file
urls = pd.read_excel("E:\\aaravi\\pranab\\websites\\websites (2).xlsx")["url"].tolist()

# Read the keywords from the Excel file
keywords = pd.read_excel("E:\\aaravi\\pranab\\keywords\\keywords.xlsx")["key"].tolist()

# Define the function to extract the data
def extract_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the title, meta description, and published date
    title = soup.find("title").get_text() if soup.find("title") else ""
    meta_description = soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else ""
    published_date = soup.find("meta", attrs={"name": "pubdate"})["content"] if soup.find("meta", attrs={"name": "pubdate"}) else ""
    
    # Extract the text from the HTML content
    text = soup.get_text()
    
    # Check if any keyword exists in the text
    for keyword in keywords:
        if keyword in text:
            return [url, keyword, title, meta_description, published_date]

# Create a list to store the matching results
results = []

# Loop through each URL and scrape the data
for url in urls:
    result = extract_data(url)
    if result:
        results.append(result)

# Write the results to an Excel file
df = pd.DataFrame(results, columns=["URL", "Keyword", "Title", "Meta Description", "Published Date"])
df.to_excel(f"E:\\aaravi\\pranab\\results\\results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", index=False)

# Set the scanning and monitoring duration to 5 minutes daily
time.sleep(300)
