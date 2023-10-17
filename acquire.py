import requests
import re
import os
import pandas as pd

from requests import get
from bs4 import BeautifulSoup

def get_blog_articles_data(refresh=False):
    
    if not os.path.isfile('blog_articles.csv') or refresh:
        
        url = 'https://codeup.com/blog/'
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        links = [link['href'] for link in soup.select('h2 a[href]')]

        articles = []

        for url in links:

            url_response = get(url, headers=headers)
            soup = BeautifulSoup(url_response.text, 'html.parser')

            title = soup.find('h1', class_='entry-title').text
            content = soup.find('div', class_='entry-content').text.strip()

            article_dict = {
                'title': title,
                'content': content
            }

            articles.append(article_dict)
        
        blog_article_df = pd.DataFrame(articles)
        
        blog_article_df.to_csv('blog_articles.csv', index=False)
        
    return pd.read_csv('blog_articles.csv')



def get_news_articles_data(refresh=False):
    
    if not os.path.isfile('news_articles.csv') or refresh:
        
        url = 'https://inshorts.com/en/read'
        response = get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        categories = [li.text.lower() for li in soup.select('li')][1:]
        #categories[0] = 'national'

        inshorts = []

        for category in categories:

            cat_url = url + '/' + category
            response = get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            titles = [span.text for span in soup.find_all('span', itemprop='headline')]
            contents = [div.text for div in soup.find_all('div', itemprop='articleBody')]

            for i in range(len(titles)):

                article = {
                    'title': titles[i],
                    'content': contents[i],
                    'category': category,
                }

                inshorts.append(article)
                
        inshorts_article_df = pd.DataFrame(inshorts)
        
        inshorts_article_df.to_csv('news_articles.csv', index=False)
                
    return pd.read_csv('news_articles.csv')




def get_new_links(url, headers, sc1, sc2, sc3):
    # Send an HTTP GET request to the specified URL with the defined User-Agent header
    response = requests.get(url, headers=headers)
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the HTML elements with the 'h2' tag in the parsed HTML content
    links = soup.find_all(sc1)
    # Initialize an empty list to store the extracted links
    new_links = []

    # Loop through each 'article' element in the 'links' list
    for article in links:
        # Check if the 'article' contains an 'a' (anchor) element
        if article.find(sc2):
            # Append the link to the 'new_links' list
            new_links.append(article.find(sc2).get(sc3))

    return new_links


def get_news_article(new_links, headers):
    # Get the fourth URL from the 'new_links' list and assign it to the variable 'url'
    url = new_links[0]  # Change the index to the correct one
    # Send an HTTP GET request to the specified URL with the defined User-Agent header
    response = requests.get(url, headers=headers)
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the HTML element with the title and extract the text
    title = soup.find('h2').get_text()
    # Find the HTML element(s) containing the article content and extract the text
    content_elements = soup.select('.entry-content')  # Update this line to match the HTML structure
    # Initialize an empty list to store cleaned content
    clean_content = []
    
    # Loop through each content element
    for element in content_elements:
        # Extract the text content from the element and append it to the 'clean_content' list
        clean_content.append(element.get_text())
    content = ''.join(clean_content)
    news_ = {'title': title,
               'content': content  
    }
    news_.append(news_df)
        
    news_df = pd.DataFrame(news)
        
    news_df.to_csv('news_articles.csv', index=False)
        
    return pd.read_csv('news_articles.csv')


def get_article_data(new_links, headers):
    article_list = []
    
    for url in new_links:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title
        title = soup.find('h1')
        if title and title.get_text() != "Example Domain":
            title_text = title.get_text()
        else:
            title_text = "Title Not Found"

        # Extract the content
        content = soup.select('.entry-content')
        if content:
            content_text = ''.join([p.get_text() for p in content[0].find_all('p')])
        else:
            content_text = "Content Not Found"

        article_data = {
            'title': title_text,
            'content': content_text
        }

        article_list.append(article_data)
    
    return article_list