import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the token from environment variable
TOKEN = os.environ.get("TOKEN")

def create_github_repo(token, repo_name, private=True, description=""):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {
        "name": repo_name,
        "private": private,
        "description": description,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# Streamlit UI
st.title("GitHub Repository Creator")

with st.form(key='repo_creation_form'):
    repo_name = st.text_input("Repository Name")
    description = st.text_input("Description")
    is_private = st.selectbox("Visibility", ["Public", "Private"]) == "Private"
    
    submit_button = st.form_submit_button(label='Create Repository')

    if submit_button:
        result = create_github_repo(TOKEN, repo_name, is_private, description)
        
        if "clone_url" in result:
            st.success(f"Repository created successfully!")
            clone_url = result['clone_url']
            
            # Display clone URL
            st.write(f"Clone URL: {clone_url}")

# Place the copy button outside the form
copy_button = st.button('Copy Clone URL')
if copy_button and "clone_url" in locals():
    st.write('<script>window.navigator.clipboard.writeText("' + clone_url + '");</script>', unsafe_allow_html=True)
    st.success('Clone URL copied to clipboard!')

if __name__ == "__main__":
    st.write("Enter repository details and click 'Create Repository'.")
