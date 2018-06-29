import os
import requests
import json


# This class is the parent class of organization queries
class Query:
    currentPage = 0
    hasNextPage = True
    totalResults = None

    api_base = ""
    api_key = ""

    # Queries return information grouped in pages
    page_map = [', after: "0|50"', ', after: "1|50"', ', after: "2|50"', ', after: "3|50"', ', after: "4|50"',
                ', after: "5|50"', ', after: "6|50"', ', after: "7|50"', ', after: "8|50"', ', after: "9|50"',
                ', after: "10|50"']

    def __init__(self):
        # Get config
        self.api_base = os.environ.get("mm_graphql_api")
        self.api_key = os.environ.get("api_key")

    def base_query(self, msfl):
        # GraphQL wrapper for MatterMark
        # For query schema please refer to -->
        #       https://docs.mattermark.com/graphql_api/schema/index.html
        # Returns a list of organizations with fields specified as below that satisfies conditions in child classes
        query = """query {organizationSummaryQuery("""+msfl+""") {
            organizations(first: 10""" + self.page_map[self.currentPage] + """) {
                edges {
                    cursor
                    node {
                        id
                        name
                        companyPersona {
                            companyStage
                            lastFundingAmount {
                                value
                                currency
                            }
                            lastFundingDate
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    startCursor
                    hasPreviousPage
                }
                currentPage
                totalResults
            }}
        }"""

        # GraphQL structure is pretty similar to json, yet it's not meant to store data but to get related fields
        # in JSON format.
        # So the query defines what to retrieve from the database in the request. Format isn't KEY:VALUE,
        # yet it's just the KEY.  Simply, you post the KEY and it returns the KEY:VALUE pairs.
        return query

    def query(self, query):
        # Create Header
        auth = 'Bearer ' + self.api_key
        header = {'Content-Type': 'application/graphql', 'Authorization': auth, 'Accept': 'application/json'}

        # Create Query String
        query_str = query

        # Send Request
        try:
            response = requests.post(url=self.api_base, headers=header, data=query_str)
            if response.status_code == requests.codes.ok:
                self.log("Request is successful with code {} ...".format(response.status_code))
                return json.loads(response.content)
            else:
                self.log("Error in response: {}".format(response.raise_for_status()))
        except Exception as e:
            self.log("Problem while sending request: {}".format(e))
            return

    @staticmethod
    def org_info_query(org_id):
        # Returns information related to the company given its id
        org_query = """query {
                organization(id: \""""+org_id+"""") {
                    estFounded
                    domains {
                        domain
                    }
                    businessModels {
                        name
                    }
                    industries {
                        name
                    }
                    offices {
                        location {
                            city { name }
                            country { iso3 }
                            region { name }
                        }
                    }

                }
            }
        """
        return org_query

    def page_info(self, data):
        # Updates pages
        self.totalResults = data['data']['organizationSummaryQuery']['organizations']['totalResults']
        # !!!!!! Uncomment for use page usage (that is +50 companies returned)!!!!!!!!
        # page_info = data['data']['organizationSummaryQuery']['organizations']['pageInfo']
        # self.currentPage = data['data']['organizationSummaryQuery']['organizations']['currentPage']
        # self.hasNextPage = page_info['hasNextPage']

    def create_query(self):
        # Override in child
        return ""

    def write_query(self):
        # Write results to the file query_results
        wfile = open("query_results.txt", "a")
        while self.hasNextPage is True:
            q_data = self.query(self.create_query())
            self.hasNextPage = False
            self.page_info(q_data)
            data_organizations = q_data['data']['organizationSummaryQuery']['organizations']['edges']
            if q_data is not None:
                print("Data successfully retrieved...")
                for company in data_organizations:
                    wfile.write("<tr>\n")

                    data_stem = company["node"]
                    wfile.write("<td>"+data_stem["name"]+"</td>\n")
                    wfile.write("<td>"+data_stem["companyPersona"]["companyStage"]+"</td>\n")

                    funding = data_stem["companyPersona"]["lastFundingAmount"]
                    if funding is not None:
                        wfile.write("<td>"+str(data_stem["companyPersona"]["lastFundingAmount"]["value"]))
                        wfile.write(data_stem["companyPersona"]["lastFundingAmount"]["currency"]+"</td>\n")
                    else:
                        wfile.write("<td>No data</td>\n")
                    funding_date = data_stem["companyPersona"]["lastFundingDate"]
                    if funding_date is not None:
                        wfile.write("<td>"+data_stem["companyPersona"]["lastFundingDate"]+"</td>\n")
                    else:
                        wfile.write("<td>No data</td>\n")

                    org_id = data_stem["id"]
                    org_data = self.query(self.org_info_query(org_id))['data']['organization']
                    wfile.write("<td>" + org_data['domains'][0]['domain'] + "</td>\n")
                    wfile.write("<td>" + org_data['offices'][0]['location']['region']['name'] + "</td>\n")

                    wfile.write("</tr>\n")
            else:
                self.log("Returned data is null...")

        wfile.close()

    def log(self, text):
        wfile = open("log", "a")
        wfile.write(text)
        wfile.close()
