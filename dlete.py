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

def is_valid_phone_number(contact_number):
    return contact_number.isdigit() and len(contact_number) == 10

def delete_emergency_reference(patient_id):
    # Delete emergency reference information for the specified patient
    delete_query = "DELETE FROM Emergency_reference WHERE Patient_ID = %s"
    cursor.execute(delete_query, (patient_id,))
    db_connection.commit()
    st.success("Emergency reference information deleted successfully!")
    
    # Return patient_id for use in insert_emergency_reference
    return patient_id

def insert_emergency_reference(name, contact_number, patient_id):
    # Insert new emergency reference information
    insert_query = "INSERT INTO Emergency_reference (Name, Contact_number, Patient_ID) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (name, contact_number, patient_id))
    db_connection.commit()
    st.success("Emergency Reference Submitted")

def emgmain():
    st.title("Emergency Reference Management")

    # Get user input for patient ID
    patient_id = st.text_input("Enter Patient ID:")

    # Button to delete emergency reference information
    if st.button("Delete Emergency Reference"):
        # Use the returned patient_id from delete_emergency_reference
        patient_id = delete_emergency_reference(patient_id)

    # Form to input new emergency reference information
    st.title("Enter Emergency Reference Information")

    name_er = st.text_input("Name of emergency contact")
    contact_number_er = st.text_input("Enter Contact Number of emergency contact (10 digits):", max_chars=10)
    valid_contact_number_er = is_valid_phone_number(contact_number_er)

    # Validate that all required fields are filled
    all_fields_filled = all([name_er, contact_number_er])

    # Enable or disable the submission button based on validation
    submit_button = st.button("Submit", disabled=not (all_fields_filled and valid_contact_number_er))

    # Show a message if any required field is not filled
    if not all_fields_filled:
        st.warning("Please fill in all the required fields.")

    # Button to insert new emergency reference information
    if submit_button:
        insert_emergency_reference(name_er, contact_number_er, patient_id)

if __name__ == "__main__":
    emgmain()

