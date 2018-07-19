from apscheduler.schedulers.blocking import BlockingScheduler
from Database import firebase_db_conn as db_dictionary
from Mailing import send_mail as sender
from MatterMark import msfl_query
from Utils import utils

sched = BlockingScheduler(timezone="UTC")
date = db_dictionary.get_parameters()["day"]
hour = utils.decode_time(db_dictionary.get_parameters()["time"])["hour"]
minute = utils.decode_time(db_dictionary.get_parameters()["time"])["minute"]


def scheduled_job():
    # #######Delete previous file content
    utils.clean_file("query_results.txt")

    # #######Get mattermark digest;
    # write the result in the file query_results.txt
    success = msfl_query.LatestQuery().write_query()
    # try until no internal server errors
    while not success:
        utils.clean_file("query_results.txt")
        success = msfl_query.LatestQuery().write_query()

    # #######Invoke send mail
    sender.send_mail()


def check_job_date():
    # Check if the execution date is changed (checks once in every hour)
    db_date = db_dictionary.get_parameters()["day"]
    db_hour = utils.decode_time(db_dictionary.get_parameters()["time"])["hour"]
    db_minute = utils.decode_time(db_dictionary.get_parameters()["time"])["minute"]

    global date, hour, minute
    if date != db_date:
        date = db_date
        sched.remove_job('job')
        sched.add_job(scheduled_job, 'cron', day_of_week=date, hour=hour, minute=minute, id='job')
    if hour != db_hour:
        hour = db_hour
        minute = db_minute
        sched.remove_job('job')
        sched.add_job(scheduled_job, 'cron', day_of_week=date, hour=hour, minute=minute, id='job')


sched.add_job(scheduled_job, 'cron', day_of_week=date, hour=hour, minute=minute, id='job')
sched.add_job(check_job_date, 'interval', hours=1)
sched.start()
