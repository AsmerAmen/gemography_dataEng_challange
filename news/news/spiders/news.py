import scrapy
from pprint import pprint

class News(scrapy.Spider):
    # Spider calling name
    name = 'news'
    start_urls = [
        'https://www.bbc.com/news/technology-54244612',
        # 'https://www.bbc.com/news/world-europe-54262279',
        # 'https://www.bbc.com/news/world-us-canada-54258526',
        # 'https://www.bbc.com/news/av/world-54239887'
        'https://www.bbc.com/news/entertainment-arts-54179877'
        ]

    def parse(self, response):

        # Articles have different structure for their main text,
        # And we got 2 types of text,
        #   1. The main body mainly p or b of class e5tfeyi2.
        #   2. Subheads h2 or class e1fj1fc10
        # Example articles: https://www.bbc.com/news/world-europe-54262279 , https://www.bbc.com/news/av/world-54239887
        article_text = response.css(
            '.css-83cqas-RichTextContainer.e5tfeyi2 > p::text,'
            ' .css-83cqas-RichTextContainer.e5tfeyi2 > b::text,'
            ' .css-83cqas-RichTextContainer.e5tfeyi2::text, .css-1jlqpzd-StyledHeading.e1fj1fc10::text'

        ).extract()

        # If the pages doesn't match 1 of the 2 structures above, try the following.
        # Example article: https://www.bbc.com/news/world-us-canada-54258526
        if not article_text:
            article_text = response.css('.story-body__inner').css('p, h2').css('::text').extract()

        # Process the list into one string if extraction was successful.
        article_text = '\n'.join(article_text) if article_text else None

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
        # print(article_text)
        print('\n\n')

