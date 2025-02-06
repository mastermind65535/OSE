import requests
import json
from bs4 import BeautifulSoup
import re

class Account:
    def __init__(self, handle: str):
        self.handle = handle
    
    def fetch(self):
        url = f"https://youtube.com/@{self.handle}/about"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, 'html.parser')
        data = re.search(r"var ytInitialData = ({.*?});</script>", str(soup), re.DOTALL).group(1)
        json_data = json.loads(data)

        # Title
        title_tag = soup.find("meta", {"property": "og:title"})
        title = title_tag["content"] if title_tag else ""

        # Description
        description_tag = soup.find("meta", {"property": "og:description"})
        description = description_tag["content"] if description_tag else ""

        # Published Date (Joined Date)
        published_at_tag = soup.find("span", string=re.compile("Joined"))
        published_at = published_at_tag.text if published_at_tag else ""

        # Custom URL
        custom_url_tag = soup.find("link", {"rel": "canonical"})
        custom_url = custom_url_tag["href"] if custom_url_tag else ""

        # View Count
        view_count_tag = soup.find("span", string=re.compile("views"))
        view_count = int(view_count_tag.text.split()[0].replace(",", "")) if view_count_tag else 0

        # Subscriber Count
        subscriber_count_tag = soup.find("yt-formatted-string", {"id": "subscriber-count"})
        subscriber_count = int(subscriber_count_tag.text.split()[0].replace(",", "")) if subscriber_count_tag else 0

        # Video Count
        video_count_tag = soup.find("span", string=re.compile("videos"))
        video_count = int(video_count_tag.text.split()[0].replace(",", "")) if video_count_tag else 0

        # Banner Image URL
        profile_image_tag = soup.find("meta", {"property": "og:image"})
        profile_image_url = profile_image_tag["content"] if profile_image_tag else ""

        banner_image_url = json_data["header"]["pageHeaderRenderer"]["content"]["pageHeaderViewModel"]["banner"]["imageBannerViewModel"]["image"]["sources"]

        # Keywords
        keywords_tag = soup.find("meta", {"name": "keywords"})
        keywords = keywords_tag["content"] if keywords_tag else ""

        # Construct JSON response
        channel_info = {
            "channel_id": custom_url.split("/")[-1] if custom_url else "",
            "title": title,
            "description": description,
            "published_at": published_at,
            "custom_url": custom_url,
            "view_count": view_count,
            "subscriber_count": subscriber_count,
            "video_count": video_count,
            "profileImg": profile_image_url,
            "bannerImg": banner_image_url,
            "keywords": keywords,

        }

        # return json.dumps(json_data, indent=4)

        return json.dumps(channel_info, indent=4)