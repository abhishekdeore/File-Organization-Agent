import streamlit as st
import os
from pathlib import Path

# Page setup
st.set_page_config(
    page_title="File Organization Agent - Setup",
    page_icon="⚙️",
    layout="wide"
)

# App title and description
st.title("⚙️ File Organization Agent Setup")
st.markdown("""
Configure your file organization agent by providing the necessary API keys and settings.
""")

# Check if .env file exists
env_path = ".env"
existing_config = {}

if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                existing_config[key] = value
    
    st.success("Existing configuration found.")

# Configuration form
with st.form("config_form"):
    st.subheader("API Configuration")
    
    # Google API Key
    google_api_key = st.text_input(
        "Google Gemini API Key",
        value=existing_config.get("GOOGLE_API_KEY", ""),
        type="password",
        help="Get this from Google AI Studio"
    )
    
    st.subheader("Workspace Configuration")
    
    # Default workspace directory
    default_workspace = st.text_input(
        "Default Workspace Directory",
        value=existing_config.get("DEFAULT_WORKSPACE", str(os.path.join(Path.home(), "Documents", "agent_workspace"))),
        help="This is where files will be organized by default"
    )
    
    # Test connection
    test_connection = st.checkbox("Test API connection after saving", value=True)
    
    # Submit button
    submitted = st.form_submit_button("Save Configuration")
    
    if submitted:
        if not google_api_key:
            st.error("Google API Key is required.")
        else:
            # Save configuration to .env file
            with open(env_path, 'w') as f:
                f.write(f"GOOGLE_API_KEY={google_api_key}\n")
                f.write(f"DEFAULT_WORKSPACE={default_workspace}\n")
            
            # Create default workspace if it doesn't exist
            try:
                os.makedirs(default_workspace, exist_ok=True)
                
                st.success(f"""
                Configuration saved successfully!
                - API key: {'✓ Set' if google_api_key else '✗ Missing'}
                - Default workspace: {default_workspace} {'(Created)' if not os.path.exists(default_workspace) else '(Exists)'}
                """)
                
                # Test API connection if requested
                if test_connection and google_api_key:
                    st.info("Testing API connection...")
                    
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=google_api_key)
                        model = genai.GenerativeModel('gemini-2.0-flash')
                        response = model.generate_content("Say hello!")
                        
                        st.success("API connection successful! 🎉")
                    except Exception as e:
                        st.error(f"API connection failed: {str(e)}")
                
            except Exception as e:
                st.error(f"Failed to create workspace directory: {str(e)}")

# Instructions
st.markdown("""
### Next Steps

1. After saving your configuration, run the main application:

2. If you encounter any issues with the API key, double-check it in Google AI Studio.

3. If you need to change your configuration later, you can return to this setup page.
""")

# Footer
st.divider()
st.markdown("*File Organization Agent Setup* - Configuration Tool")
