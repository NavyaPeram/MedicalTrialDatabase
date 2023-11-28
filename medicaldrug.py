# research_team.py
import streamlit as st
import mysql.connector
import hashlib

def insert_medical_drug():
    st.title("Medical Drug Information")

    # Connect to the MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="landonkillian",
        database="medical_trialsf"
    )
    cursor = db_connection.cursor()

    drug_id = st.text_input("Enter Drug ID to update:")
    common_name = st.text_input("Enter Common Name:")
    chemical_name = st.text_input("Enter Chemical Name:")
    administration_mode = st.selectbox("Select Administration Mode", ["Oral", "Intravenous", "Nasal", "Dermal"])
    side_effects = st.text_area("Enter Side Effects:")
    team_id = st.text_input("Enter team ID to update:")
    trial_id = st.text_input("Enter trial ID to update:")
    compensation = st.number_input("Enter Compensation:", min_value=0.0, step=0.01)

    if st.button("Insert Medical Drug"):
        # Query to update medical drug
        update_query = "INSERT INTO medical_drug (common_name, chemical_name, administration_mode, side_effects, team_id, trial_id, compensation, drug_id) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(update_query, (common_name, chemical_name, administration_mode, side_effects, team_id, trial_id, compensation, drug_id))
        db_connection.commit()
        st.success("Medical drug inserted successfully!")

def main():
    insert_medical_drug()

if __name__ == "__main__":
    main()