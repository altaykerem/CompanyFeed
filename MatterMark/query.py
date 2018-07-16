import os
import requests
import json
from Trello import assign
from Utils import meta_extractor
from Utils import utils
from Mailing import mail_form_adapter as mailing


# This class is the parent class of organization queries
class Query:
    currentPage = 0
    hasNextPage = True
    totalResults = None
    pageSize = 10

    api_base = ""
    api_key = ""

    # Queries return information grouped in pages
    page_map = [', after: "0|50"', ', after: "1|50"', ', after: "2|50"', ', after: "3|50"', ', after: "4|50"',
                ', after: "5|50"', ', after: "6|50"', ', after: "7|50"', ', after: "8|50"', ', after: "9|50"',
                ', after: "10|50"']

    def __init__(self):
        # Get config
        self.api_base = os.environ.get("mm_graphql_api")
        self.api_key = os.environ.get("mm_api_key")

    def base_query(self, msfl):
        # GraphQL wrapper for MatterMark
        # For query schema please refer to -->
        #       https://docs.mattermark.com/graphql_api/schema/index.html
        # Returns a list of organizations with fields specified as below that satisfies conditions in child classes
        query = """query {organizationSummaryQuery("""+msfl+""") {
            organizations(first:""" + str(self.pageSize) + self.page_map[self.currentPage] + """) {
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
                print("Request is successful with code {} ...".format(response.status_code))
                return json.loads(response.content)
            else:
                utils.log("Error in response: {}".format(response.raise_for_status()))
        except Exception as e:
            utils.log("Problem while sending request: {}".format(e))
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
        mail_adaptor = mailing.MailAdapter()
        mail_adaptor.open_file("query_results.txt")

        while self.hasNextPage is True:
            q_data = self.query(self.create_query())
            self.hasNextPage = False
            if q_data is not None:
                self.page_info(q_data)
                data_organizations = q_data['data']['organizationSummaryQuery']['organizations']['edges']
                print("Data successfully retrieved...")
                for company in data_organizations:
                    # Access company data
                    data_stem = company["node"]
                    org_id = data_stem["id"]
                    org_data = self.query(self.org_info_query(org_id))['data']['organization']
                    domain = org_data['domains'][0]['domain']
                    funding = data_stem["companyPersona"]["lastFundingAmount"]
                    funding_amount = "Undisclosed"
                    currency = ""
                    funding_date_info = data_stem["companyPersona"]["lastFundingDate"]
                    funding_date = "Undisclosed"

                    if org_data['offices']:
                        location = org_data['offices'][0]['location']['region']['name']
                    else:
                        location = "-"

                    if funding is not None:
                        funding_amount = str(data_stem["companyPersona"]["lastFundingAmount"]["value"])
                        currency = data_stem["companyPersona"]["lastFundingAmount"]["currency"]
                        funding_amount = utils.number_formatter(funding_amount)

                    if funding_date_info is not None:
                        funding_date = data_stem["companyPersona"]["lastFundingDate"]

                    # Assign company
                    assign.add_assignment(domain)

                    # Write company data in html table format
                    mail_adaptor.open_row()

                    # image, name, description
                    company_image = mail_adaptor.adapt_image(meta_extractor.get_image(domain))
                    mail_adaptor.add_header_data(company_image, 5)
                    mail_adaptor.add_header_data(mail_adaptor.make_bold(data_stem["name"]), 5)
                    mail_adaptor.add_header_data(meta_extractor.get_description(domain), 5)

                    columns = ["Stage", "Last Funding", "Last Funding Date", "Domain", "Region"]
                    mail_adaptor.add_row_data(columns)

                    values = [data_stem["companyPersona"]["companyStage"],
                              funding_amount+" "+currency,
                              funding_date, domain, location]
                    mail_adaptor.add_row_data(values)

                    mail_adaptor.close_row()
            else:
                utils.log("Returned data is null...")
                return False
        mail_adaptor.close_file()
        return True
