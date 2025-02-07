import requests
from datetime import datetime, timedelta
from win10toast import ToastNotifier

def check_tasks_and_notify():
    # 1. Get tasks from your Django API (assuming tasks API returns JSON)
    response = requests.get("http://127.0.0.1:8000/api/tasks/")
    tasks = response.json()
    
    # 2. Figure out which tasks are due soon
    upcoming_tasks = []
    now = datetime.now()
    
    for task in tasks:
        # Ensure task has date/time
        if task['start_date'] and task['start_time']:
            # Combine strings, e.g. "2025-02-07 09:58"
            start_str = f"{task['start_date']} {task['start_time']}"
            
            try:
                # Adjust the format depending on how start_time is formatted
                task_datetime = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            except ValueError:
                # If the format doesn’t match, skip this task
                continue

            # Check if the task time is within the next 15 minutes
            if now <= task_datetime <= (now + timedelta(minutes=15)):
                upcoming_tasks.append(task)

    if upcoming_tasks:
        toaster = ToastNotifier()
        toaster.show_toast(
            "Task Reminder",
            f"You have {len(upcoming_tasks)} upcoming tasks!",
            duration=10,  # seconds
            threaded=True
        )
if __name__ == "__main__":
    check_tasks_and_notify()
