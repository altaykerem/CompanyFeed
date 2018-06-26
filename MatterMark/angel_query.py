from MatterMark import query


class AssistanceQuery(query.Query):

    def __init__(self):
        # Get config
        super().__init__()

    def create_query(self):
        # Targeted and sorted queries with MSFL
        # For msfl queries please refer to -->
        #   https://docs.mattermark.com/graphql_api/msfl/index.html
        msfl_dataset = """\\"dataset\\": \\"companies\\" """

        msfl_filter = """\\"filter\\":{\\"and\\": ["""
        momentum = """{\\"organizationMetrics.weeklyMomentumScore.current\\":{\\"lte\\":1}}"""
        last_fund = """{\\"companyPersona.monthsSinceLastFunding\\":2}"""
        msfl_filter = msfl_filter + momentum + ","
        msfl_filter = msfl_filter + last_fund
        msfl_filter += "]}"

        msfl_sort = """\\"sort\\": [ { \\"organizationMetrics.growthScore.current\\": \\"desc\\" } ]"""

        msfl = "msfl:\"{"+msfl_dataset+","+msfl_filter+","+msfl_sort+"}\""

        search_query = self.base_query(msfl)
        return search_query

    def write_query(self):
        # Write results to the file query_results
        wfile = open("query_results.txt", "a")
        wfile.write("\nRecently funded but not yet progressed\n")
        wfile.write("NAME, STAGE, LAST FUNDING, LAST FUNDING DATE\n\n")
        wfile.close()
        super().write_query()
