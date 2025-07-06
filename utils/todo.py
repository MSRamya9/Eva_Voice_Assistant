# utils/todo.py
import json
import os
from datetime import datetime, timedelta

TASK_FILE = "todo_data.json"
tasks = []

# Load tasks from file
if os.path.exists(TASK_FILE):
    with open(TASK_FILE, "r") as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []

def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(task_text, priority="normal", due_date=None):
    task = {
        "text": task_text,
        "priority": priority.lower(),
        "due_date": due_date  # should be a string like "2025-07-10"
    }
    tasks.append(task)
    save_tasks()
    print(f"📝 Saving task: {task}")

    return f"Task '{task_text}' added with priority {priority}" + (f", due {due_date}" if due_date else "") + "."

def view_tasks(sort_by=None):
    if not tasks:
        return "Your to-do list is empty."

    # Sort tasks if requested
    if sort_by == "priority":
        priority_order = {"high": 1, "normal": 2, "low": 3}
        sorted_tasks = sorted(tasks, key=lambda t: priority_order.get(t.get("priority", "normal"), 2))
    elif sort_by == "due":
        def parse_date(task):
            try:
                return datetime.strptime(task.get("due_date", ""), "%Y-%m-%d")
            except:
                return datetime.max
        sorted_tasks = sorted(tasks, key=parse_date)
    else:
        sorted_tasks = tasks

    lines = []
    for i, task in enumerate(sorted_tasks):
        if isinstance(task, str):
            line = f"{i+1}. {task} (Priority: unknown)"
        else:
            line = f"{i+1}. {task['text']} (Priority: {task['priority']}"
            if task['due_date']:
                line += f", Due: {task['due_date']}"
            line += ")"
        lines.append(line)

    return "Here are your tasks:\n" + "\n".join(lines)




def remove_task(index):
    try:
        removed = tasks.pop(index - 1)
        save_tasks()
        return f"Removed task: {removed['text']}"
    except IndexError:
        return "Invalid task number."
    
def tasks_due_today():
    today = datetime.now().strftime("%Y-%m-%d")
    due_today = [t for t in tasks if isinstance(t, dict) and t.get("due_date") == today]

    if not due_today:
        return "You have no tasks due today."

    lines = [f"{i+1}. {t['text']} (Priority: {t['priority']})" for i, t in enumerate(due_today)]
    return "Tasks due today:\n" + "\n".join(lines)

def clear_tasks():
    tasks.clear()
    save_tasks()
    return "All tasks have been removed."


