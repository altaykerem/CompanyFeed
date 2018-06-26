import os
import requests

# Get mattermark configuration
api_key = os.environ.get("api_key")
base = os.environ.get("mattermark_api")

# Url's
# company search endpoint
companies_url = base + "/companies"

# Payload
# add payload to request along with mattermark uri
# ##FOR PARAMETER REFERENCE
# https://docs.mattermark.com/rest_api/companies_list/index.html
companies_payload = {
    "key":      api_key,

    # amount returned
    "page":     1,
    "per_page": 50,

    # search parameters
    "industries":       "e-commerce|cloud computing|finance|banking|enterprise software|payments",
    "country":          "USA|CAN",
    "momentum_score":   "1000~",
    "mattermark_score": "1000~"
}


# get a list of companies from mattermark
# returns 50 companies each time it's called
def get_companies(payload):
    # mattermark call
    print("Getting companies, page 1")
    response = requests.get(companies_url, params=payload)
    response.raise_for_status()

    return response.json()


def write_results(companies_json):
    # Write results
    wfile = open("query_results.txt", "w")
    wfile.write("Check these out\n")
    for company in companies_json["companies"]:
        wfile.write("Company name: "+company["company_name"]+", domain: "+company["domain"]+"\n")
    wfile.close()


def write_mm_result():
    companies = get_companies(companies_payload)
    write_results(companies)


"""     example payload
companies_payload = {
    "key":      api_key,

    # amount returned
    "page":     1,
    "per_page": 50,

    # search parameters
    "industries":       "e-commerce|cloud computing|finance|banking|enterprise software|payments",
    "employees":        "1~50",
    "total_funding":    "1000000",
    "added_date":       "2018-01-01~",
    "est_founding_date": "within 1 year",
    "state":            "CA"
}
"""