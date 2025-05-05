%%writefile app.py
import streamlit as st
import pandas as pd
from datetime import date

# -------------------------
# Initialize session state
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}  # default user
if "task_data" not in st.session_state:
    st.session_state.task_data = pd.DataFrame(columns=["Task", "Category", "Due Date", "Status"])

# -------------------------
# Page Navigation Function
# -------------------------
def switch_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Login"

# -------------------------
# Page 1: Login
# -------------------------
def login_page():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            switch_page("Dashboard")
        else:
            st.error("Invalid credentials")

    st.info("Don't have an account?")
    if st.button("Register"):
        switch_page("Register")

# -------------------------
# Page 2: Register
# -------------------------
def register_page():
    st.title("📝 Register")
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    if st.button("Register"):
        if username in st.session_state.users:
            st.error("Username already exists!")
        else:
            st.session_state.users[username] = password
            st.success("Registered successfully!")
            switch_page("Login")

    if st.button("Back to Login"):
        switch_page("Login")

# -------------------------
# Page 3: Dashboard
# -------------------------
def dashboard():
    st.title("📊 Dashboard")
    total_tasks = len(st.session_state.task_data)
    completed = len(st.session_state.task_data[st.session_state.task_data["Status"] == "Done"])
    pending = total_tasks - completed

    st.metric("Total Tasks", total_tasks)
    st.metric("Completed", completed)
    st.metric("Pending", pending)

    st.write("---")
    if st.button("Go to Task Manager"):
        switch_page("Task Manager")
    if st.button("Logout"):
        st.session_state.logged_in = False
        switch_page("Login")

# -------------------------
# Page 4: Task Manager
# -------------------------
def task_manager():
    st.title("📒 Task Manager")

    # Reminder for tasks due today
    today = pd.to_datetime(date.today())
    due_today = st.session_state.task_data[
        pd.to_datetime(st.session_state.task_data["Due Date"]) == today
    ]
    if not due_today.empty:
        st.warning("📌 You have tasks due today!")
        st.dataframe(due_today)

    menu = st.sidebar.radio("Select", ["Add Task", "View Tasks", "Search Tasks", "Update Status", "Back to Dashboard"])

    if menu == "Add Task":
        st.subheader("Add New Task")
        with st.form("add_task"):
            task = st.text_input("Task Description")
            category = st.selectbox("Category", ["Work", "Personal", "Study", "Others"])
            due_date = st.date_input("Due Date", min_value=date.today())
            submit = st.form_submit_button("Add Task")
            if submit and task:
                new = {"Task": task, "Category": category, "Due Date": due_date, "Status": "Pending"}
                st.session_state.task_data = pd.concat([st.session_state.task_data, pd.DataFrame([new])], ignore_index=True)
                st.success("Task added!")

    elif menu == "View Tasks":
        st.subheader("All Tasks")
        filter_category = st.selectbox("Filter by Category", ["All"] + st.session_state.task_data["Category"].unique().tolist())
        if filter_category == "All":
            st.dataframe(st.session_state.task_data)
        else:
            filtered = st.session_state.task_data[st.session_state.task_data["Category"] == filter_category]
            st.dataframe(filtered)

    elif menu == "Search Tasks":
        st.subheader("Search Tasks")
        option = st.radio("Search by", ["Task", "Category"])
        query = st.text_input("Enter search term:")
        if query:
            df = st.session_state.task_data
            result = df[df[option].str.contains(query, case=False, na=False)]
            st.dataframe(result)

    elif menu == "Update Status":
        st.subheader("Update Task Status")
        task_name = st.text_input("Task to update")
        status = st.selectbox("Mark as", ["Pending", "Done"])
        if st.button("Update"):
            index = st.session_state.task_data[
                st.session_state.task_data["Task"].str.contains(task_name, case=False, na=False)
            ].index
            if not index.empty:
                st.session_state.task_data.at[index[0], "Status"] = status
                st.success("Status updated!")
            else:
                st.error("Task not found.")

    elif menu == "Back to Dashboard":
        switch_page("Dashboard")


# -------------------------
# Routing Logic
# -------------------------
if st.session_state.current_page == "Login":
    login_page()
elif st.session_state.current_page == "Register":
    register_page()
elif st.session_state.logged_in:
    if st.session_state.current_page == "Dashboard":
        dashboard()
    elif st.session_state.current_page == "Task Manager":
        task_manager()
else:
    switch_page("Login")
