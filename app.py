
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests
import time

app = Flask(__name__)

# ---------- HyRead Crawler ----------
def crawl_hyread(keyword):
    search_url = f"https://web.hyread.com.tw/searchList.jsp?search_field=all&search_input={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    books = []
    for book in soup.select(".search_booklist .bookTitle"):
        link_tag = book.find("a")
        if link_tag:
            title = link_tag.text.strip()
            link = "https://web.hyread.com.tw" + link_tag.get("href")
            books.append({"title": title, "link": link})
    return books

# ---------- UDN Crawler ----------
def crawl_udn(keyword):
    base_url = "https://reading.udn.com/search.do"
    params = {"keyword": keyword}
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    books = []
    for div in soup.select(".book_info_title"):
        link_tag = div.find("a")
        if link_tag:
            title = link_tag.text.strip()
            link = "https://reading.udn.com" + link_tag.get("href")
            books.append({"title": title, "link": link})
    return books

# ---------- Google Search Proxy for Airiti ----------
def crawl_airiti_site_search(keyword):
    search_url = f"https://www.google.com/search?q={keyword}+site:airitibooks.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    books = []
    for link in soup.select("a"):
        href = link.get("href")
        if href and "airitibooks.com" in href:
            books.append({"title": link.text.strip(), "link": href})
    return books

# ---------- Google Search Proxy for CloudLibrary ----------
def crawl_cloudlib_site_search(keyword):
    search_url = f"https://www.google.com/search?q={keyword}+site:cloudlibrary.org"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    books = []
    for link in soup.select("a"):
        href = link.get("href")
        if href and "cloudlibrary.org" in href:
            books.append({"title": link.text.strip(), "link": href})
    return books

# ---------- National Central Library Search (Public Search Site) ----------
def crawl_ncl(keyword):
    search_url = f"https://webpac.ncl.edu.tw/F/?func=find-b&request={keyword}&find_code=WRD"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    books = []
    for row in soup.select("table tr td a"):
        href = row.get("href")
        title = row.text.strip()
        if href and title:
            link = "https://webpac.ncl.edu.tw/F/" + href
            books.append({"title": title, "link": link})
    return books

# ---------- MOC 計次電子書平台 Google 搜尋 ----------
def crawl_moc_ebook(keyword):
    search_url = f"https://www.google.com/search?q={keyword}+site:ebook.moc.gov.tw"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    books = []
    for link in soup.select("a"):
        href = link.get("href")
        if href and "ebook.moc.gov.tw" in href:
            books.append({"title": link.text.strip(), "link": href})
    return books

# ---------- Route ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    keyword = request.args.get("q")
    result = {
        "HyRead": crawl_hyread(keyword),
        "UDN": crawl_udn(keyword),
        "Airiti": crawl_airiti_site_search(keyword),
        "台灣雲端書庫": crawl_cloudlib_site_search(keyword),
        "國家圖書館": crawl_ncl(keyword),
        "文化部計次電子書": crawl_moc_ebook(keyword)
    }
    return render_template("results.html", keyword=keyword, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

