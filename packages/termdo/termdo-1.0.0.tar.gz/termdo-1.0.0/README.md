# termdo

**termdo** is a lightweight, fast, terminal-based to-do manager with natural commands, subcommands, colored output, categories, and priorities.  
Designed for developers and power users who want a clean, intuitive workflow without leaving the terminal.

---

## 🚀 Features

### ✔ Simple Commands
```
termdo add "Buy groceries"
termdo done 2
termdo delete 3
termdo list
```

### ✔ Custom Syntax Support
```
1. Complete assignment
done task 1
```

### ✔ Categories & Priorities
```
termdo add "Finish report" --category work --priority high
termdo list --category work
```

### ✔ Colored Output (Rich)
- High priority → 🔴 Red  
- Medium → 🟡 Yellow  
- Low → 🟢 Green  
- Completed tasks → dim or green checkmark  

### ✔ Human-friendly storage
Uses JSON for easy portability.

---

## 📦 Installation

Once published to PyPI:

```
pip install termdo
```

Or install locally for development:

```
pip install .
```

---

## 📝 Usage

### Add a task
```
termdo add "Buy milk"
```

Add with category + priority:
```
termdo add "Finish project" --category work --priority high
```

### List tasks
```
termdo list
```

Filter:
```
termdo list --category personal
termdo list --priority high
```

### Mark task as done
```
termdo done 3
```

### Delete a task
```
termdo delete 2
```

---

## 📁 Storage Format

`~/.termdo/tasks.json` contains:

```json
{
  "text": "Buy milk",
  "done": false,
  "category": "personal",
  "priority": "medium"
}
```

---

## 🛠 Developer Notes

### Install in editable mode
```
pip install -e .
```

### Project Structure
```
termdo/
│
├── termdo/
│   ├── __init__.py
│   ├── cli.py
│
├── README.md
├── pyproject.toml
```

---

## 📜 License

MIT License © 2025 Akash Nandy
