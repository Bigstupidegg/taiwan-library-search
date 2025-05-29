from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# ---------- HyRead Crawler (Google site search) ----------
def crawl_hyread(keyword):
    search_url = f"https://www.google.com/search?q={keyword}+site:web.hyread.com.tw"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    books = []
    for link in soup.select("a"):
        href = link.get("href")
        if href and "web.hyread.com.tw" in href:
            books.append({"title": link.text.strip(), "link": href})
    return books

# ---------- UDN Crawler (Google site search) ----------
def crawl_udn(keyword):
    search_url = f"https://www.google.com/search?q={keyword}+site:reading.udn.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    books = []
    for link in soup.select("a"):
        href = link.get("href")
        if href and "reading.udn.com" in href:
            books.append({"title": link.text.strip(), "link": href})
    return books

# ---------- Airiti 電子書（Google site search）----------
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

# ---------- 台灣雲端書庫（Google site search）----------
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

# ---------- 國家圖書館 WebPAC（Google site search）----------
def crawl_ncl(keyword):
    search_url = f"https://www.google.com/search?q={keyword}+site:webpac.ncl.edu.tw"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    books = []
    for link in soup.select("a"):
        href = link.get("href")
        if href and "webpac.ncl.edu.tw" in href:
            books.append({"title": link.text.strip(), "link": href})
    return books

# ---------- 文化部計次電子書（Google site search）----------
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

# ---------- 路由 ----------
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