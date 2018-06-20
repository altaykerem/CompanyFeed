import requests
from MatterMark import dd_utils

# Get mattermark configuration
config = dd_utils.get_config()
api_key = dd_utils.get_api_key(config)
base = dd_utils.get_uri(config)

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
    "stage":            "Pre Series A",
    "employees":        "1~100",
    "country":          "USA|CAN",
    "mattermark_score": "100~",
    "total_funding": "100000~"
}

"""     example
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


# get a list of companies from mattermark
# returns 50 companies each time it's called
def get_companies(payload):
    # mattermark call
    print("Getting companies, page 1")
    response = requests.get(companies_url, params=payload)
    response.raise_for_status()

    return response.json()


companies = get_companies(companies_payload)

print(companies)

# Write results
wfile = open("query_results.txt", "w")
wfile.write("Check these out\n")
for company in companies["companies"]:
    wfile.write("Company name: "+company["company_name"]+", domain: "+company["domain"]+"\n")
wfile.close()
