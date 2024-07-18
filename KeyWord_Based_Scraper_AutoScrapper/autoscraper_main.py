from autoscraper import AutoScraper
import streamlit as st


st.title("AutoScraper")

# First text input
url = st.text_input("Enter your url :", "")

# Second text input
key_word = st.text_input("Enter your keyword:", "")

# Button to trigger action
if st.button("Submit"):
    if url and key_word:
        st.success(f"You entered: {url} and {key_word}")
        keyword_list = key_word.split(",")
        
        wanted_list = [s.strip() for s in keyword_list]
        print(wanted_list)
        scraper = AutoScraper()
        result = scraper.build(url, wanted_list)
        st.write(result)
    else:
        st.warning("Please enter both inputs.")

