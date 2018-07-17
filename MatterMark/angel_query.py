from MatterMark import query
from Mailing import mail_form_adapter as mailing


class AssistanceQuery(query.Query):

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
            {\\"organizationMetrics.weeklyMomentumScore.current\\":{\\"lte\\":0}},\
            {\\"companyPersona.monthsSinceLastFunding\\":3},\
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
        # Write results to the file query_results
        mail_adaptor = mailing.MailAdapter()
        mail_adaptor.open_file("query_results.txt")
        mail_adaptor.open_table("Recently funded but not progressed this week", 5)
        mail_adaptor.close_file()

        success = super().write_query()

        mail_adaptor.open_file("query_results.txt")
        mail_adaptor.close_table()
        mail_adaptor.close_file()

        return success
