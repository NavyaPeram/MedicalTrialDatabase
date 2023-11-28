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

def is_valid_phone_number(phone_number):
    return phone_number.isdigit() and len(phone_number) == 10


blood_groups = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]

# Function to update patient information
def update_patient_info(patients_id, new_age, new_weight, new_height, new_blood_group, new_contact_number, new_conditions, new_allergies, new_family_history):
    cursor.callproc('UpdatePatientInfo',(patients_id, new_age, new_weight, new_height, new_blood_group, new_contact_number, new_conditions, new_allergies, new_family_history))
    db_connection.commit()
    st.success(f"Patient Info with name {patients_id} updated successfully!")

        # Get the success status from the OUT parameter
    # cursor.execute("SELECT @_UpdatePatientInfo_12")
    # success = cursor.fetchone()

    # if success:
    #     st.success("Patient information updated successfully!")
    # else:
    #     st.error("Patient not found. Update failed.")

# Streamlit UI
def main1():
    st.title("Update Patient Information")

    # Get user input for updating patient information
    patients_id = st.text_input("Enter Patient ID:")
    new_age = st.number_input("Enter New Age:", min_value=1, step=1)
    new_weight = st.number_input("Enter New Weight:", min_value=0.0, step=0.1)
    new_height = st.number_input("Enter New Height:", min_value=0.0, step=0.1)
    new_blood_group = st.selectbox("Select New Blood Group:", blood_groups)
    contact_number = st.text_input("Enter Contact Number (10 digits):", max_chars=10)
    valid_contact_number = is_valid_phone_number(contact_number)
    # Validate the input
    if valid_contact_number:
        st.success("Valid phone number!")
        # Use the phone_number variable in your application logic
    else:
        st.warning("Please enter a valid 10-digit phone number.")
    new_conditions = st.text_area("Enter New Conditions:")
    new_allergies = st.text_area("Enter New Allergies:")
    new_family_history = st.text_area("Enter New Family History:")

    if st.button("Update Patient Information"):
        update_patient_info(patients_id, new_age, new_weight, new_height, new_blood_group, contact_number, new_conditions, new_allergies, new_family_history)

if __name__ == "__main__":
    main1()
