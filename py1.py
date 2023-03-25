import sqlite3
import os
import datetime

# Get the path to the user's Chrome history database
data_path = os.path.expanduser('~') + "/Library/Application Support/Google/Chrome/Default"
files = os.listdir(data_path)
history_db = os.path.join(data_path, 'History')

# Establish a connection to the Chrome history database
connection = sqlite3.connect(history_db)
cursor = connection.cursor()

# Retrieve the URL, title, and visit time for each history item
select_statement = "SELECT urls.url, urls.title, visits.visit_time FROM urls, visits WHERE urls.id = visits.url;"
cursor.execute(select_statement)
results = cursor.fetchall()

# Print out the results
print("Chrome History:\n")
for row in results:
    url = row[0]
    title = row[1]
    timestamp = row[2] / 1000000
    visit_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{visit_time}: {title} ({url})")

# Close the database connection
connection.close()
