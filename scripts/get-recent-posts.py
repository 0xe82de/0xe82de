import os

import requests
from bs4 import BeautifulSoup

TISTORY_BLOG_URL = "https://0xe82de.tistory.com/"


class Post:
    def __init__(self, no, title, date):
        self.no = no
        self.title = title
        self.date = date
        self.link = TISTORY_BLOG_URL + str(no)


def parse_html():
    response = requests.get(TISTORY_BLOG_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    div = soup.find("div", {"id": "recent"})
    return div.find_all("a")


def create_posts(a_tags):
    return [Post(int(a_tag["href"][1:]),
                 a_tag.find("span", {"class": "title"}).text,
                 a_tag.find("span", {"class": "date"}).text)
            for a_tag in a_tags]


def write_contents(contents):
    with open("README.md", "w", encoding="UTF8") as readme:
        for content in contents:
            readme.write(content)
            readme.write("\n")


def create_header():
    FILENAME = "HEADER.md"

    if not os.path.isfile(FILENAME):
        return []

    header = []
    with open(FILENAME, "r") as file:
        header += file.readlines()

    return header


def create_body(posts):
    body = []

    body.append("| no | Title | Date |")
    body.append("| :-: | :-: | :-: |")

    for post in posts:
        body.append("| %d | [%s](%s) | %s |" % (post.no,
                                                post.title,
                                                post.link,
                                                post.date))

    return body


def create_footer():
    FILENAME = "FOOTER.md"

    if not os.path.isfile(FILENAME):
        return []

    footer = [""]
    with open(FILENAME, "r") as file:
        for line in file.readlines():
            footer.append(line.strip())

    return footer


def create_readme(posts):
    contents = []
    contents += create_header()
    contents += create_body(posts)
    contents += create_footer()
    write_contents(contents)


def init():
    os.chdir("../")


if __name__ == "__main__":
    init()
    a_tags = parse_html()
    posts = create_posts(a_tags)
    create_readme(posts)
