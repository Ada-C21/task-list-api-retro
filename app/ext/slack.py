import os
import requests

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

def notify_complete(task):
    if not SLACK_BOT_TOKEN:
        return
    
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }

    data = {
        "channel": "task-notifications-demo",
        "text": f'Task "{task.title}" has been marked complete',
    }

    requests.post(SLACK_API_URL, headers=headers, data=data)
