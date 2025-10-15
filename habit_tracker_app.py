import csv
from datetime import datetime
import streamlit as st
from plyer import notification
import os

FILENAME = "habits.csv"

# --------------------------
# Helper functions
# --------------------------

def load_habits():
    habits = []
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Ensure each row has 4 columns (name, frequency, status, last_done)
                while len(row) < 4:
                    row.append("")
                habits.append(row)
    return habits

def save_habits(habits):
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(habits)

def add_habit(name, frequency):
    habits = load_habits()
    habits.append([name, frequency, "Not Done", ""])
    save_habits(habits)

def mark_done(name):
    habits = load_habits()
    for habit in habits:
        if habit[0] == name:
            habit[2] = "Done"
            habit[3] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_habits(habits)

def edit_habit(old_name, new_name, new_freq):
    habits = load_habits()
    for habit in habits:
        if habit[0] == old_name:
            habit[0] = new_name
            habit[1] = new_freq
    save_habits(habits)

def delete_habit(name):
    habits = load_habits()
    habits = [habit for habit in habits if habit[0] != name]
    save_habits(habits)

def set_reminder(name, time):
    notification.notify(
        title=f"Reminder for {name}",
        message=f"Time to complete your habit: {name}",
        timeout=10
    )

# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(page_title="Habit Tracker", page_icon="📋")

# 📋 Baby pink background
page_bg = """
<style>
body {
    background-color: #FADADD;
}
.stApp {
    background-color: #FADADD;
}
div[data-testid="stToolbar"] {display: none;}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("📋 Habit Tracker App")

# 🔵 Blue buttons
button_style = """
<style>
div.stButton > button {
    background-color: #2196F3;
    color: white;
    border-radius: 10px;
    height: 2.8em;
    width: 100%;
    font-size: 16px;
}
div.stButton > button:hover {
    background-color: #1E88E5;
}
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# --------------------------
# Functionality
# --------------------------

option = st.sidebar.selectbox("Choose Action", [
    "Add Habit", "View Habits", "Mark as Done", "Edit Habit", "Set Reminder", "Delete Habit"
])

if option == "Add Habit":
    st.header("Add New Habit")
    name = st.text_input("Habit Name")
    freq = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
    if st.button("Add Habit"):
        if name:
            add_habit(name, freq)
            st.success(f"✅ Habit '{name}' added successfully!")
        else:
            st.warning("Please enter a habit name!")

elif option == "View Habits":
    st.header("Your Habits")
    habits = load_habits()
    if habits:
        for h in habits:
            name = h[0] if len(h) > 0 else "Unnamed Habit"
            frequency = h[1] if len(h) > 1 else "N/A"
            status = h[2] if len(h) > 2 else "Unknown"
            last_done = h[3] if len(h) > 3 and h[3] else "Never"

            st.write(f"🌿 **{name}** — {frequency} — Status: {status} — Last Done: {last_done}")
    else:
        st.info("No habits found! Try adding one.")

elif option == "Mark as Done":
    st.header("Mark Habit as Done")
    habits = [h[0] for h in load_habits()]
    if habits:
        choice = st.selectbox("Select Habit", habits)
        if st.button("Mark as Done"):
            mark_done(choice)
            st.success(f"🌟 Marked '{choice}' as Done!")
    else:
        st.warning("No habits to mark!")

elif option == "Edit Habit":
    st.header("Edit Habit")
    habits = [h[0] for h in load_habits()]
    if habits:
        old = st.selectbox("Select Habit to Edit", habits)
        new_name = st.text_input("New Name")
        new_freq = st.selectbox("New Frequency", ["Daily", "Weekly", "Monthly"])
        if st.button("Edit Habit"):
            edit_habit(old, new_name, new_freq)
            st.success(f"✏️ Updated '{old}' to '{new_name}'!")
    else:
        st.warning("No habits available!")

elif option == "Set Reminder":
    st.header("Set Reminder")
    habits = [h[0] for h in load_habits()]
    if habits:
        habit = st.selectbox("Choose Habit", habits)
        reminder_time = st.time_input("Select Time")
        if st.button("Set Reminder"):
            set_reminder(habit, reminder_time)
            st.success(f"⏰ Reminder set for '{habit}' at {reminder_time}")
    else:
        st.warning("No habits found to set reminders!")

elif option == "Delete Habit":
    st.header("Delete Habit")
    habits = [h[0] for h in load_habits()]
    if habits:
        habit_to_delete = st.selectbox("Select Habit to Delete", habits)
        if st.button("Delete Habit"):
            delete_habit(habit_to_delete)
            st.success(f"🗑️ Habit '{habit_to_delete}' deleted successfully!")
    else:
        st.warning("No habits to delete!")

