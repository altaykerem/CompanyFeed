from apscheduler.schedulers.blocking import BlockingScheduler
from MatterMark import rising_query
from Mailing import send_mail as sender

sched = BlockingScheduler(timezone="UTC")


@sched.scheduled_job('cron', day_of_week='mon', hour=14, minute=30)
def scheduled_job():
    # #######Delete previous file content
    f = open("query_results.txt", "w")
    f.close()

    # #######Get mattermark digest;
    # write the result in the file query_results.txt
    rising_query.EmergingQuery().write_query()

    # #######Invoke send mail
    sender.send_mail()


sched.start()
