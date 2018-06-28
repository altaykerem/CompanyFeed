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

        open_table = """
        <tr>
            <td bgcolor="#ffffff">
                <table border="1" cellpadding="0" cellspacing="0" width="100%%">
                    <tr>
                        <td colspan="4"><h3 align="center">
        """
        wfile.write(open_table)
        wfile.write("Recently funded but not yet progressed")
        wfile.write(" </h3></td></tr>")

        table_columns = """
        <tr>
            <td colspan="1" align="center">Name</td>
            <td colspan="1" align="center">Stage</td>
            <td colspan="1" align="center">Last Funding</td>
            <td colspan="1" align="center">Last Funding Date</td>
        </tr>
        """
        wfile.write(table_columns)
        wfile.close()

        super().write_query()

        wfile = open("query_results.txt", "a")
        wfile.write("</table></td></tr>")
        wfile.close()
