# BBC News Articles Scrapper
## By Ahmed "Asmer" Amen

## Introduction
- This is a Data Engineering Coding Challenge.
- Objective:
    - The goal of this coding challenge is to create a solution that crawls for articles from a news website, cleanses the response, stores it in a mongo database, then makes it available to search via an API.
    

## Specifications
- Write an application to crawl articles on a news website such as [theguardian.com](http://theguardian.com) or [bbc.com](http://bbc.com/) using a crawler framework such as [Scrapy](http://scrapy.org). You can use a crawl framework of your choice and build the application in Python.
- The application should cleanse the articles to obtain only information relevant to the news story, e.g. article text, author, headline, article url, etc. Use a framework such as Readability to cleanse the page of superfluous content such as advertising and HTML.
- Store the data in a hosted Mongo database, e.g. [MongoDB Atlas](https://www.mongodb.com/cloud/atlas), for subsequent search and retrieval. Ensure the URL of the article is included to enable comparison to the original.
- Write an API that provides access to the content in the mongo database.
- Bonus: The user should be able to search the articles' text by keyword.


## Software
- Python3.6.
- Jetbrains Pycharm.
- Scrapy v2.3.0.
- Flask v1.1.2.
- Flask-RESTful v0.3.8
- pymongo v3.6.0


- Use the following command to install Requirements if not installed.
```shell script
# If virtual environment was not created.
python -m venv venv

# If virtual environment was not activated.
# Windows
source venv\Scripts\activate

# Linux & MacOs
source venv\bin\activate

pip install -r requirements.txt
```


## Running and Using
1. Scraper:
    - Follow the instructions below.
    ```shell script
    # If virtual environment was not activated.
    # Windows
    source venv\Scripts\activate
    
    # Linux & MacOs
    source venv\bin\activate
    
    # To run scraper.
    # From outer news directory 
    scrapy crawl news
    ```

2. Flask API:
    - Follow the instructions below.
    ```shell script
    # If virtual environment was not activated.
    # Windows
    source venv\Scripts\activate
    
    # Linux & MacOs
    source venv\bin\activate
    
    # To run Flask app.
    # From api directory 
    python api.py
    ``` 
    
## Project structure
- The project mainly has 2 parts, the main one is the scraper, and the second part is the API.

#### Scraper
1. news/spider:
    - This file has the main logic of the scraping, the flow goes:
        1. It opens the homepage for both BBC news and BBC UK news.
        2. Then extracts the articles links on the homepages, and the news section links like US Election, Coronavirus, World, etc.
        3. It starts scraping the articles from homepage for their data
        4. And visits the sections to get their articles as well.
        5. When scraping the article, the most tricky part is the article text, for these reasons:
            - The schema used vary a lot (over 10 schemas).
            - Links are found between text, causing the extracted string to split on wrong places.
            - Extra escape and non-ascii characters.
        6. Used regex to regenerate the final string as normal as possible. 
        7. Then extracting the title.
        8. After that we extract the author name if exits, and remove the word "By" if found.
        9. The URL is taken from the response object.
        10. And the processed field are saved in the item object to be sent to the pipeline.
 
2. items:
    - Defines the item field to be saved after extraction:
        1. Article Title.
        2. Article Text.
        3. Article Author.
        4. Article URL.
3. pipelines:
    - Responsible of saving the extracted item to the database.
    - Opens connection with the database, and creates the collection "news_data" if not connected.
    - Saves new extracted items.

4. settings:
    - Important modifications:
        1. Enabled random user-agent on line 19.
        2. Enabled pipeline on line 68.
        3. And finally set log level to 'INFO', to limit the log data printed on the screen.
        
#### API
- Flask app with 1 endpoint '/' and 2 methods (GET, POST).
- App runs on port 8008.
- Postman collection with POST and GET request examples is to be found in api directory.
1. GET:
    - Get all the articles data from the "news_data" collection.
    - Response: JSON object with 2 elements: list of the articles and the no. of elements in that list.
2. POST: 
    - Get the query result for keyword from the articles.
    - Body: JSON object with 1 element "query" which is the keyword to use in query.
    - Response: JSON object with 2 elements; list of the query results and the no. of elements in that list.