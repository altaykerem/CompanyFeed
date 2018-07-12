from MatterMark import latest_query
from Utils import utils

# #######Delete previous file content
utils.clean_file("query_results.txt")

# #######Get mattermark digest;
# write the result in the file query_results.txt
success = latest_query.LatestQuery().write_query()
# try until no internal server errors
while not success:
    utils.clean_file("query_results.txt")
    success = latest_query.LatestQuery().write_query()
