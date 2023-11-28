import streamlit as st
import mysql.connector
import hashlib

# Assuming you have established a database connection
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

# Function to check if provided information matches the database for a patient
def check_patient_info(name, secret_question, secret_answer):
    query = "SELECT Patient_ID FROM Patient WHERE Name = %s AND SecretQuestion = %s AND LOWER(SecretAnswer) = LOWER(%s)"

    cursor.execute(query, (name, secret_question, secret_answer))
    result = cursor.fetchone()

    if result:
        return result[0]  # Return the patient ID if information is correct
    else:
        return None

# Streamlit app for patient forgot password
def patient_forgot_password_page():
    st.title("Forgot Password")

    name = st.text_input("Name ")
    secret_question = st.selectbox("Select Secret Question", ["What is the name of your first pet?", "In what city were you born?", "What is your favorite movie?", "Who is your childhood best friend?", "What is the name of your favorite teacher?"])
    secret_answer = st.text_input("Secret Answer")
    new_password = st.text_input("Enter New Password", type="password")

    if st.button("Submit"):
        patient_id = check_patient_info(name, secret_question, secret_answer)

        if patient_id:
            st.success(f"Patient information verified! Password updated successfully! You can now log in with your new password.")
            hashed_password = hash_password(new_password)
            
             # Update the password in the database for the patient
            update_query = "UPDATE Patient SET Password = %s WHERE Patient_ID = %s"
            cursor.execute(update_query, (hashed_password, patient_id))
            db_connection.commit()
            print(new_password)
        else:
            st.error("Invalid patient information. Please check your details and try again.")

# Main Streamlit app
def main():
    patient_forgot_password_page()

if __name__ == "__main__":
    main()
