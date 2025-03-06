import click
import json
import os

TODO_FILE = "todo.json"

# Function to load tasks
def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r") as file:
            tasks = json.load(file)
            if not isinstance(tasks, list):
                return []
            return tasks
    except (json.JSONDecodeError, ValueError):
        return []

# Function to save tasks
def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@click.group()
def cli():
    """Simple To-Do List Manager"""
    pass

@click.command()
@click.argument("task", nargs=-1)  # Handle spaces in task names
def add(task):
    """Add a new task to the list"""
    task = " ".join(task)  # Convert tuple to string
    tasks = load_tasks()
    tasks.append({"task": task, "done": False})
    save_tasks(tasks)
    click.echo(f"Task added: {task}")

@click.command(name="list")
def list_tasks():  # Fixed function name
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found!")
        return
    for index, task in enumerate(tasks, 1):
        status = "✓" if task.get("done", False) else "✗"
        click.echo(f"{index}. {task['task']} [{status}]")

@click.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as completed!")
    else:
        click.echo("Invalid task number.")

@click.command()
@click.argument("task_number", type=int)
def remove(task_number):
    """Remove a task from the list"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Removed task: {removed_task['task']}")
    else:
        click.echo("Invalid task number.")

# Register commands
cli.add_command(add)
cli.add_command(list_tasks)  # Fixed function name
cli.add_command(complete)
cli.add_command(remove)

if __name__ == "__main__":
    cli()