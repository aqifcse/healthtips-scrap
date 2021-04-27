from lxml import html
from requests_html import HTMLSession
from collections import OrderedDict
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import json


def get_search_url(query_search_keyword):

    query_search_url = "https://www.verywellhealth.com/search?q=%s" % query_search_keyword

    print(query_search_url)
    session = HTMLSession()
    query_resp = session.get(query_search_url)
    query_soup = BeautifulSoup(query_resp.text, "lxml")

    return query_soup


def parse(page, query):
    # print(page)

    suggestions = page.find_all(
        "li", attrs={"class": "loc item search-result-list-item"}
    )
    print(suggestions)
    suggestion_list = []

    for suggestion in suggestions:

        suggestion.suggestion_output = {
            "title": '',
            "title_link":  '',
            "description": '',
            # "time": ''
        }

        title = suggestion.find(
            "div", attrs={"class": "block__title"}
        )
        if title is not None:
            title = title.getText().replace('\n', '')  # .replace(' ', '')
        else:
            title = ""

        title_link = suggestion.find(
            "a", attrs={"id": "block_2-0"}
        )
        if title_link is not None:
            title_link = title_link.get('href')
        else:
            title_link = ""

        description = suggestion.find(
            "p", attrs={"class": "block__excerpt"})
        if description is not None:
            description = description.getText().replace('\n', '')
        else:
            description = ""

        # time = suggestion.find("time", attrs={"class": "result-item__date"})
        # if time is not None:
        #     time = time.getText()  # .replace('\t', '').replace('\n', '').replace(' ', '')
        # else:
        #     time = ""

        suggestion.suggestion_output["title"] = title
        suggestion.suggestion_output["title_link"] = title_link
        suggestion.suggestion_output["description"] = description
        #suggestion.suggestion_output["time"] = time

        suggestion_list.append(suggestion.suggestion_output)

    suggestion_list.pop(0)

    output = {
        'query': query,
        'suggestions': suggestion_list
    }

    return output


def main_fun(query):
    page = get_search_url(query)
    scraped_data = parse(page, query)

    file = open('verywellhealth-summary.json', 'w', encoding='utf-8')
    json.dump(scraped_data, file, ensure_ascii=False)

    return scraped_data


if __name__ == '__main__':

    query_search_keyword = 'fever'

    output = main_fun(query_search_keyword)

    print('JSON output =====>', output)
