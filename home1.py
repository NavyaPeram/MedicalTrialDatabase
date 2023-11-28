import streamlit as st
import mysql.connector
# from rest2 import insert_user,secret_questions,validate_login,db_connection,cursor,update_password,user_register,user_login,user_forgot_password,user_patient
#from patient1 import get_patient_id,patient_data_entry
from patient import patient, hash_password
from team import register_research_team
from center import register_trial_center
from streamlit import session_state as state
from forgot import patient_forgot_password_page
from login1 import login_page
from clinicaltrial import clinicalinformation


def main():
    #st.title("User Registration and Login")

    page = st.sidebar.selectbox("Select Page", ["Patient Registration", "Research team Registration", "Center Registration", "Login", "Forgot Password","Research Team Dashboard"])


    
    if page == "Patient Registration":
        patient()

       

    elif page == "Research team Registration":
        register_research_team()


    elif page == "Center Registration":
        register_trial_center()


    elif page == "Login":
        login_page()


    elif page == "Forgot Password":
        patient_forgot_password_page()
    
    elif page == "Research Team Dashboard":
        clinicalinformation()
    

if __name__ == "__main__":
    main()