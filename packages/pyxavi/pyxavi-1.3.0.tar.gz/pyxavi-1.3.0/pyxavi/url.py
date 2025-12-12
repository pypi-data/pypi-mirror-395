from urllib.parse import urlparse
import validators
import requests
import feedparser
from bs4 import BeautifulSoup as bs4


class Url:

    @staticmethod
    def clean(url, remove_components: dict = None) -> str:

        if remove_components is None:
            remove_components = {}

        to_remove = {
            "scheme": False,
            "netloc": False,
            "path": False,
            "params": False,
            "query": False,
            "fragment": False
        }
        to_remove = {**to_remove, **remove_components}

        parsed = urlparse(url)

        if to_remove["scheme"] is True:
            parsed = parsed._replace(scheme="")
        if to_remove["netloc"] is True:
            parsed._replace(netloc="")
        if to_remove["path"] is True:
            parsed = parsed._replace(path="")
        if to_remove["params"] is True:
            parsed = parsed._replace(params="")
        if to_remove["query"] is True:
            parsed = parsed._replace(query="")
        if to_remove["fragment"] is True:
            parsed = parsed._replace(fragment="")

        return parsed.geturl()

    @staticmethod
    def is_valid(url: str) -> bool:
        return True if validators.url(url) else False

    @staticmethod
    def ensure_absolute(url: str, base: str) -> str:
        # Is this URL relative? then add the base
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.hostname:
            url = base + url

        return url

    @staticmethod
    def findfeeds(url: str):
        """
        It returns a list of URLs found in the given site's URL that have entries.
        so be prepared to receive an array.

        In case that the feed url is already found in the HEAD, we ignore the BODY

        kindly adapted from
          https://alexmiller.phd/posts/python-3-feedfinder-rss-detection-from-url/
        What I added:
          1. Send a HEAD first, so we can follow redirections
          2. Do not search within the body, only the LINK inside the HEAD
          3. Add the base URL in case the RSS link is relative
          4. Sort, I want RSS mainly
          5. HEAD wins, if present
        """

        def by_priority(element):
            prio_value = 9
            if "rss" in element:
                prio_value = 1
            elif "atom" in element:
                prio_value = 3
            return prio_value

        # Get the header first, so we know if there is a redirection
        r = requests.head(url, allow_redirects=True)

        # Now get the content from the real URL
        raw = requests.get(r.url).text
        result = []

        # Prepare the base URL, as sometimes the Feed comes relative
        parsed_url = urlparse(url)
        base = parsed_url.scheme + "://" + parsed_url.hostname

        # We'll parse the HTML using beautifulsoup
        html = bs4(raw, features="html.parser")

        # The "link" tags that are rel="alternate" may contain the feed
        feed_urls = html.find_all("link", rel="alternate")
        print(feed_urls)
        if len(feed_urls) >= 1:
            for f in feed_urls:
                # They have to have a "type" attribute
                t = f.get("type", None)
                # if ther's a type and it's what we want
                if t and ("rss" in t or "xml" in t):
                    href = f.get("href", None)
                    # If we have an url and it's a valid feed
                    #   we add it into the resulting list if not there yet
                    if href:
                        href = Url.ensure_absolute(url=href, base=base)
                        # If it's a valid feed and not there yet
                        #   we add it into the resulting list
                        if Url.is_a_valid_feed(href) and href not in result:
                            result.append(href)

        # We continue throug the BODY only if we didn't find any feed yet
        if len(result) == 0:
            # In case we don't
            #
            # Search for "a" tags in the body
            atags = html.find_all("a")
            for a in atags:
                href = a.get("href", None)
                # If we have a href and contains any "feed" text and
                #   we add it into the resulting list if not there yet
                if href and ("xml" in href or "rss" in href or "feed" in href):
                    href = Url.ensure_absolute(url=href, base=base)
                    # If it's a valid feed and not there yet
                    #   we add it into the resulting list
                    if Url.is_a_valid_feed(href) and href not in result:
                        result.append(href)

        # Finally, apply sorting, as RSS are more prio than Atom...
        result = sorted(result, key=by_priority)

        # Return the list found!
        return (result)

    @staticmethod
    def is_a_valid_feed(url) -> bool:
        f = feedparser.parse(url)
        return len(f.entries) > 0
