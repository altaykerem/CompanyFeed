from MatterMark import mm_digest
from MatterMark import send_mail as sender

# #######Get mattermark digest
# writes the result in a file query_results.txt
mm_digest.write_mm_result()

# #######Invoke send mail
sender.send_mail()
