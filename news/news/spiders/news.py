import scrapy
from ..items import NewsItem
import re


def is_good_url(url):
    # ideas and world_radio_and_tv are mainly videos.
    # 'sounds/play' are podcasts.
    for exclude in ['ideas', 'sounds/play', 'news/world_radio_and_tv']:
        if exclude in url:
            return False
    return True


class News(scrapy.Spider):
    # Spider calling name
    name = 'news'
    start_urls = [
        'https://www.bbc.co.uk/news',
        'https://www.bbc.com/news'
    ]

    def parse(self, response):
        # First page, extracts the articles' links and the sections links.
        # Redirect these links to their parsing functions, if they don't have specific words in them, which imply the
        # main content of the link is video or audio.
        articles_links = response.css('.gs-c-promo-heading.gs-o-faux-block-link__overlay-link.gel-pica-bold'
                                      '.nw-o-link-split__anchor::attr(href)').extract()

        sections_links = response.css('.nw-c-nav__wide a::attr(href)').extract()

        for link in articles_links:
            if is_good_url(link):
                yield response.follow(link, self.parse_article)

        for link in sections_links:
            if is_good_url(link):
                yield response.follow(link, self.parse_section)

    def parse_section(self, response):
        articles_links = response.css('.gs-c-promo-heading.gs-o-faux-block-link__overlay-link.gel-pica-bold'
                                      '.nw-o-link-split__anchor::attr(href)').extract()
        for link in articles_links:
            if is_good_url(link):
                yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        item = NewsItem()

        # Article text section

        # Articles have different structures for their main text,
        article_text = response.css(
            '.css-83cqas-RichTextContainer.e5tfeyi2, .css-1jlqpzd-StyledHeading.e1fj1fc10,'
            ' .LongArticle-body .Text.gel-body-copy'
        ).css('::text').extract()

        # If the pages doesn't match 1 of the 2 structures above, try the following.
        # Example article: https://www.bbc.com/news/world-us-canada-54258526
        if not article_text:
            article_text = response.css('.story-body__inner').css('p, h2').css('::text').extract()

        # If the pages doesn't match any of the structures above, try the following.
        if not article_text:
            article_text = response.css('.qa-story-body.story-body p').css(' ::text').extract()

        if not article_text:
            article_text = response.css(
                '.article__body-content'
                ' .body-text-card__text.body-text-card__text--future.body-text-card__text--flush-text,'
                ' .article-body__pull-quote').css(' ::text').extract()

        if not article_text:
            article_text = response.css('.body-content p, blockqoute').css(' ::text').extract()

        if not article_text:
            article_text = response.css(
                '.Theme-Layer-BodyText p, .Theme-SubTitle.Theme-TextSize-xxsmall').css(' ::text').extract()

        if not article_text:
            article_text = response.css(
                '.gel-body-copy.sp-c-media-collection_body-copy p').css(' ::text').extract()

        if not article_text:
            article_text = response.css(
                '.newsround-story-body__content .newsround-story-body__text, .newsround-story-body__crosshead'
            ).css(' ::text').extract()

        # Process the list into one string if extraction was successful.
        # Remove the style parts selected by mistake, since we need multiple levels of text extraction.
        article_text = '\n'.join(
            [line.replace(u'\xa0', u' ') for line in article_text if '.css' not in line and line is not '\n']
        ) if article_text else None

        # Reshaping the string, which maybe distorted because embed links.
        if article_text:
            article_text = re.sub(r'\n and \n', ' and ', article_text)
            article_text = re.sub(r'\nand \n', 'and ', article_text)
            article_text = re.sub(r' \n', ' ', article_text)
            article_text = re.sub(r'\n,', ',', article_text)
            article_text = re.sub(r'\n.\n', '.\n', article_text)

        # Article title section

        # Extract and process title
        article_title = response.css(
            'h1,'
            ' .article-headline__text.b-reith-sans-font,'
            ' title').css('::text').extract()
        article_title = article_title[0] if article_title else None

        # Article author section

        # Extract and process Author if it was present.
        article_author = response.css(
            '.css-15hnagr-Contributor.e5xb54n0,'
            ' .byline__name,'
            ' .Info-authorName.gel-long-primer,'
            ' .author-unit__text.b-font-family-serif,'
            ' .source-attribution-author .index-body,'
            ' .Theme-Byline,'
            ' .Theme-Layer-BodyText--inner p.h-align-center,'
            ' .qa-contributor-name.gel-long-primer').css(' ::text').extract()
        article_author = article_author[0].replace('By', '').strip() if article_author else None

        # URL extracted from the response object
        article_url = response.url

        # Save details
        item['title'] = article_title
        item['text'] = article_text
        item['author'] = article_author
        item['url'] = article_url

        yield item

