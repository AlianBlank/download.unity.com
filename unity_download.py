import ssl
import urllib.request
import requests


# download web page
def download_web():
    url = 'https://unity.com/releases/editor/archive'
    html = requests.get(url)
    # context = ssl._create_unverified_context()

    # html = urllib.request.urlopen(url, context=context).read()
    fo = open("download.html", "w", encoding="utf-8")
    fo.write(html.text)
    # close file
    fo.close()
    return html


download_web()
