#!/usr/bin/env python3

import json
import os
import argparse
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

TASK_FILE = os.path.expanduser("~/.termdo/tasks.json")

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    os.makedirs(os.path.dirname(TASK_FILE), exist_ok=True)
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(text, category, priority):
    tasks = load_tasks()
    tasks.append({
        "text": text,
        "done": False,
        "category": category or "general",
        "priority": priority or "medium"
    })
    save_tasks(tasks)
    console.print(f"[green]Added:[/green] {text}")

def list_tasks(category=None, priority=None):
    tasks = load_tasks()

    table = Table(title="Termdo Tasks", box=box.ROUNDED, show_lines=True)
    table.add_column("#", style="bold cyan")
    table.add_column("Task")
    table.add_column("Category")
    table.add_column("Priority")
    table.add_column("Status")

    for i, task in enumerate(tasks, 1):
        if category and task["category"] != category:
            continue
        if priority and task["priority"] != priority:
            continue

        pr_color = {
            "high": "red",
            "medium": "yellow",
            "low": "green"
        }.get(task["priority"], "white")

        status = "[green]✓[/green]" if task["done"] else "[red]✗[/red]"

        table.add_row(
            str(i),
            task["text"],
            task["category"],
            f"[{pr_color}]{task['priority']}[/{pr_color}]",
            status
        )

    console.print(table)

def mark_done(index):
    tasks = load_tasks()
    try:
        tasks[index - 1]["done"] = True
        save_tasks(tasks)
        console.print(f"[green]Marked task {index} as done[/green]")
    except:
        console.print("[red]Invalid task number[/red]")

def delete_task(index):
    tasks = load_tasks()
    try:
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        console.print(f"[yellow]Deleted:[/yellow] {removed['text']}")
    except:
        console.print("[red]Invalid task number[/red]")

def main():
    parser = argparse.ArgumentParser(prog="termdo", description="Terminal To-Do Manager")
    sub = parser.add_subparsers(dest="command")

    # ADD
    add = sub.add_parser("add", help="Add a new task")
    add.add_argument("text", type=str)
    add.add_argument("--category", type=str)
    add.add_argument("--priority", type=str, choices=["high", "medium", "low"])

    # LIST
    ls = sub.add_parser("list", help="List all tasks")
    ls.add_argument("--category", type=str)
    ls.add_argument("--priority", type=str)

    # DONE
    done = sub.add_parser("done", help="Mark a task as done")
    done.add_argument("task_number", type=int)

    # DELETE
    delete = sub.add_parser("delete", help="Delete a task")
    delete.add_argument("task_number", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.text, args.category, args.priority)

    elif args.command == "list":
        list_tasks(args.category, args.priority)

    elif args.command == "done":
        mark_done(args.task_number)

    elif args.command == "delete":
        delete_task(args.task_number)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
