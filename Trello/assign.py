import os
import requests

board_id = "5b27f88ba97dd9992a5ae9a7"
list_id = "5b27f896f0377cbab70b7674"
api_key = os.environ.get("trello_api")
token = os.environ.get("trello_token")

# Request board
url = "https://api.trello.com/1/boards/"+board_id
querystring = {"key": api_key, "token": token}
response = requests.request("GET", url, params=querystring)
print(response.text)

# Create card
url = "https://api.trello.com/1/cards"
desc = "Company assinged for you this week"

querystring = {"name": "<name>", "desc": desc, "idList": list_id, "keepFromSource": "all",
               "key": api_key, "token": token}
response = requests.request("POST", url, params=querystring)
print(response.text)
