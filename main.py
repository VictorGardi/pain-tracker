import streamlit as st
from pages import show_progress, add_progress
from utils import connect_to_db, login

st.header('Pain Tracker')

def run_app():
    with st.sidebar:
        choice = st.radio("What do you want to do today?", ["Show progress","Add progress"])

    if choice == "Show progress":
        show_progress()
    elif choice == "Add progress":
        add_progress()

def main() -> None:
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        login()
    if st.session_state.logged_in:
        st.session_state.db = connect_to_db()
        run_app()


if __name__ == "__main__":
    main()


