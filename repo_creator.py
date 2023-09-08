import streamlit as st
import requests
import json
import toml
import os

TOKEN = os.environ.get("github")


# Load the secrets from the TOML file
#secrets = toml.load("secrets.toml")
#TOKEN = secrets["github"]["token"]

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
            
            # Display clone URL and copy button
            st.write(f"Clone URL: {clone_url}")
            copy_button = st.button('Copy Clone URL')
            if copy_button:
                st.write('<script>window.navigator.clipboard.writeText("' + clone_url + '");</script>', unsafe_allow_html=True)
                st.success('Clone URL copied to clipboard!')
        else:
            st.error(f"Error creating repository: {result['message']}")

if __name__ == "__main__":
    st.write("Enter repository details and click 'Create Repository'.")
