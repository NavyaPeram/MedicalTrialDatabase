import streamlit as st
import mysql.connector
import pandas as pd

# Function to execute the stored procedure and fetch participant information
def get_participant_info(patient_name):
    try:
        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="landonkillian",
            database="medical_trialsf"
        )
        cursor = db_connection.cursor()

        # Call the stored procedure
        cursor.callproc("GetParticipantInfoForPatient", [patient_name])

        # Fetch the results
        result = []
        for result_cursor in cursor.stored_results():
            result.extend(result_cursor.fetchall())

        return result

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        # Close the database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()

# Streamlit app
def patientmain():
    st.title("Participant Information Lookup")

    # Get patient name from the user
    patient_name = st.text_input("Enter Patient Name:")

    if st.button("Get Participant Information"):
        # Call the stored procedure and get the participant information
        participant_info = get_participant_info(patient_name)

        # Display the results as a table
        if participant_info:
            df = pd.DataFrame(participant_info, columns=["Patient_ID", "Drug_ID", "Center_ID", "Dosage", "Remarks", "Entry_Date"])
            st.table(df)
        else:
            st.warning("No participant information found for the given patient name.")

if __name__ == "__main__":
    patientmain()



