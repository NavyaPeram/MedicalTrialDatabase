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

# Streamlit app for Research Team Registration
def register_research_team():
    st.title("Research Team Registration")

    # Input fields for registration
    #team_id = st.text_input("Team ID")
    name = st.text_area("Employee Names:")
    team_name = st.text_input("Team name:")
    company = st.text_input("Company:")
    password = st.text_input("Password:", type="password")

    # Validate that all required fields are filled
    all_fields_filled = all([name, company, password])
    
    # Enable or disable the submission button based on validation
    submit_button = st.button("Submit", disabled=not (all_fields_filled))

    # Show a message if any required field is not filled
    if not all_fields_filled:
        st.warning("Please fill in all the required fields.")

    if submit_button:
        # Hash the password before storing it in the database
        hashed_password = hash_password(password)

        # Insert the data into the database
        insert_query = "INSERT INTO Research_team ( Name,Team_name, Company, Password) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, ( name, team_name, company, hashed_password))
        db_connection.commit()

        st.success("Registration successful!")


if __name__ == "__main__":
    register_research_team()

    