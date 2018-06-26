import os
import requests
import json


class Query:
    currentPage = 0
    hasNextPage = True
    totalResults = None

    api_base = ""
    api_key = ""

    # Create query adds page information into the query
    page_map = [', after: "0|50"', ', after: "1|50"', ', after: "2|50"', ', after: "3|50"', ', after: "4|50"',
                ', after: "5|50"', ', after: "6|50"', ', after: "7|50"', ', after: "8|50"', ', after: "9|50"',
                ', after: "10|50"']

    def __init__(self):
        # Get config
        self.api_base = os.environ.get("mattermark_api")
        self.api_key = os.environ.get("api_key")

    def create_query(self):
        return ""

    def query(self):
        # Create Header
        auth = 'Bearer ' + self.api_key
        header = {'Content-Type': 'application/graphql', 'Authorization': auth, 'Accept': 'application/json'}

        # Create Query String
        query_str = self.create_query()

        # Send Request
        try:
            response = requests.post(url=self.api_base, headers=header, data=query_str)
            if response.status_code == requests.codes.ok:
                print("Request is successful with code {} ...".format(response.status_code))
                return json.loads(response.content)
            else:
                print("Error in response: {}".format(response.raise_for_status()))
        except Exception as e:
            print("Problem while sending request: {}".format(e))
            return
