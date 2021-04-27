from lxml import html
from requests_html import HTMLSession
from collections import OrderedDict
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import json


def get_search_url(query_search_keyword):

    query_search_url = "https://www.everydayhealth.com/search/%s/" % query_search_keyword

    #query_search_url = "https://www.everydayhealth.com/search/fever/"

    print(query_search_url)
    session = HTMLSession()
    query_resp = session.get(query_search_url)
    query_soup = BeautifulSoup(query_resp.text, "lxml")

    return query_soup


def parse(page, query):

    suggestions = page.find_all("div", attrs={"class": "result-item"})

    suggestion_list = []

    for suggestion in suggestions:

        suggestion.suggestion_output = {
            "title": '',
            "title_link":  '',
            "description": '',
            "time":  '',
        }

        title = suggestion.find(
            "h2", attrs={"class": "result-item__title"}).find("a")
        if title is not None:
            title = title.getText()  # .replace('\t', '').replace('\n', '').replace(' ', '')
        else:
            title = ""

        title_link = suggestion.find(
            "a", attrs={"class": "cr-anchor result-item__link"})
        if title_link is not None:
            title_link = title_link.get('href')
        else:
            title_link = ""

        description = suggestion.find(
            "div", attrs={"class": "result-item__description"})
        if description is not None:
            description = description.getText()
        else:
            description = ""

        time = suggestion.find("time", attrs={"class": "result-item__date"})
        if time is not None:
            time = time.getText()  # .replace('\t', '').replace('\n', '').replace(' ', '')
        else:
            time = ""

        suggestion.suggestion_output["title"] = title
        suggestion.suggestion_output["title_link"] = title_link
        suggestion.suggestion_output["description"] = description
        suggestion.suggestion_output["time"] = time

        suggestion_list.append(suggestion.suggestion_output)

    output = {
        'query': query,
        'suggestions': suggestion_list
    }

    return output


def main_fun(query):
    page = get_search_url(query)
    scraped_data = parse(page, query)

    file = open('everydayhealth-summary.json', 'w', encoding='utf-8')
    json.dump(scraped_data, file, ensure_ascii=False)

    return scraped_data


if __name__ == '__main__':

    query_search_keyword = 'fever'

    output = main_fun(query_search_keyword)

    print('JSON output =====>', output)
