from MatterMark import query


class EmergingQuery(query.Query):

    def __init__(self):
        # Get config
        super().__init__()
        print("uri: " + self.api_base + "\napi_key: " + self.api_key)

    def create_query(self):
        # GraphQL wrapper for MatterMark
        # For query schema please refer to -->
        #       https://docs.mattermark.com/graphql_api/schema/index.html
        # For msfl queries please refer to -->
        #   https://docs.mattermark.com/graphql_api/msfl/index.html
        msfl_dataset = """\\"dataset\\": \\"companies\\" """

        msfl_filter = """\\"filter\\":{\\"and\\": ["""
        # growth = """{\\"organizationMetrics.growthScore.current\\":{\\"gte\\":1000}}"""
        momentum = """{\\"organizationMetrics.weeklyMomentumScore.current\\":{\\"gte\\":1}}"""
        last_fund = """{\\"companyPersona.monthsSinceLastFunding\\":1}"""
        # msfl_filter = msfl_filter + growth + ","
        msfl_filter = msfl_filter + momentum + ","
        msfl_filter = msfl_filter + last_fund
        msfl_filter += "]}"

        msfl_sort = """\\"sort\\": [ { \\"organizationMetrics.growthScore.current\\": \\"desc\\" } ]"""

        msfl = "msfl:\"{"+msfl_dataset+","+msfl_filter+","+msfl_sort+"}\""

        search_query = """query {organizationSummaryQuery("""+msfl+""") {
            organizations(first: 50""" + self.page_map[self.currentPage] + """) {
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
        return search_query

    def page_info(self, data):
        self.totalResults = data['data']['organizationSummaryQuery']['organizations']['totalResults']
        # !!!!!! Uncomment for use page usage !!!!!!!!
        # page_info = data['data']['organizationSummaryQuery']['organizations']['pageInfo']
        # self.currentPage = data['data']['organizationSummaryQuery']['organizations']['currentPage']
        # self.hasNextPage = page_info['hasNextPage']

    def post_query(self):
        # Write results to the file query_results
        wfile = open("query_results.txt", "a")
        wfile.write("\nRecently funded and on the radar\n")
        wfile.write("NAME, STAGE, LAST FUNDING, LAST FUNDING DATE\n\n")
        while self.hasNextPage is True:
            q_data = self.query()
            print(q_data)
            self.hasNextPage = False
            self.page_info(q_data)
            data_organizations = q_data['data']['organizationSummaryQuery']['organizations']['edges']
            if q_data is not None:
                print("Data successfully retrieved...")
                for company in data_organizations:
                    print(company)
                    data_stem = company["node"]
                    wfile.write(data_stem["name"] + ", ")
                    wfile.write(data_stem["companyPersona"]["companyStage"] + ", ")
                    funding = data_stem["companyPersona"]["lastFundingAmount"]

                    if funding is not None:
                        wfile.write(str(data_stem["companyPersona"]["lastFundingAmount"]["value"]))
                        wfile.write(data_stem["companyPersona"]["lastFundingAmount"]["currency"] + ", ")
                    else:
                        wfile.write("None")

                    funding_date = data_stem["companyPersona"]["lastFundingDate"]
                    if funding_date is not None:
                        wfile.write(data_stem["companyPersona"]["lastFundingDate"])
                    else:
                        wfile.write("None")
                    wfile.write("\n")
            else:
                print("Returned data is null...")
                wfile.write("Data was not fetched")

        wfile.close()


score_query = EmergingQuery()
score_query.post_query()
