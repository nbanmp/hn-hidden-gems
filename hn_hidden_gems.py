import re
import os
import html
import time
import pytz
import argparse
from datetime import datetime
from urllib.parse import urlparse
from typing import List
from tqdm import tqdm

import requests
import feedparser
from feedgenerator import Rss201rev2Feed

# Fetch data from the HN API.
def fetch_api_data(endpoint: str):
    url = f"https://hacker-news.firebaseio.com/v0/{endpoint}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Get the top 100 story IDs.
def get_top_stories() -> List[int]:
    return fetch_api_data("topstories")

# Get an item (comment or story) by ID.
def get_item(item_id: int) -> dict:
    return fetch_api_data(f"item/{item_id}")

# Extract the first URL from a comment's text.
def extract_url(comment: dict) -> str:
    if 'text' not in comment:
        return None

    decoded_text = html.unescape(comment['text'])
    url_match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', decoded_text)
    if url_match:
        comment['text'] = decoded_text
        return url_match.group(0)
    return None

# Get the base domain from a URL.
def get_base_domain(url: str) -> str:
    parsed_uri = urlparse(url)
    return parsed_uri.netloc

# Retrieve the top comments containing a URL.
def get_top_comments_with_url(min_score: int, depth: int):
    top_stories = get_top_stories()[:100]
    comments_with_url = []

    for story_id in tqdm(top_stories, desc="Processing stories"):
        story = get_item(story_id)
        if 'kids' not in story or story['score'] < min_score:
            continue

        top_comments_ids = story['kids'][:-1] if len(story['kids']) < depth else story['kids'][:depth]

        for comment_id in top_comments_ids:
            comment = get_item(comment_id)
            url = extract_url(comment)

            if url and 'kids' in comment:
                base_domain = get_base_domain(url)

                if base_domain not in ["news.ycombinator.com", "archive.ph", "archive.md", "archive.is"]:
                    comment['story_title'] = story['title']
                    comments_with_url.append(comment)

    return comments_with_url


# Read existing feed items to prevent duplicates.
def read_existing_feed_items(filename: str) -> set:
    if not os.path.exists(filename):
        return set()

    existing_feed = feedparser.parse(filename)
    return existing_feed.entries


def generate_rss_feed(comments_with_url, filename):
    existing_items = read_existing_feed_items(filename)

    feed = Rss201rev2Feed(
        title="HN Gems: Commented URLs",
        link="https://news.ycombinator.com/",
        description="The top Hacker News comments containing URLs.",
        language="en",
    )

    # Add existing items to the feed
    for entry in existing_items:
        pubdate = datetime.fromtimestamp(time.mktime(entry.published_parsed)).replace(tzinfo=pytz.UTC)
        feed.add_item(
            title=entry.title,
            link=entry.link,
            description=entry.description,
            author_name=entry.author,
            pubdate=pubdate,
        )

    # Add new items to the feed
    existing_urls = {entry.link for entry in existing_items}
    for comment in comments_with_url:
        url = f"https://news.ycombinator.com/context?id={comment['id']}"
        if url not in existing_urls:
            base_domain = get_base_domain(extract_url(comment))
            discovery_date = datetime.now().replace(microsecond=0).replace(tzinfo=pytz.UTC)
            pub_date = datetime.utcfromtimestamp(comment['time']).replace(tzinfo=pytz.UTC)

            feed.add_item(
                title=f"HN Gem: {base_domain} - {comment['by']}",
                link=url,
                description=f"{comment['text']}<br><small>Posted: {pub_date}</small>",
                author_name=comment['by'],
                pubdate=discovery_date,
            )

    with open(filename, "w") as f:
        f.write(feed.writeString("utf-8"))


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Fetch top HN comments containing URLs")
    parser.add_argument("--depth", type=int, default=5, help="Depth of comments to read on each post (default: 5)")
    parser.add_argument("--min-score", type=int, default=50, help="Minimum score a post should have (default: 50)")
    parser.add_argument("--output", type=str, default="hn_gems.xml", help="Output file path (default: hn_gems.xml)")
    args = parser.parse_args()

    comments_with_url = get_top_comments_with_url(args.min_score, args.depth)
    generate_rss_feed(comments_with_url, filename=args.output)

