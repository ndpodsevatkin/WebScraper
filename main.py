import os
import requests
from bs4 import BeautifulSoup
import string


def search_article(page_num, article_type, url='https://www.nature.com/nature/articles'):
    for j in range(1, page_num + 1):
        if not os.path.isdir(f"Page_{j}"):
            os.mkdir(f"Page_{j}")   # creates a file with the page number
        r = requests.get(url, {'page': j})
        soup = BeautifulSoup(r.text, 'html.parser')
        article_types = soup.find_all('span', {'data-test': 'article.type'})    # looking for article type
        # looking for links to page's content
        article_content = soup.find_all('a', {'data-track-action': "view article"})
        save_path = os.getcwd()     # main path
        links = [i['href'] for i in article_content]    # links to content in a specific article
        titles = [j.text for j in article_content]  # the length of this two lists is the same, that's why I use indexes
        os.chdir(os.path.join(save_path, f"Page_{j}"))  # changes directory to a specific file named with
        # respect to page number
        for i in range(len(article_types)):
            if article_types[i].text.strip() == article_type:
                article_url = 'https://www.nature.com' + links[i]
                r_article = requests.get(article_url)
                soup_article = BeautifulSoup(r_article.text, 'html.parser')
                with open(f"{titles[i].translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')}.txt",
                          'w', encoding='UTF-8') as f:
                    if article_type == "Research Highlight":
                        f.write(soup_article.find('div', class_="article-item__body").text.strip())
                    else:
                        f.write(soup_article.find('div', class_='article__body').text.strip())
        os.chdir('..')  # goes to a parent directory


usr_page = int(input())
usr_article = input()

search_article(usr_page, usr_article)
