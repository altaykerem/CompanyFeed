from MatterMark import high_score_query, angel_query, rising_query
from MatterMark import send_mail as sender

# #######Delete file content
f = open("query_results.txt", "w")
f.close()

# #######Get mattermark digest
# writes the result in a file query_results.txt
rising_query.EmergingQuery().post_query()
angel_query.AssistanceQuery().post_query()
high_score_query.ScoreQuery().post_query()

# #######Invoke send mail
sender.send_mail()

''' Rest Api Call from MatterMark import mm_digest
mm_digest.write_mm_result()
'''