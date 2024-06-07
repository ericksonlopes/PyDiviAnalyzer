import requests
from bs4 import BeautifulSoup

from py_invest_analyser.models.suno.news_suno_model import SunoNewsModel
from py_invest_analyser.services.openai.openai import OpenaiService


def get_html(url):
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5, verify=False)

    soup = BeautifulSoup(req.text, "html.parser")
    return soup


def get_news_suno(fii):
    url = f"https://www.suno.com.br/noticias/search/{fii}/"

    soup = get_html(url)

    loop_container = soup.find("div", class_="loopContainer")

    list_cards = loop_container.find_all("div", class_="cardsPage__listCard__boxs")

    for card in list_cards:
        card_news = SunoNewsModel()

        title = card.find("h2", class_="content__title").text
        card_news.title = title

        link = card.div.a["href"]
        card_news.link = link

        author_box = card.find("div", class_="authorBox__name")
        author = author_box.span.a.span.text
        datetime = author_box.time.text

        card_news.author = author
        card_news.date = datetime

        yield card_news


if __name__ == '__main__':
    list_news = []

    for news in get_news_suno("hglg11"):
        soup = get_html(news.link)

        content = soup.find("article", class_="newsContent__article").text
        news.content = content

        result_analysis = OpenaiService().get_answer(news.link)
        news.analysis = result_analysis

        # list_news.append(news)
