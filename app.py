from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs


def _safe_get(url, headers):
    """Perform a GET request with basic error handling."""
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return res.text
    except requests.RequestException:
        return None


def _extract_google_url(href):
    """Google search links contain tracking parameters. Strip them."""
    if href.startswith("/url?"):
        qs = parse_qs(urlparse(href).query)
        url = qs.get("q")
        if url:
            return url[0]
    return href


def google_site_search(keyword, domain):
    """Query Google for a specific domain and return a list of results."""
    search_url = f"https://www.google.com/search?q={keyword}+site:{domain}"
    headers = {"User-Agent": "Mozilla/5.0"}
    body = _safe_get(search_url, headers)
    if body is None:
        return []

    soup = BeautifulSoup(body, "html.parser")
    books = []
    for link in soup.select("a"):
        href = link.get("href")
        if href and domain in href:
            books.append({"title": link.text.strip(), "link": _extract_google_url(href)})
    return books

app = Flask(__name__)

# ---------- HyRead Crawler (Google site search) ----------
def crawl_hyread(keyword):
    return google_site_search(keyword, "web.hyread.com.tw")

# ---------- UDN Crawler (Google site search) ----------
def crawl_udn(keyword):
    return google_site_search(keyword, "reading.udn.com")

# ---------- Airiti 電子書（Google site search）----------
def crawl_airiti_site_search(keyword):
    return google_site_search(keyword, "airitibooks.com")

# ---------- 台灣雲端書庫（Google site search）----------
def crawl_cloudlib_site_search(keyword):
    return google_site_search(keyword, "cloudlibrary.org")

# ---------- 國家圖書館 WebPAC（Google site search）----------
def crawl_ncl(keyword):
    return google_site_search(keyword, "webpac.ncl.edu.tw")

# ---------- 文化部計次電子書（Google site search）----------
def crawl_moc_ebook(keyword):
    return google_site_search(keyword, "ebook.moc.gov.tw")

# ---------- 路由 ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    keyword = request.args.get("q", "").strip()
    if not keyword:
        return render_template("index.html", error="請輸入關鍵字")
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