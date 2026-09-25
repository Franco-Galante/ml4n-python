import re
from bs4 import BeautifulSoup
from .file_util import cached
from .reference import Reference


def canonicalize(text: str):
    """Remove newlines and extra whitespace with one space."""
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def is_arxiv_link(url: str) -> bool:
    return url.startswith("https://arxiv.org/")

def arxiv_reference(url: str, **kwargs) -> Reference:
    """
    Parse an arXiv reference from a URL (e.g., https://arxiv.org/abs/2005.14165).
    Scrapes the arxiv.org HTML page to extract metadata.
    """
    m = re.search(r'arxiv.org\/...\/(\d+\.\d+)(v\d)?(\.pdf)?$', url)
    if not m:
        raise ValueError(f"Cannot handle this URL: {url}")
    paper_id = m.group(1)

    abs_url = f"https://arxiv.org/abs/{paper_id}"
    html_path = cached(abs_url, "arxiv")
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    def meta(name):
        tag = soup.find("meta", {"name": name})
        return tag["content"] if tag else ""

    title = canonicalize(meta("citation_title"))
    authors_div = soup.find("div", class_="authors")
    if authors_div:
        authors = [canonicalize(a.get_text()) for a in authors_div.find_all("a") if "searchtype=author" in a.get("href", "")]
    else:
        authors = [canonicalize(t["content"]) for t in soup.find_all("meta", {"name": "citation_author"})]
    date = meta("citation_date").replace("/", "-")
    summary = canonicalize(soup.find("meta", {"property": "og:description"})["content"] if soup.find("meta", {"property": "og:description"}) else "")

    return Reference(
        title=title,
        authors=authors,
        url=url,
        date=date,
        description=summary,
        **kwargs,
    )
