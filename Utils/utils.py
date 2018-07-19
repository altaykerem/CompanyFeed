import datetime


def number_formatter(n):
    abbreviations = ["", "K", "M", "B", "T", "quad"]
    n = "{:,}".format(int(n))
    coma_count = n.count(',')
    return "".join([n[:n.find(',')], abbreviations[coma_count]])


def log(text):
    now = datetime.datetime.now().time()
    wfile = open("log", "a")
    wfile.write("["+now+"]: "+text+"\n")
    wfile.close()


def clean_file(file):
    open(file, "w").close()


def decode_time(time):
    time = time.split(":")
    result = {
        "hour": int(time[0]),
        "minute": int(time[1])
    }
    return result
