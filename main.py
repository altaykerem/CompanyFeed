from apscheduler.schedulers.blocking import BlockingScheduler
from MatterMark import latest_query
from Mailing import send_mail as sender

sched = BlockingScheduler(timezone="UTC")


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=14, minute=30)
def scheduled_job():
    # #######Delete previous file content
    open("query_results.txt", "w").close()

    # #######Get mattermark digest;
    # write the result in the file query_results.txt
    latest_query.LatestQuery().write_query()

    # #######Invoke send mail
    sender.send_mail()


sched.start()
