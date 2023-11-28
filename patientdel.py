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

def delete_patientinfo(patient_id):
    # Delete emergency reference information for the specified patient
    delete_query = "UPDATE PATIENT set password=NULL, secretquestion=NULL,secretanswer=NULL, contact_number=NULL where Patient_ID=%s"
    #delete_query = "UPDATE PATIENT FROM Emergency_reference WHERE Patient_ID = %s"
    cursor.execute(delete_query, (patient_id,))
    db_connection.commit()
    st.success("Patient information deleted successfully!")

def delete_emg(patient_id):
    # Delete emergency reference information for the specified patient
    delete_query = "DELETE FROM Emergency_reference WHERE Patient_ID = %s"
    cursor.execute(delete_query, (patient_id,))
    db_connection.commit()
    st.success("Emergency reference information deleted successfully!")

def delpatient():
    st.title("Delete Patient Info")

    # Get user input for patient ID
    patient_id = st.text_input("Enter Patient ID:")

    # Button to delete emergency reference information
    if st.button("Delete P"):
        delete_patientinfo(patient_id)
        delete_emg(patient_id)

    

if __name__ == "__main__":
    delpatient()

