# Information search crawler project

Crawls ria.ru with scrapy

## Usage

### Crawler

1. `pip install -r requirements.txt`
2. Set up `splash` instance, e.g. `docker run -p 8050:8050 scrapinghub/splash`
3. `scrapy crawl article_spider`

### Stemmer

1. Crawl data
2. run [stemmer.py](./stemming/stemmer.py)

### Inverted index search

1. Run stemmer on some data
2. Run [search.py](./inverted_index/search.py)
3. Enter search query 
4. A list of article titles will be returned sorted by total term count