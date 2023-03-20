# 🔥 HN Gems: Commented URLs

Discover the best URLs hidden in top Hacker News comments with this simple Python script that generates an RSS feed of the top comments containing URLs from the latest Hacker News stories.

## Features

- Fetches top 100 Hacker News stories
- Filters comments by minimum score
- Customizable comment depth
- Generates an RSS feed with the latest URLs from top comments
- Avoids duplication by checking for existing feed items

## Requirements

- Python 3.6+
- `requests`
- `feedparser`
- `feedgenerator`
- `tqdm`
- `pytz`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nbanmp/hn-commented-links.git
cd hn-commented-links
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage
Run the script with the default settings:

```bash
python hn_hidden_gems.py
```

The default settings fetch the top 5 comments from each story with a minimum score of 50.

Use the `--depth` and `--min-score` arguments to customize the search:

```bash
python hn_hidden_gems.py --depth 10 --min-score 100
```

This command fetches the top 10 comments from each story with a minimum score of 100.

The script generates an RSS feed file named `www/hn_top_comments_rss.xml` with the latest URLs from top comments. You can use any RSS feed reader to subscribe to the feed and receive updates.

##Contributing
Contributions are welcome! Please submit a pull request or create an issue with your ideas, suggestions, or bug reports.


