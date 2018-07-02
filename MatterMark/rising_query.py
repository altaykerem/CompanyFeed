from MatterMark import query


class EmergingQuery(query.Query):

    def __init__(self):
        # Get config
        super().__init__()

    def create_query(self):
        # Targeted and sorted queries with MSFL
        # For msfl queries please refer to -->
        #   https://docs.mattermark.com/graphql_api/msfl/index.html
        msfl = """msfl:\"{\
        \\"dataset\\": \\"companies\\",\
        \\"filter\\":{\\"and\\": [\
            {\\"organizationMetrics.weeklyMomentumScore.current\\":{\\"gte\\":500}},\
            {\\"organizationMetrics.growthScore.current\\":{\\"lte\\":1500}},\
            {\\"businessModels.name\\": \\"B2B\\" },\
            {\\"industries.name\\": {\\"in\\":\
                [ \\"banking\\",\\"cloud\\", \\"enterprise software\\", \\"finance\\", \\"hardware\\",\
                \\"human resources\\", \\"internet of things\\", \\"insurance\\", \\"lending\\", \\"mobile\\",\
                \\"payments\\", \\"robotics\\", \\"security\\", \\"software development\\",\
                \\"technical support\\"] } },\
            {\\"or\\" : [\
                {\\"companyPersona.stage\\": \\"pre series a\\"},\
                {\\"companyPersona.stage\\": \\"a\\"},\
                {\\"companyPersona.stage\\": \\"b\\"},\
                {\\"companyPersona.stage\\": \\"c\\"},\
                {\\"companyPersona.stage\\": \\"exited(acquired)\\"},\
                {\\"companyPersona.stage\\": \\"late\\"}]},\
            { \\"offices.location.country.iso3\\": \\"USA\\" }\
        ]},\
        \\"sort\\": [ { \\"organizationMetrics.growthScore.current\\": \\"desc\\" } ]\
        }\" """

        search_query = self.base_query(msfl)
        return search_query

    def write_query(self):
        wfile = open("query_results.txt", "a")

        open_table = """
        <tr>
            <td bgcolor="#ffffff">
                <table border="1" cellpadding="0" cellspacing="0" width="100%%">
                    <tr>
                        <td colspan="6"><h3 align="center">"""
        wfile.write(open_table)
        wfile.write("Growing this week")
        wfile.write(" </h3></td></tr>")
        wfile.close()

        super().write_query()

        wfile = open("query_results.txt", "a")
        wfile.write("</table></td></tr>")
        wfile.close()
