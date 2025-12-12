from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import os
import mimetypes


class Media:
    """Class for operations over the Media

    :Authors:
        Xavier Arnaus <xavi@arnaus.net>

    """

    def get_image_url_from_text(self, text: str) -> str:
        soup = BeautifulSoup(text, 'html.parser')
        img = soup.select('img')
        if img:
            return [{"url": i['src'], "alt_text": i.get('alt', None)} for i in img if i['src']]
        else:
            return None

    def download_from_url(self, url: str, destination_path: str) -> dict:
        parsed_url = urlparse(url)

        result = {
            "file": destination_path.strip("/") + "/" + os.path.basename(parsed_url.path),
            "mime_type": None
        }

        with open(result["file"], 'wb') as handle:
            # Download
            response = requests.get(url, stream=True, allow_redirects=True)

            # Check the response and raise if not OK
            if not response.ok:
                raise RuntimeError(response)

            # Write the binary
            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

        # Get the Mime type from the binary
        discovered_mime = mimetypes.guess_type(url)
        result["mime_type"] = discovered_mime[0] if discovered_mime else None

        return result
