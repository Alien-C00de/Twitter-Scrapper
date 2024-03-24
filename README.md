# Twitter Scraper - Using Python

The Twitter Scraper is a powerful tool designed to scrape tweets from Twitter and generate insightful word clouds. This tool is ideal for data analysts, marketers, and researchers interested in understanding the frequency of word usage in tweets.

## Features

- Scrape tweets from single or multiple Twitter accounts.
- Generate word clouds from tweets to visualize common terms.
- Save scraped data in CSV format for further analysis.

## Prerequisites

Before running the Twitter Scraper, ensure you have the following libraries installed:

```bash
pip install pandas
pip install wordcloud
pip install numpy
pip install matplotlib
pip install Pillow
```

## Usage

Execute the following commands based on your requirements:
- To scrape tweets from a single Twitter account and save the output in CSV format:
   ```bash
   python twitter.py -u elonmusk -l 10
   ```
![image](https://github.com/Alien-C00de/Twitter-Scrapper/assets/138598543/4efd686c-dbb9-45c5-89e9-f64194f88b41)
- To scrape tweets from multiple Twitter accounts listed in a text file:
   ```bash
   python twitter.py -f usernames.txt -l 1
   ```
![image](https://github.com/Alien-C00de/Twitter-Scrapper/assets/138598543/29cf1e58-5cec-45d2-ae76-7790d5ceaad0)
   
- To generate a word cloud from a saved CSV file:
   ```bash
   python twitter.py -w elonmusk_1697470902.csv
   ```
![image](https://github.com/Alien-C00de/Twitter-Scrapper/assets/138598543/f5603ba5-1c63-487f-9a8a-ebf5b26f7c1f)
## Recommendations

- For optimal performance and to prevent potential blocking by Twitter, limit the number of tweets scraped to between 10 and 50.

## Output

The output files will be saved in the following formats:

- CSV files for individual Twitter accounts.
- Word cloud images to visualize the tweet content.

🐦 Happy Twitter scraping and word cloud generation! 🌟
