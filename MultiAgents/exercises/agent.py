import requests
from bs4 import BeautifulSoup

CHANNEL_ID = "UCAW-NpUFkMyCNrvRSSGIvDQ"
url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

resp = requests.get(url, timeout=10)
print("status:", resp.status_code)
print(resp.text[:300])

soup = BeautifulSoup(resp.text, "xml")
entries = soup.find_all("entry")
print("videos in feed:", len(entries))
if entries:
    print("latest title:", entries[0].find("title").text)