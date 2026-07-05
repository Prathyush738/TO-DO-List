# 📄 Project Documentation — To-Do List


## 1. Introduction

### 1.1 Purpose
The To-Do List application is a Python-based task management system that helps users organize, prioritize, and track their daily tasks efficiently with persistent JSON storage.

### 1.2 Project Scope
The scope of this project is to design and develop a To-Do List application using Python that enables users to add, edit, delete, and manage tasks with priority levels (High, Medium, Low), categories, and due dates, featuring persistent JSON file storage, a Tkinter desktop GUI, and a Flask web application deployed on Vercel.

### 1.3 Intended Audience
- Students managing assignments and deadlines
- Professionals managing work tasks
- Anyone who wants to stay organized


## 2. System Overview

The To-Do List application is built in three versions:

| Version | Technology | Platform |
|---|---|---|
| Desktop GUI | Python + Tkinter | Windows/Mac/Linux |
| Web App | Python + Flask | Browser (Vercel) |
| Standalone HTML | HTML + CSS + JS | Any Browser |


## 3. Features & Functionality

### 3.1 Task Management
- Add tasks with title, priority, category, due date, note
- Mark tasks as complete with checkbox
- Edit any task field
- Delete tasks with confirmation

### 3.2 Priority System
| Priority | Color | Meaning |
|---|---|---|
| 🔴 High | Red | Urgent — needs immediate attention |
| 🟡 Medium | Yellow | Important but not urgent |
| 🟢 Low | Green | Can be done when time permits |

### 3.3 Categories
```
Work | Personal | Shopping | Health | Study | Other
```

### 3.4 Due Date Tracking
- Set due dates for any task
- Overdue tasks highlighted in red automatically
- Overdue count shown in sidebar stats

### 3.5 Search & Filter
- Live search by title or note keyword
- Filter by Status (All/Pending/Done)
- Filter by Priority (All/High/Medium/Low)
- Filter by Category

### 3.6 Statistics (Sidebar)
- Total tasks count
- Pending tasks count
- Completed tasks count
- Overdue tasks count



## 4. Technical Design

### 4.1 Architecture
```
User Interface (Tkinter/Flask/HTML)
        ↓
Business Logic (Python Methods)
        ↓
Data Layer (JSON File)
```

### 4.2 Data Model
```json
[
  {
    "id": 1,
    "title": "Complete project report",
    "priority": "High",
    "category": "Work",
    "due": "2025-06-30",
    "note": "Submit before 5 PM",
    "done": false
  }
]
```

### 4.3 Key Functions/Methods

| Function | Description |
|---|---|
| `load_tasks()` | Reads tasks from JSON file |
| `save_tasks()` | Writes tasks to JSON file |
| `next_id()` | Generates unique task ID |
| `add_task()` | Adds new task |
| `edit_task()` | Updates existing task |
| `delete_task()` | Removes task by ID |
| `toggle_done()` | Marks task complete/incomplete |
| `render_tasks()` | Displays filtered task list |
| `update_stats()` | Updates sidebar statistics |
| `_filtered()` | Returns tasks matching filters |

### 4.4 Flask API Routes

| Route | Method | Description |
|---|---|---|
| `/todo` | GET | View all tasks |
| `/todo/add` | POST | Add new task |
| `/todo/toggle/<id>` | POST | Toggle task complete |
| `/todo/delete/<id>` | POST | Delete task |


## 5. Testing

| Test Case | Input | Expected Output | Result |
|---|---|---|---|
| Add task | Valid title | Task appears in list | ✅ Pass |
| Add task | Empty title | Warning shown | ✅ Pass |
| Mark complete | Checkbox click | Strikethrough applied | ✅ Pass |
| Delete task | Click delete | Task removed | ✅ Pass |
| Filter High | High priority | Only red tasks shown | ✅ Pass |
| Search keyword | Type "lunch" | Matching tasks shown | ✅ Pass |
| Overdue task | Past due date | Highlighted red | ✅ Pass |
| Data persistence | Relaunch app | Tasks still there | ✅ Pass |


## 6. Limitations

- No email/push notifications for due tasks
- No recurring tasks feature
- Single user only (no login)
- No calendar view
- Local JSON storage only


## 7. Future Enhancements

- 🔔 Email alerts for due tasks
- 📅 Calendar view for tasks
- 🔁 Recurring tasks support
- 👥 Multi-user with login
- ☁️ Cloud database storage
- 📱 Mobile app version
- 📊 Task completion analytics


## 8. Conclusion

The To-Do List application provides a complete task management solution with priority tracking, due dates, and persistent storage. It demonstrates Python OOP, Tkinter GUI, Flask web development, and JSON data handling skills gained during the CodeTech IT Solutions internship.

