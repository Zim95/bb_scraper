from scraper import media_sense_news_scraper


def main():
    reuters_urls = [
        'https://news.google.com/search?q=reuters%20sports%20cricket&hl=en-IN&gl=IN&ceid=IN%3Aen'
    ]
    for reuters_url in reuters_urls:
        media_sense_news_scraper.ReuterMediaSenseNewsScraper(reuters_url)()

if __name__ == "__main__":
    main()