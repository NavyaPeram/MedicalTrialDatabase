#login.py
import pandas as pd
import streamlit as st
import mysql.connector
import hashlib
from center import register_trial_center
from team import register_research_team
from participantinfo import participant_info
from medicaldrug import insert_medical_drug
from datetime import date

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="landonkillian",
    database="medical_trialsf"
)
cursor = db_connection.cursor()

def update_medical_drug(team_id):
    st.title("Update Medical Drug")

    drug_id = st.text_input("Enter Drug ID to update:")
    common_name = st.text_input("Enter Common Name:")
    chemical_name = st.text_input("Enter Chemical Name:")
    administration_mode = st.selectbox("Select Administration Mode", ["Oral", "Intravenous", "Nasal", "Dermal"])
    side_effects = st.text_area("Enter Side Effects:")
    compensation = st.number_input("Enter Compensation:", min_value=0.0, step=0.01)

    if st.button("Update Medical Drug"):
        # Query to update medical drug
        update_query = "UPDATE Medical_drug SET Common_name=%s, Chemical_name=%s, " \
                       "Administration_mode=%s, Side_effects=%s, compensation=%s, Team_ID=%s WHERE Drug_id=%s"

        cursor.execute(update_query, (common_name, chemical_name,  administration_mode,
                                      side_effects, compensation, team_id, drug_id))
        db_connection.commit()
        st.success("Medical drug updated successfully!")

def update_clinical_trial(team_id):
    st.title("Update Clinical Trial")

    trial_id = st.text_input("Enter Trial ID to update:")
    trial_name = st.text_input("Enter Trial Name:")
    start_date = st.date_input("Select Start Date:")
    end_date = st.date_input("Select Expected End Date:")
    outcome = st.text_area("Enter Outcome:")
    num_subjects = st.number_input("Enter Number of Subjects:", min_value=0)
    budget = st.number_input("Enter Budget:", min_value=0.0, step=0.01)

    if st.button("Update Clinical Trial"):
        # Query to update clinical trial
        update_query = "UPDATE Clinical_trial SET Trial_name=%s, Start_date=%s, Expected_enddate=%s, " \
                       "Outcome=%s, Number_of_subjects=%s, Budget=%s, Team_ID=%s WHERE Trial_ID=%s"

        cursor.execute(update_query, (trial_name, start_date, end_date, outcome, num_subjects, budget, team_id, trial_id))
        db_connection.commit()
        st.success("Clinical trial updated successfully!")

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to validate login credentials
def validate_login(username, password):
    query_patient = "SELECT Patient_ID, Password FROM Patient WHERE Name = %s"
    query_trial_center = "SELECT Center_ID, Password FROM Trial_Center WHERE Name = %s"
    query_research_team = "SELECT Team_ID, Password FROM Research_team WHERE Team_name = %s"

    cursor.execute(query_patient, (username,))
    result_patient = cursor.fetchone()
    if result_patient and verify_password(password, result_patient[1]):
        return result_patient[0], 'Patient'

    cursor.execute(query_trial_center, (username,))
    result_trial_center = cursor.fetchone()
    if result_trial_center and verify_password(password, result_trial_center[1]):
        return result_trial_center[0], 'Trial_Center'

    cursor.execute(query_research_team, (username,))
    result_research_team = cursor.fetchone()
    if result_research_team and verify_password(password, result_research_team[1]):
        return result_research_team[0], 'Research_team'

    return None

# Function to verify the entered password against the stored hashed password
def verify_password(entered_password, hashed_password):
    return hashlib.sha256(entered_password.encode()).hexdigest() == hashed_password

def home_page_patient(user_id):
    st.title("Patient Home Page")
    st.write(f"Patient ID: {user_id}")
    print(user_id)
    # Specify the patient_id you want to retrieve information for
    patient_id_to_query = user_id

    # Execute the SQL query
    query = """
        SELECT
            pi.Patient_ID,
            pi.Drug_id,
            md.Compensation,
            pi.dosage,
            pi.remarks
        FROM
            Participant_info pi
        JOIN
            Medical_drug md ON pi.Drug_id = md.Drug_id
        WHERE
            pi.Patient_ID = %s
        ORDER BY
            md.compensation;
    """

    sum_query="""
        SELECT
            pi.Patient_ID,
            sum(md.Compensation) as total_compensation
        FROM
            Participant_info pi
        JOIN
            Medical_drug md ON pi.Drug_id = md.Drug_id
        WHERE
            pi.Patient_ID = %s; 
    """

    cursor.execute(query, (patient_id_to_query,))
    participant_info = cursor.fetchall()

    cursor.execute(sum_query, (patient_id_to_query,))
    sum_info = cursor.fetchall()

    # Check if any participant_info is returned before accessing the values
    if participant_info:
        headers = ["Patient ID", "Drug ID", "Compensation", "Dosage", "Remarks"]
        df = pd.DataFrame(participant_info, columns=headers)

        # Display the clinical trial information in a table
        st.table(df.set_index(pd.Index(range(1, len(df) + 1))))

        sum_info = sum(row[2] for row in participant_info)
        st.write(f"Total compensation received is: {sum_info:.2f}")
    else:
        st.warning("No participant info found for the specified patient ID.")
            # Add patient-specific content for Home Page here

def about_page_patient(user_id):
    st.title("Drug Info")
    st.write(f"Patient ID: {user_id}")
    # Add patient-specific content for About Page here
    drug_info="""
        SELECT
            Drug_id,
            Common_name,
            Administration_mode,
            Side_effects,
            compensation
        FROM
            medical_drug
        WHERE
            drug_id 
            IN(
            SELECT
                drug_id
            FROM
                participant_info
            WHERE
                patient_id = %s);
    """
    cursor.execute(drug_info, (user_id,))
    info = cursor.fetchall()

    # Check if any participant_info is returned before accessing the values
    if info:
        headers = ["Drug ID", "Drug Name", "Administration Mode", "Side Effects", "Compensation"]
        df = pd.DataFrame(info, columns=headers)

        # Display the clinical trial information in a table
        st.table(df.set_index(pd.Index(range(1, len(df) + 1))))

    else:
        st.warning("No drug info found for the specified patient ID.")
            # Add patient-specific content for Home Page here

def home_page_research_team(user_id):
    st.title("Drug Information Page")
    st.write(f"Research Team ID: {user_id}")
    drugs="""
        SELECT
            Drug_id,
            Trial_id,
            Common_name,
            Chemical_name,
            Administration_mode,
            Side_effects,
            compensation
        FROM
            medical_drug
        WHERE
            team_id = %s;
    """
    cursor.execute(drugs, (user_id,))
    info = cursor.fetchall()

    # Check if any participant_info is returned before accessing the values
    if info:
        headers = ["Drug ID", "Trial ID", "Common Name", "Chemical Name", "Administration Mode", "Side Effects", "Compensation"]
        df = pd.DataFrame(info, columns=headers)

        # Display the clinical trial information in a table
        st.table(df.set_index(pd.Index(range(1, len(df) + 1))))

    else:
        st.warning("No drug info found for the specified team ID.")
            # Add patient-specific content for Home Page here

    # Add research team-specific content for Home Page here

def about_page_research_team(user_id):
    st.title("Participant Page")
    st.write(f"Research Team ID: {user_id}")
    # Add research team-specific content for About Page here
    patient_info="""
        SELECT
            participant_info.patient_id, 
            drug_id, 
            age, 
            gender, 
            weight, 
            height, 
            blood_group, 
            conditions, 
            allergies, 
            family_history,
            dosage, 
            remarks, 
            entry_date
        FROM
            participant_info
        JOIN 
            patient on participant_info.patient_id=patient.patient_id
        WHERE
            drug_id 
            IN(
            SELECT
                drug_id
            FROM
                medical_drug
            WHERE
                team_id = %s);
    """
    cursor.execute(patient_info, (user_id,))
    info = cursor.fetchall()

    # Check if any participant_info is returned before accessing the values
    if info:
        headers = ["Participant ID", "Drug ID", "Age", "Gender", "Weight", "Height", "Blood Group", "Conditions", "Allergies", "Family History", "Dosage", "Remarks", "Entry Date"]
        df = pd.DataFrame(info, columns=headers)

        # Display the clinical trial information in a table
        st.table(df.set_index(pd.Index(range(1, len(df) + 1))))

    else:
        st.warning("No participant info found for the specified team ID.")
            # Add patient-specific content for Home Page here

def home_page_trial_center(user_id):
    st.title("Trial Center Home Page")
    st.write(f"Trial Center ID: {user_id}")
    center_info="""
        SELECT
            patient_id, 
            drug_id, 
            center_id, 
            dosage, 
            remarks, 
            entry_date
        FROM
            participant_info
        WHERE
            center_id 
            IN(
            SELECT
                center_id
            FROM
                trial_center
            WHERE
                center_id = %s);
    """
    cursor.execute(center_info, (user_id,))
    info = cursor.fetchall()

    # Check if any participant_info is returned before accessing the values
    if info:
        headers = ["Participant ID", "Drug ID", "Center ID", "Dosage", "Remarks", "Entry Date"]
        df = pd.DataFrame(info, columns=headers)

        # Display the clinical trial information in a table
        st.table(df.set_index(pd.Index(range(1, len(df) + 1))))

    else:
        st.warning("No info found for the specified center ID.")
    # Add research team-specific content for Home Page here

def about_page_trial_center(user_id):
    st.title("Current Trials Page")
    st.write(f"Trial Center ID: {user_id}")

    trials="""
        SELECT
            CT.trial_id, 
            CT.trial_name, 
            CT.start_date, 
            CT.expected_enddate,  
            MD.Drug_id, 
            MD.Common_name,
            MD.Chemical_name,
            RT.Company
        FROM
            Clinical_trial CT
        JOIN
            Medical_drug MD ON CT.Trial_ID = MD.Trial_ID
        JOIN
             Research_team RT ON MD.Team_ID = RT.Team_ID
        WHERE
            CT.Start_date <= CURDATE()and CT.Expected_enddate >= CURDATE();
    """
    cursor.execute(trials)
    info = cursor.fetchall()

    # Check if any participant_info is returned before accessing the values
    if info:
        headers = ["Trial ID", "Trial Name", "Start date", "Expected End Date", "Drug ID", "Common Name", "Chemical Name", "Company"]
        df = pd.DataFrame(info, columns=headers)

        # Display the clinical trial information in a table
        st.table(df.set_index(pd.Index(range(1, len(df) + 1))))

    else:
        st.warning("No drug info found for the specified center ID.")


# def patient_pages(user_id):
#     st.title("Patient Pages")
#     st.write(f"Patient ID: {user_id}")
#     # Add patient-specific content here

def login_page():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login_result = validate_login(username, password)

        if login_result:
            user_id, user_type = login_result
            st.success(f"Login successful! User ID: {user_id}, User Type: {user_type}")
           
            # return user_id, user_type
            if user_type == 'Patient':
                # patient_pages(user_id)
                st.title("Patient Pages")
                # Home Page expander
                with st.expander("Home Page"):
                    home_page_patient(user_id)

                # About Page expander
                with st.expander("Drug Information Page"):
                    about_page_patient(user_id)



            elif user_type == 'Research_team':
                st.title("Research Team Pages")

                # Home Page expander
                with st.expander("Home Page"):
                    home_page_research_team(user_id)

                # About Page expander
                with st.expander("Participant Info Page"):
                    about_page_research_team(user_id)



            elif user_type == 'Trial_Center':
                st.title("Trial Center Pages")
                # Home Page expander
                with st.expander("Home Page"):
                    home_page_trial_center(user_id)

                # About Page expander
                with st.expander("Current Trials Page"):
                    about_page_trial_center(user_id)

        else:
            st.error("Invalid login credentials")

if __name__ == "__main__":
    login_page()