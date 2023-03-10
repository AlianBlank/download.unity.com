import ssl
import urllib.request

# download web page
def download_web():
    context = ssl._create_unverified_context()
    url = 'https://unity3d.com/get-unity/download/archive'
    html = urllib.request.urlopen(url, context=context).read()
    fo = open("download.html", "w")
    fo.write(html)
    # close file
    fo.close()
    return html

download_web()