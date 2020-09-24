from flask import Flask, request
from flask_restful import Resource, Api
import pymongo
from bson import json_util
import json

app = Flask(__name__)
api = Api(app)


class NewsAPI(Resource):
    def __init__(self):
        # Private variables
        self.conn = None
        self.collection = None

        # Methods
        self.create_connection()
        self.create_table()

    def create_connection(self):
        """
            Creates connection to the MongoDB "news" database if not connected already.
        :return: None
        """
        if not self.conn:
            self.conn = pymongo.MongoClient(
                "mongodb+srv://asmer_amen:newpassword@cluster0.wjnt1.mongodb.net/news?retryWrites=true&w=majority")

    def create_table(self):
        """
            Creates the database and collection if not created already.
        :return: None
        """
        if not self.collection:
            db = self.conn['news']
            self.collection = db['news_data']

    def query(self, query_text=None):
        """
            Creates Query from the given keyword, issues command to find it and return the list of results.
            If no keyword provides returns all the data.

        :param query_text: The keyword/phrase to query from the database.
        :return: list of dictionaries, each is a query result.
        """
        # Checking if the requested word is somewhere in Article text or title.
        if query_text:
            regex_txt = '.*{}.*'.format(query_text)

            query = {"$or": [
                {
                    'text': {"$regex": regex_txt}
                },
                {
                    'title': {"$regex": regex_txt}
                }
            ]
            }

            # Getting query results, and convert the cursor iterate to a list.
            query_result = list(self.collection.find(query))
        else:
            query_result = list(self.collection.find())

        return query_result

    def get(self):
        """
            Returns all the articles in the database..

        :return: JSON response, 2 elements; list of the articles and the no. of elements in that list.
        """
        result = self.query()
        # Create a dict with the returned list and its length
        result = {
            "count": len(result),
            "data": result
        }

        return json.loads(json_util.dumps(result))

    def post(self):
        """
            API endpoint, receives a body with 1 element query, which is the keyword to query the database for.

        :return: JSON response, 2 elements; list of the query results and the no. of elements in that list.
        """
        body = request.json

        result = self.query(body['query'])

        # Create a dict with the returned list and its length
        result = {
            "count": len(result),
            "data": result
        }

        return json.loads(json_util.dumps(result))


api.add_resource(NewsAPI, '/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
