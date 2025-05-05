
import streamlit as st
import pandas as pd

# Initialize task data
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Task", "Category", "Due Date", "Status"])

# Load existing data or initialize
if "task_data" not in st.session_state:
    st.session_state.task_data = load_data()

# Application title
st.title("🎯 Simple Task Manager App")

# Navigation menu
menu = st.sidebar.radio("Menu", ["Add Task", "View Tasks", "Search Tasks", "Update Task Status"])

# Add a new task
if menu == "Add Task":
    st.header("Add a New Task")
    with st.form("add_task_form"):
        task = st.text_input("Task Description")
        category = st.selectbox("Category", ["Work", "Personal", "Study", "Others"])
        due_date = st.date_input("Due Date")
        submit = st.form_submit_button("Add Task")

        if submit:
            if task:
                new_task = {"Task": task, "Category": category, "Due Date": due_date, "Status": "Pending"}
                st.session_state.task_data = pd.concat(
                    [st.session_state.task_data, pd.DataFrame([new_task])], ignore_index=True
                )
                st.success("Task added successfully!")
            else:
                st.error("Please enter the task description.")

# View all tasks
elif menu == "View Tasks":
    st.header("All Tasks")
    st.dataframe(st.session_state.task_data)

# Search for a task
elif menu == "Search Tasks":
    st.header("Search Tasks")
    search_option = st.radio("Search by", ["Task", "Category"])
    query = st.text_input(f"Enter {search_option}:")

    if query:
        filtered_data = st.session_state.task_data[
            st.session_state.task_data[search_option].str.contains(query, case=False, na=False)
        ]
        if not filtered_data.empty:
            st.dataframe(filtered_data)
        else:
            st.warning(f"No tasks found matching {search_option}: {query}")

# Update task status
elif menu == "Update Task Status":
    st.header("Update Task Status")
    with st.form("update_task_form"):
        task_name = st.text_input("Enter Task Description")
        action = st.selectbox("Mark as", {"Pending", "Done"})
        submit = st.form_submit_button("Update Status")

    if submit:
        if task_name:
            task_index = st.session_state.task_data[
                st.session_state.task_data["Task"].str.contains(task_name, case=False, na=False)
            ].index
            if not task_index.empty:
                st.session_state.task_data.at[task_index[0], "Status"] = action
                st.success(f"Task marked as {action}!")
            else:
                st.error("Task not found. Please check the description.")
        else:
            st.error("Please enter a task description.")
