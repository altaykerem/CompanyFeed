from MatterMark import high_score_query, angel_query, rising_query
from Mailing import send_mail as sender

# #######Delete previous file content
f = open("query_results.txt", "w")
f.close()

# #######Get mattermark digest;
# write the result in the file query_results.txt
rising_query.EmergingQuery().write_query()
angel_query.AssistanceQuery().write_query()
high_score_query.ScoreQuery().write_query()

# #######Invoke send mail
sender.send_mail()
