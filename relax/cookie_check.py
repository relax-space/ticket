from bs4 import BeautifulSoup, Tag
from requests import get


def check(url: str, headers: dict):
    resp = get(url, headers=headers, verify=False)
    txt = resp.text

    btObj = BeautifulSoup(txt, "html.parser")
    span: Tag = btObj.find("span", attrs={"class": "fb f16"})
    if not span:
        return False
    print(span.text)
    return True
