import requests
from bs4 import BeautifulSoup
from pygooglenews import GoogleNews
import nltk
nltk.download('vader_lexicon')
import pathlib
import textwrap
import google.generativeai as genai
import os
api_key  = "GEMINI_API_KEY"
genai.configure(api_key=api_key )
model = genai.GenerativeModel('gemini-pro')

company_name = input("Enter the company name: ")

gn = GoogleNews(lang='en') 
news_results = gn.search(company_name)

url = news_results['entries'][0]['link']

def extract_text_from_url(url):
    try:
        
        response = requests.get(url)
        
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
            
            return text
        else:
            print("Failed to retrieve content from URL.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def generate(text):
  return model.generate_content(f" I will provide some recent articles about a company. You have to do sentimental analysis of the company based on general information about the company and from the articles I'm giving. {text} ")



text = extract_text_from_url(url)
response = generate(text)
print(response.text)


