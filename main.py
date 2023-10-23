import sys
import re
import requests
from bs4 import BeautifulSoup


TO_CRAWL = []
CRAWLED = set()
COLLECTED_EMAILS = set()


def request(url):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
    try:
        response = requests.get(url, headers=header)
        return response.text
    except KeyboardInterrupt:
        print("\nProgram interrupted by the user.")
        sys.exit()
    except:
        pass


def get_emails(html):
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", html)
    return emails


def get_links(html):
    links = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        tags_a = soup.find_all("a", href=True)
        if tags_a is not None:
            for tag in tags_a:
                link = tag["href"]
                if link.startswith("http"):
                    links.append(link)
        return links
    except:
        pass


def crawl():
    try:
        while TO_CRAWL:
            url = TO_CRAWL.pop()
            html = request(url)
            if html:
                emails = get_emails(html)
                for email in emails:
                    if email not in COLLECTED_EMAILS:
                        COLLECTED_EMAILS.add(email)
                        print(email)
                links = get_links(html)
                if links:
                    for link in links:
                        if link not in CRAWLED and link not in TO_CRAWL:
                            TO_CRAWL.append(link)
                CRAWLED.add(url)
            else:
                CRAWLED.add(url)
        print("Done!")
    except KeyboardInterrupt:
        print("\nProgram interrupted by the user.")


if __name__ == "__main__":
    url = sys.argv[1]
    TO_CRAWL.append(url)
    crawl()
