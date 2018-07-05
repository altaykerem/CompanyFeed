def number_formatter(n):
    abbreviations = ["", "K", "M", "B", "T", "quad"]
    n = "{:,}".format(int(n))
    coma_count = n.count(',')
    return "".join([n[:n.find(',')], abbreviations[coma_count]])


def log(text):
    wfile = open("log", "a")
    wfile.write(text)
    wfile.close()
