from requests import get
from bs4 import BeautifulSoup
from string import punctuation
from os import chdir, getcwd, mkdir
url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"


def scrap_by_page_and_cat(page_number, category):
    current_dir = getcwd()
    for i in range(1, page_number + 1):
        main_url = url + f"&page={i}"
        main_request = get(main_url)
        soup = BeautifulSoup(main_request.content, 'html.parser')
        article_links = soup.find_all('span', {'class': 'c-meta__type'}, text=category)
        folder_name = f"Page_{i}"
        mkdir(folder_name)
        chdir(current_dir + "/" + folder_name)
        for article in article_links:
            anchor = article.find_parent('article').find('a', {'data-track-action': 'view article'})
            follow_link = "https://www.nature.com" + anchor['href']
            article_request = get(follow_link)
            soup2 = BeautifulSoup(article_request.content, 'html.parser')
            main_body = soup2.find('div', {'class': 'c-article-body'}).text.encode()
            article_title = anchor.text.translate(str.maketrans(' ', ' ', punctuation)).replace(" ", "_").replace("’", "").strip() + ".txt"
            with open(article_title, "wb") as f:
                f.write(main_body)
        chdir("..")
    print("Saved all articles.")

pages_to_scrap = int(input())
category_to_scrap = input()
scrap_by_page_and_cat(pages_to_scrap, category_to_scrap)