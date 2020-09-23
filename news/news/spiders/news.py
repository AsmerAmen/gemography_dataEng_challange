import scrapy
from pprint import pprint
import re

class News(scrapy.Spider):
    # Spider calling name
    name = 'news'
    start_urls = [
        # 'https://www.bbc.com/news/technology-54244612',
        # 'https://www.bbc.com/news/world-europe-54262279',
        # 'https://www.bbc.com/news/world-us-canada-54258526',
        # 'https://www.bbc.com/news/av/world-54239887',
        # 'https://www.bbc.com/news/entertainment-arts-54179877',
        # 'https://www.bbc.com/news/world-middle-east-54235209',
        # 'https://www.bbc.com/sport/football/54262570',
        # 'https://www.bbc.com/sport/football/54259386',
        # 'https://www.bbc.com/news/world-us-canada-54254141',
        'https://www.bbc.com/news/world-54218131'
        ]

    def parse(self, response):

        # Articles have different structure for their main text,
        # And we got 2 types of text,
        #   1. The main body mainly p or b of class e5tfeyi2.
        #   2. Subheads h2 or class e1fj1fc10
        # Example articles: https://www.bbc.com/news/world-europe-54262279 , https://www.bbc.com/news/av/world-54239887
        article_text = response.css(
            ' .css-83cqas-RichTextContainer.e5tfeyi2, .css-1jlqpzd-StyledHeading.e1fj1fc10'
        ).css('::text').extract()

        # If the pages doesn't match 1 of the 2 structures above, try the following.
        # Example article: https://www.bbc.com/news/world-us-canada-54258526
        if not article_text:
            article_text = response.css('.story-body__inner').css('p, h2').css('::text').extract()

        # If the pages doesn't match any of the structures above, try the following.
        # Example article: https://www.bbc.com/sport/football/54262570
        if not article_text:
            article_text = response.css('.qa-story-body.story-body p').css(' ::text').extract()

        # Process the list into one string if extraction was successful.
        # Remove the style parts selected by mistake, since we need multiple levels of text extraction.
        article_text = '\n'.join([line for line in article_text if '.css' not in line]) if article_text else None

        # Reshaping the string, which maybe distorted because embed links.
        if article_text:
            article_text = re.sub(r'\nand \n', 'and ', article_text)
            article_text = re.sub(r' \n', ' ', article_text)
            article_text = re.sub(r'\n,', ',', article_text)
            article_text = re.sub(r'\n.\n', '.\n', article_text)

        # article_text = article_text.replace('\nand\n', ' and ')
        # Extract and process title
        article_title = response.css('h1::text').extract()
        article_title = article_title[0] if article_title else None

        # Extract and process Author if it was present.
        article_author = response.css('.css-15hnagr-Contributor.e5xb54n0, .byline__name').css(' ::text').extract()
        article_author = article_author[0].replace('By', '').strip() if article_author else None

        #
        article_url = response.url

        print(article_title)
        print(article_author)
        print('\n')
        print(article_text)
        print('\n\n')

