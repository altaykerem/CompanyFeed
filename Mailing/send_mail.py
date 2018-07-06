import os
import smtplib
from email.mime.text import MIMEText


def send_mail():
    # Send results saved in the file query_results
    recipients = [os.environ.get("a_mail"),
                  os.environ.get("c_mail"), os.environ.get("k_mail")]
    # ###Form html
    file_base = "/app"

    head_file = open(file_base + "/Mailing/mail_head.txt", "r")
    mail_head = head_file.read()
    head_file.close()

    body_file = open(file_base + "/query_results.txt", "r")
    mail_body = body_file.read()
    body_file.close()

    foot_file = open(file_base + "/Mailing/mail_foot.txt", "r")
    mail_foot = foot_file.read()
    foot_file.close()

    send_html = mail_head + mail_body + mail_foot
    # ###End of form html

    for mail in recipients:
        send_client(mail, send_html)


def send_client(to_mail, mail_content):
    # Access google account
    address = os.environ.get("mail_addr")
    password = os.environ.get("mail_pass")

    msg = MIMEText(mail_content, 'html')
    msg['Subject'] = "Daily mattermark"
    msg['To'] = to_mail
    msg['From'] = address

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(address, password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
