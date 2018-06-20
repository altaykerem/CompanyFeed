import os
import smtplib
from email.mime.text import MIMEText
# from MatterMark import dd_utils

# Access google account
address = os.environ.get("mail_addr")
password = os.environ.get("mail_pass")
"""
account = dd_utils.get_mail_credentials()
address = dd_utils.get_mail_address(account)
password = dd_utils.get_mail_pass(account)
"""

send_file = open("query_results.txt", "r")
msg = MIMEText(send_file.read())
send_file.close()

msg['Subject'] = "Daily mattermark"
msg['To'] = "kerem.alty@gmail.com"
msg['From'] = address

print(msg)
s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
s.login(address, password)
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()
