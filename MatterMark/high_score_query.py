from MatterMark import query


class ScoreQuery(query.Query):

    def __init__(self):
        # Get config
        super().__init__()

    def create_query(self):
        # Targeted and sorted queries with MSFL
        # For msfl queries please refer to -->
        #   https://docs.mattermark.com/graphql_api/msfl/index.html
        msfl_dataset = """\\"dataset\\": \\"companies\\" """

        msfl_filter = """\\"filter\\":{\\"and\\": ["""
        growth = """{\\"organizationMetrics.growthScore.current\\":{\\"gte\\":1000}}"""
        momentum = """{\\"organizationMetrics.weeklyMomentumScore.current\\":{\\"gte\\":1000}}"""
        msfl_filter = msfl_filter + growth + ","
        msfl_filter = msfl_filter + momentum
        msfl_filter += "]}"

        msfl_sort = """\\"sort\\": [ { \\"organizationMetrics.growthScore.current\\": \\"desc\\" } ]"""

        msfl = "msfl:\"{" + msfl_dataset + "," + msfl_filter + "," + msfl_sort + "}\""

        search_query = self.base_query(msfl)
        return search_query

    def write_query(self):
        # Write results to the file query_results
        wfile = open("query_results.txt", "a")
        wfile.write("\nTop 5 Highest scorers\n")
        wfile.write("NAME, STAGE, LAST FUNDING, LAST FUNDING DATE\n\n")
        wfile.close()
        super().write_query()
