#RESEARCH TEAM DASHBOARD
import streamlit as st
import mysql.connector
import pandas as pd
from medicaldrug import insert_medical_drug
from participantinfo import participant_info
from updateclinicaltrial import clinicaltrialworks
from particpatient import patientmain

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="landonkillian",
    database="medical_trialsf"
)
cursor = db_connection.cursor()

def enter_clinical_trial_info():
    st.title("Enter Clinical Trial Information")

    # Get user input for entering clinical trial information
    trial_id = st.text_input("Enter Trial ID:")
    trial_name = st.text_input("Enter Trial Name:")
    start_date = st.date_input("Enter Start Date:")
    expected_end_date = st.date_input("Enter Expected End Date:")
    outcome = st.text_area("Enter Outcome:")
    num_subjects = st.number_input("Enter Number of Subjects:", min_value=1, step=1)
    budget = st.number_input("Enter Budget:", min_value=0.0, step=0.01)

    # Insert clinical trial information into the database
    if st.button("Submit Clinical Trial Information"):
        query = "INSERT INTO Clinical_trial (Trial_ID, Trial_name, Start_date, Expected_enddate, Outcome, Number_of_subjects, Budget) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (trial_id, trial_name, start_date, expected_end_date, outcome, num_subjects, budget)
        cursor.execute(query, values)
        db_connection.commit()
        st.success("Clinical trial information submitted successfully!")

def view_clinical_trial_info():
    st.title("Clinical Trial Information")

    # Fetch clinical trial information from the database
    query = "SELECT * FROM Clinical_trial"
    cursor.execute(query)
    clinical_trials = cursor.fetchall()

    # Convert the result to a DataFrame
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(clinical_trials, columns=columns)

    # Convert 'Start_date' and 'Expected_enddate' to 'datetime64[ns]'
    df['Start_date'] = pd.to_datetime(df['Start_date'])
    df['Expected_enddate'] = pd.to_datetime(df['Expected_enddate'])

    # Display the clinical trial information in a table
    st.table(df.set_index(pd.Index(range(1, len(df) + 1))))
    

def clinicalinformation():
    st.title("Research Team Dashboard")

    # Sidebar navigation
    selected_page = st.sidebar.radio("Navigation", ["Enter Clinical Trials", "View Clinical Trials","Update Clinical Trials","Add Medical Drugs","Add Participants","View ParticipantInfo"])

    # Display selected page content
    if selected_page == "Enter Clinical Trials":
        enter_clinical_trial_info()
    elif selected_page == "View Clinical Trials":
        view_clinical_trial_info()
    elif selected_page == "Update Clinical Trials":
        clinicaltrialworks()    
    elif selected_page == "Add Medical Drugs":
        insert_medical_drug()
    elif selected_page == "Add Participants":
        participant_info()
    elif selected_page == "View ParticipantInfo":
        patientmain()

if __name__ == "__main__":
    clinicalinformation()
