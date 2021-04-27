from lxml import html
from requests_html import HTMLSession
from collections import OrderedDict
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import json


def get_search_url(query_search_keyword):

    query_search_url = (
        "https://www.whattoexpect.com/pregnancy/week-by-week/%s.aspx"
        % query_search_keyword
    )

    print(query_search_url)
    session = HTMLSession()
    query_resp = session.get(query_search_url)
    query_soup = BeautifulSoup(query_resp.text, "lxml")

    return query_soup


def parse(page, query):
    # print(page)

    video_transcript = page.find("div", attrs={"id": "videoTranscript"})
    if video_transcript is not None:
        video_transcript = video_transcript.getText()
    else:
        video_transcript = ""

    # print(video_transcript)

    at_a_glance_items = page.find_all(
        "div", attrs={"class": "your-baby__dev__descr-c__items__item"}
    )

    for at_a_glance_item in at_a_glance_items:
        at_a_glance_headline = at_a_glance_item.find(
            "div", attrs={"class": "your-baby__dev__descr-c__items__item__body-c__headline"})
        if at_a_glance_headline is not None:
            at_a_glance_headline = at_a_glance_headline.getText()
        else:
            at_a_glance_headline = ""

        # print(at_a_glance_headline)

        at_a_glance_body = at_a_glance_item.find(
            "div", attrs={"class": "your-baby__dev__descr-c__items__item__body-c__body"})
        if at_a_glance_body is not None:
            at_a_glance_body = at_a_glance_body.getText()
        else:
            at_a_glance_body = ""

        # print(at_a_glance_body)

    baby_development_info_headers = page.find(
        "div", attrs={"id": "lightbox-inline-form-79fdff90-8a54-40e6-9db7-30b6ef1dd207"}
    ).find_next().find_all("h3")
    for baby_development_info_header in baby_development_info_headers:
        if baby_development_info_header is not None:
            baby_development_info_header = baby_development_info_header.getText()
        else:
            baby_development_info_header = ""
        # print(baby_development_info_header)

    baby_development_info_paragraphs = page.find(
        "div", attrs={"id": "lightbox-inline-form-79fdff90-8a54-40e6-9db7-30b6ef1dd207"}
    ).find_next().find_all("p")
    for baby_development_info_paragraph in baby_development_info_paragraphs:
        if baby_development_info_paragraph is not None:
            baby_development_info_paragraph = baby_development_info_paragraph.getText()
        else:
            baby_development_info_paragraph = ""
        # print(baby_development_info_paragraph)

    # your body
    your_body_headline = page.find(
        "h2", attrs={"class": "your-body__headline"}
    )
    if your_body_headline is not None:
        your_body_headline = your_body_headline.getText()
    else:
        your_body_headline = ""

    your_body_info_headers = page.find(
        "div", attrs={"class": "your-body__body"}
    ).find_all("h3")
    for your_body_info_header in your_body_info_headers:
        if your_body_info_header is not None:
            your_body_info_header = your_body_info_header.getText()
        else:
            your_body_info_header = ""
        # print(your_body_info_header)

    your_body_info_paragraphs = page.find(
        "div", attrs={"class": "your-body__body"}
    ).find_all("p")
    for your_body_info_paragraph in your_body_info_paragraphs:
        if your_body_info_paragraph is not None:
            your_body_info_paragraph = your_body_info_paragraph.getText()
        else:
            your_body_info_paragraph = ""
        # print(your_body_info_paragraph)

    # return output


def main_fun(query):
    page = get_search_url(query)
    scraped_data = parse(page, query)

    file = open("whattoexpect-%s-tips.json" % query, "w", encoding="utf-8")
    json.dump(scraped_data, file, ensure_ascii=False)

    return scraped_data


if __name__ == "__main__":

    query_search_keyword = "weeks-1-and-2"

    # query_search_keyword = "week-3"

    output = main_fun(query_search_keyword)

    print("JSON output =====>", output)


# print(baby_developent_informations)

    # print(baby_developent_info)

    # suggestions = page.find_all(
    #     "li", attrs={"class": "loc item search-result-list-item"}
    # )
    # print(suggestions)
    # suggestion_list = []

    # for suggestion in suggestions:

    #     suggestion.suggestion_output = {
    #         "title": "",
    #         "title_link": "",
    #         "description": "",
    #         # "time": ''
    #     }

    #     title = suggestion.find("div", attrs={"class": "block__title"})
    #     if title is not None:
    #         title = title.getText().replace("\n", "")  # .replace(' ', '')
    #     else:
    #         title = ""

    #     title_link = suggestion.find("a", attrs={"id": "block_2-0"})
    #     if title_link is not None:
    #         title_link = title_link.get("href")
    #     else:
    #         title_link = ""

    #     description = suggestion.find("p", attrs={"class": "block__excerpt"})
    #     if description is not None:
    #         description = description.getText().replace("\n", "")
    #     else:
    #         description = ""

    #     # time = suggestion.find("time", attrs={"class": "result-item__date"})
    #     # if time is not None:
    #     #     time = time.getText()  # .replace('\t', '').replace('\n', '').replace(' ', '')
    #     # else:
    #     #     time = ""

    #     suggestion.suggestion_output["title"] = title
    #     suggestion.suggestion_output["title_link"] = title_link
    #     suggestion.suggestion_output["description"] = description
    #     # suggestion.suggestion_output["time"] = time

    #     suggestion_list.append(suggestion.suggestion_output)

    # suggestion_list.pop(0)

    # output = {"query": query, "suggestions": suggestion_list}
