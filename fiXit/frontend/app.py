# frontend/app.py

import streamlit as st
from pages import home, results

PAGES = {
    "Home": home,
    "Results": results
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()
