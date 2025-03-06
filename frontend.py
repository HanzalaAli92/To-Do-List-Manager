import streamlit as st
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

# Custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Streamlit UI
st.title("📝 To-Do List Manager")

# Add Task
task_input = st.text_input("Add a new task:")
if st.button("➕ Add Task"):
    if task_input:
        tasks = load_tasks()
        tasks.append({"task": task_input, "done": False})
        save_tasks(tasks)
        st.success(f"Task added: {task_input}")
        st.rerun()  

# Show Tasks
tasks = load_tasks()
if tasks:
    st.subheader("📋 Your Tasks")
    for index, task in enumerate(tasks, 1):
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])  # Extra column for Edit button
        col1.write(f"{index}. {task['task']}")
        
        if col2.button("✔", key=f"complete_{index}"):
            tasks[index - 1]["done"] = True
            save_tasks(tasks)
            st.rerun()

        if col3.button("❌", key=f"remove_{index}"):
            tasks.pop(index - 1)
            save_tasks(tasks)
            st.rerun()

        # Edit Option
        if col4.button("✏", key=f"edit_{index}"):
            st.session_state["edit_index"] = index - 1  # Save index in session state

    # Show input field if edit button is clicked
    if "edit_index" in st.session_state:
        edit_index = st.session_state["edit_index"]
        st.subheader("✏ Edit Task")
        new_task_text = st.text_input("Update Task:", tasks[edit_index]["task"])

        if st.button("✅ Save Changes"):
            tasks[edit_index]["task"] = new_task_text
            save_tasks(tasks)
            del st.session_state["edit_index"]  # Clear edit state
            st.rerun()

else:
    st.info("No tasks found!")

st.markdown("---")
st.caption("🚀 Built with Streamlit | By Hanzala")