# prticipant_info.py
import streamlit as st
import mysql.connector
import hashlib

def participant_info():
    st.title("Insert Participant Information")

    # Connect to the MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="landonkillian",
        database="medical_trialsf"
    )
    cursor = db_connection.cursor()

    patient_id = st.text_input("Enter Patient ID:")
    drug_id = st.text_input("Enter Drug ID:")
    center_id = st.text_input("Enter Center ID:")
    dosage = st.text_input("Enter Dosage given:")
    remarks = st.text_area("Enter Remarks(if any):")
    entry_date = st.date_input("Enter the entry date:")

    if st.button("Insert Participant Info"):
        # Query to update medical drug
        update_query = "INSERT INTO Participant_info (Patient_ID, Drug_id, Center_ID, dosage, remarks, entry_date) VALUES ( %s, %s, %s,%s, %s, %s)"

        cursor.execute(update_query, (patient_id, drug_id, center_id, dosage, remarks, entry_date))
        db_connection.commit()
        st.success("Patient Information inserted successfully!")

def main():
        participant_info()

    

if __name__ == "__main__":
    main()