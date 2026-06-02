import requests
from bs4 import BeautifulSoup


def get_latest_news():
    url = "https://habr.com/ru/news/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_list = []
    links = soup.find_all('a', class_='tm-title__link', limit=5)

    for link in links:
        title = link.text.strip()
        href = "https://habr.com" + link.get('href')
        news_list.append((title, href))

    return news_list