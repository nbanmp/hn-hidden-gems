# 🔥 HN Gems: Commented URLs

Discover the best URLs hidden in top Hacker News comments with this simple Python script that generates an RSS feed of the top comments containing URLs from the latest Hacker News stories.

RSS feed hosted here: https://hn.invades.space/hn_gems_rss.xml

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
To generate the RSS feed with the top HN comments containing URLs, run the following command:

```bash
python hn_hidden_gems.py [--depth DEPTH] [--min-score MIN_SCORE] [--output OUTPUT]
```

Optional arguments:

- `--depth DEPTH`: Depth of comments to read on each post (default: 5)
- `--min-score MIN_SCORE`: Minimum score a post should have (default: 50)
- `--output OUTPUT`: Output file path (default: `hn_gems.xml`)

Example:

```bash
python hn_hidden_gems.py --depth 5 --min-score 50 --output my_output_file.xml
```

This command will generate an RSS feed with the top comments containing URLs from the top stories and save it to the specified output file (my_output_file.xml).

You can then use an RSS reader to subscribe to the generated feed and discover interesting content shared in the comments on Hacker News.


##Contributing
Contributions are welcome! Please submit a pull request or create an issue with your ideas, suggestions, or bug reports.
