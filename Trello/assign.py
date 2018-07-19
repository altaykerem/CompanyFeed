import os
import requests

board_id = os.environ.get("trello_board")
list_id = os.environ.get("trello_list")
api_key = os.environ.get("trello_api")
token = os.environ.get("trello_token")


def add_assignment(domain):
    # Create card
    url = "https://api.trello.com/1/cards"
    desc = "Company assinged for this week"

    querystring = {"name": domain, "desc": desc, "idList": list_id, "keepFromSource": "all",
                   "key": api_key, "token": token}
    return requests.request("POST", url, params=querystring)
