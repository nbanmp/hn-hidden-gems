import requests
import re
import logging
import html
from datetime import datetime, timedelta
import pytz
from feedgenerator import Rss201rev2Feed
import os
import time
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def get_top_stories():
    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    return response.json()

def get_item(item_id):
    response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json')
    return response.json()

def check_and_add_comment(comment, comments_with_url):
    if 'text' in comment:
        decoded_text = html.unescape(comment['text'])
        if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', decoded_text):
            comment['text'] = decoded_text
            comments_with_url.append(comment)

def get_top_comments_with_url():
    top_stories = get_top_stories()[:100]  # Get the top 100 stories
    comments_with_url = []

    for story_id in tqdm(top_stories, desc="Processing stories"):
        logging.debug(f"Fetching story {story_id}")
        story = get_item(story_id)
        if 'kids' not in story:  # Skip stories without comments
            continue

        top_comments_ids = story['kids'][:10]  # Get the top 10 comments

        for comment_id in top_comments_ids:
            logging.debug(f"Fetching comment {comment_id}")
            comment = get_item(comment_id)
            check_and_add_comment(comment, comments_with_url)

            # Check top response for URL
            if 'kids' in comment:
                top_response_id = comment['kids'][0]
                logging.debug(f"Fetching top response {top_response_id}")
                top_response = get_item(top_response_id)
                check_and_add_comment(top_response, comments_with_url)

    return comments_with_url

def generate_rss_feed(comments_with_url, filename="hn_top_comments_rss.xml"):
    feed = Rss201rev2Feed(
        title="Top HN Comments with URL",
        link="https://news.ycombinator.com/",
        description="The top Hacker News comments containing URLs.",
        language="en",
    )

    for comment in comments_with_url:
        comment_url = f"https://news.ycombinator.com/item?id={comment['id']}"
        pubdate = datetime.fromtimestamp(comment['time'], pytz.utc)
        feed.add_item(
            title=f"Comment by {comment['by']} on {pubdate.strftime('%Y-%m-%d %H:%M:%S')}",
            link=comment_url,
            description=comment['text'],
            pubdate=pubdate,
        )

    with open(filename, "w") as f:
        feed.write(f, "utf-8")

def main():
    while True:
        logging.info("Fetching top comments with URL")
        comments_with_url = get_top_comments_with_url()
        logging.info("Generating RSS feed")
        generate_rss_feed(comments_with_url)
        logging.info("RSS feed generated, waiting for the next run")
        time.sleep(3600)  # Wait for 1 hour (3600 seconds)

if __name__ == '__main__':
    main()
