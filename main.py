from apscheduler.schedulers.blocking import BlockingScheduler
from MatterMark import latest_query
from Mailing import send_mail as sender
from Utils import utils

sched = BlockingScheduler(timezone="UTC")


@sched.scheduled_job('cron', day_of_week='fri', hour=14, minute=30)
def scheduled_job():
    # #######Delete previous file content
    utils.clean_file("query_results.txt")

    # #######Get mattermark digest;
    # write the result in the file query_results.txt
    latest_query.LatestQuery().write_query()

    # #######Invoke send mail
    sender.send_mail()


sched.start()
