import streamlit as st
import mysql.connector
import hashlib

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="landonkillian",
    database="medical_trialsf"
)
cursor = db_connection.cursor()

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_phone_number(phone_number):
    return phone_number.isdigit() and len(phone_number) == 10

# Streamlit app for Trial Center Registration
def register_trial_center():
    st.title("Trial Center Registration")

    # Input fields for registration
    #center_id = st.text_input("Center ID")
    name = st.text_input("Center Name")
    password = st.text_input("Password ", type="password")
    facility_type = st.selectbox("Facility Type", ['Research Center', 'Hospital', 'Independent'])
    address = st.text_area("Address")
    contact_number = st.text_input("Enter Contact Number (10 digits):", max_chars=10)
    valid_contact_number = is_valid_phone_number(contact_number)
    # Validate the input
    if valid_contact_number:
        st.success("Valid phone number!")
        # Use the phone_number variable in your application logic
    else:
        st.warning("Please enter a valid 10-digit phone number.")

    # Validate that all required fields are filled
    all_fields_filled = all([name, password, facility_type, address, contact_number])
    
    # Enable or disable the submission button based on validation
    submit_button = st.button("Submit", disabled=not (all_fields_filled and valid_contact_number))

    # Show a message if any required field is not filled
    if not all_fields_filled:
        st.warning("Please fill in all the required fields.")

    if submit_button:
        # Hash the password before storing it in the database
        hashed_password = hash_password(password)
        # Insert the data into the database
        insert_query = "INSERT INTO Trial_center ( Name, Password, Facility_Type, Address, Contact_number) VALUES ( %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, ( name, hashed_password, facility_type, address, contact_number))
        db_connection.commit()

        st.success("Registration successful!")

if __name__ == "__main__":
    register_trial_center()