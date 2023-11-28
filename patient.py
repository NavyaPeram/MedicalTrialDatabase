import streamlit as st
import mysql.connector
import hashlib
from streamlit import session_state as state
from updatepatient import main1
from dlete import emgmain
from patientdel import delpatient

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="landonkillian",
    database="medical_trialsf"
)
cursor = db_connection.cursor()

# Function to hash the password
def hash_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed

def is_valid_phone_number(phone_number):
    return phone_number.isdigit() and len(phone_number) == 10

# Predefined list of secret questions
secret_questions = [
    "What is the name of your first pet?",
    "In what city were you born?",
    "What is your favorite movie?",
    "Who is your childhood best friend?",
    "What is the name of your favorite teacher?"
]

# Streamlit app for patient data entry
def patient_data_entry1():
    st.title("Patient Registration")

    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    secretquestion = st.selectbox("Select Secret Question", secret_questions)
    secretanswer = st.text_input("Secret Answer", type="password")
    age = st.number_input("Age", min_value=0, max_value=100, value=0, step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    weight = st.number_input("Weight (kg)", min_value=0, max_value=150, step=1)
    height = st.number_input("Height (cm)", min_value=0, max_value=200, step=1)
    blood_group = st.selectbox("Blood Group", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
    contact_number = st.text_input("Enter Contact Number (10 digits):", max_chars=10)
    valid_contact_number = is_valid_phone_number(contact_number)
    # Validate the input
    if valid_contact_number:
        st.success("Valid phone number!")
        # Use the phone_number variable in your application logic
    else:
        st.warning("Please enter a valid 10-digit phone number.")
        
    conditions = st.text_area("Medical Conditions-if any")
    allergies = st.text_area("Allergies-if any")
    family_history = st.text_area("Family History-if any")

    st.title("Emergency Contact Entry")
    name_er = st.text_input("Name of emergency contact")
    contact_number_er = st.text_input("Enter Contact Number of emergency contact (10 digits):", max_chars=10)
    valid_contact_number_er = is_valid_phone_number(contact_number_er)
    # Validate the input
    if valid_contact_number_er:
        st.success("Valid phone number!")
        # Use the phone_number variable in your application logic
    else:
        st.warning("Please enter a valid 10-digit phone number.")

    # Validate that all required fields are filled
    all_fields_filled = all([name, password, secretquestion, secretanswer, age, gender, weight, height, blood_group, contact_number, conditions, allergies, family_history, name_er, contact_number_er])
    

    # Enable or disable the submission button based on validation
    submit_button = st.button("Submit", disabled=not (all_fields_filled and valid_contact_number and valid_contact_number_er))

    # Show a message if any required field is not filled
    if not all_fields_filled:
        st.warning("Please fill in all the required fields.")

    if submit_button:
        hashed_password = hash_password(password)
        insert_patient_query = "INSERT INTO Patient (Name, password, secretquestion, secretanswer, Age, Gender, Weight, Height, Blood_group, Contact_number, Conditions, Allergies, Family_history ) VALUES ( %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_emergency_query = "INSERT INTO Emergency_reference (Name, Contact_number) VALUES (%s, %s)"
        cursor.execute(insert_patient_query, (name, hashed_password, secretquestion, secretanswer, age, gender, weight, height, blood_group, contact_number, conditions, allergies, family_history))
        cursor.execute(insert_emergency_query, (name_er, contact_number_er))
        db_connection.commit()
        st.success("Patient data successfully submitted!")
        

# Sample Streamlit app
def patient():
    #patient_data_entry1()
    selected_page = st.sidebar.radio("Navigation", ["Register Patient","Update Patient","Delete Emergency Reference","Delete Patient"])

    
    if selected_page == "Register Patient":
        patient_data_entry1()
    elif selected_page == "Update Patient":
        main1()
    elif selected_page == "Delete Emergency Reference":
        emgmain()
    elif selected_page == "Delete Patient":
        delpatient()
    

if __name__ == "__main__":
    patient()