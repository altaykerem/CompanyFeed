import os
import requests
import json
from Trello import assign
from Utils import meta_extractor
from Utils import utils
from Mailing import mail_form_adapter as mailing
from Database import firebase_db_conn as db_dictionary


# This class is the parent class of organization queries
class Query:
    page_size = 10

    api_base = ""
    api_key = ""

    def __init__(self):
        # Get config
        self.api_base = os.environ.get("mm_graphql_api")
        self.api_key = os.environ.get("mm_api_key")

    def base_query(self, msfl):
        params = db_dictionary.get_parameters()
        self.page_size = params['pageSize']

        # GraphQL wrapper for MatterMark
        # For query schema please refer to -->
        #       https://docs.mattermark.com/graphql_api/schema/index.html
        # Returns a list of organizations with fields specified as below that satisfies conditions in child classes
        query = """query {organizationSummaryQuery(""" + msfl + """) {
            organizations(first: """ + self.page_size + """, after: "0|50") {
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
        print(query)
        # GraphQL structure is pretty similar to json
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
                organization(id: \"""" + org_id + """") {
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

    def create_query(self):
        # Override in child
        return ""

    def write_query(self):
        # Write results to the file query_results
        mail_adaptor = mailing.MailAdapter()
        mail_adaptor.open_file("query_results.txt")

        q_data = self.query(self.create_query())
        if q_data is not None:
            print(q_data)
            data_organizations = q_data['data']['organizationSummaryQuery']['organizations']['edges']
            print("Data successfully retrieved...")
            for company in data_organizations:
                # Access company data
                data_stem = company["node"]
                org_id = data_stem["id"]
                org_data = self.query(self.org_info_query(org_id))['data']['organization']
                funding = data_stem["companyPersona"]["lastFundingAmount"]
                funding_amount = "Undisclosed"
                currency = ""
                funding_date_info = data_stem["companyPersona"]["lastFundingDate"]
                funding_date = "Undisclosed"

                if org_data['domains']:
                    domain = org_data['domains'][0]['domain']
                else:
                    domain = "-"

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
                trello = db_dictionary.get_functions()['trello']
                if trello:
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
                          funding_amount + " " + currency,
                          funding_date, domain, location]
                mail_adaptor.add_row_data(values)

                mail_adaptor.close_row()
        else:
            utils.log("Returned data is null...")
            return False
        mail_adaptor.close_file()
        return True

    @staticmethod
    def map_sort_criteria(st):
        # adapt sorting criteria with mattermark, funding date as default
        cmap = {"funding-date": "companyPersona.lastFundingDate",
                "score": "organizationMetrics.growthScore.current",
                "funding-amount": "companyPersona.lastFundingAmount.value"}
        return cmap.get(st, "companyPersona.lastFundingDate")
