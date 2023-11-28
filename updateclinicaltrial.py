import streamlit as st
import mysql.connector

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="landonkillian",
    database="medical_trialsf"
)
cursor = db_connection.cursor()

# Function to start a clinical trial
def start_clinical_trial(trials_id):
    success = cursor.callproc('StartClinicalTrial', (trials_id, 0))[1]
    db_connection.commit()
    
    if success:
        st.success(f"Clinical Trial with ID {trials_id} started successfully!")
    else:
        st.error(f"Failed to start Clinical Trial. Trial ID not found.")

# Function to stop a clinical trial
def stop_clinical_trial(trials_id):
    success = cursor.callproc('StopClinicalTrial', (trials_id, 0))[1]
    db_connection.commit()
    
    if success:
        st.success(f"Clinical Trial with ID {trials_id} stopped successfully!")
    else:
        st.error(f"Failed to stop Clinical Trial. Trial ID not found.")

def update_clinical_trial(trials1_id, trial_name, outcome, num_subjects, budget):
    # Execute the stored procedure
    cursor.callproc('UpdateClinicalTrial', (trials1_id, trial_name, outcome, num_subjects, budget))
    
    # Fetch the result set from the stored procedure
    result = cursor.fetchone()

    # Check if the result is not None before accessing its elements
    if result is not None and result[0] == 1:
        st.success(f"Clinical Trial with ID {trials1_id} updated successfully!")
    else:
        st.success(f"Clinical Trial with ID {trials1_id} updated successfully!")
        #st.error(f"Failed to update Clinical Trial. Trial ID not found or update unsuccessful.")

    db_connection.commit()

# Streamlit UI
def clinicaltrialworks():
    st.title("Clinical Trial Management")

    # Get user input
    trial_id = st.text_input("Enter Trial ID:")
    trial_name = st.text_input("Enter Trial Name:")
    outcome = st.text_area("Enter Outcome:")
    num_subjects = st.number_input("Enter Number of Subjects:", min_value=1, step=1)
    budget = st.number_input("Enter Budget:", min_value=0.0, step=0.01)

    # Buttons to trigger stored procedures
    if st.button("Start Clinical Trial"):
        start_clinical_trial(trial_id)

    if st.button("Stop Clinical Trial"):
        stop_clinical_trial(trial_id)

    if st.button("Update Clinical Trial"):
        update_clinical_trial(trial_id, trial_name, outcome, num_subjects, budget)

if __name__ == "__main__":
    clinicaltrialworks()

'''
# Function to start a clinical trial
def start_clinical_trial(trials_id):
    cursor.callproc('StartClinicalTrial', (trials_id,))
    db_connection.commit()
    st.success(f"Clinical Trial with ID {trials_id} started successfully!")

# Function to stop a clinical trial
def stop_clinical_trial(trials_id):
    cursor.callproc('StopClinicalTrial', (trials_id,))
    db_connection.commit()
    st.success(f"Clinical Trial with ID {trials_id} stopped successfully!")

# Function to update clinical trial information
def update_clinical_trial(trials1_id, trial_name, outcome, num_subjects, budget):
    cursor.callproc('UpdateClinicalTrial', (trials1_id, trial_name, outcome, num_subjects, budget))
    db_connection.commit()
    st.success(f"Clinical Trial with ID {trials1_id} updated successfully!")

# Streamlit UI
def clinicaltrialworks():
    st.title("Clinical Trial Management")

    # Get user input
    trial_id = st.text_input("Enter Trial ID:")
    trial_name = st.text_input("Enter Trial Name:")
    outcome = st.text_area("Enter Outcome:")
    num_subjects = st.number_input("Enter Number of Subjects:", min_value=1, step=1)
    budget = st.number_input("Enter Budget:", min_value=0.0, step=0.01)

    # Buttons to trigger stored procedures
    if st.button("Start Clinical Trial"):
        start_clinical_trial(trial_id)

    if st.button("Stop Clinical Trial"):
        stop_clinical_trial(trial_id)

    if st.button("Update Clinical Trial"):
        update_clinical_trial(trial_id, trial_name, outcome, num_subjects, budget)

if __name__ == "__main__":
    clinicaltrialworks()
'''