import streamlit as st
import os
import json
import time
from pathlib import Path

from agent.memory import Memory
from agent.understanding import Understanding
from agent.planning import Planner
from agent.execution import Executor
from config import DEFAULT_WORKSPACE

# Initialize the agent components
memory = Memory()
understanding = Understanding(memory)
planner = Planner(memory)
executor = Executor(memory)

# Page setup
st.set_page_config(
    page_title="File Organization Agent",
    page_icon="📁",
    layout="wide"
)

# App title and description
st.title("📁 File Organization Agent")
st.markdown("""
This tool helps you organize and find files using simple natural language commands.
Simply tell the agent what you want to do, and it will handle the rest.
""")

# Sidebar for agent memory and settings
with st.sidebar:
    st.header("Agent Memory")
    
    # Show recent actions
    recent_actions = memory.get_recent_actions(5)
    if recent_actions:
        st.subheader("Recent Actions")
        for action in recent_actions:
            with st.expander(f"{action['type']} - {action['timestamp'][:16]}"):
                st.json(action['details'])
    else:
        st.info("No actions recorded yet.")
    
    # Settings
    st.subheader("Settings")
    
    # Display current workspace
    current_workspace = memory.get_preference("last_directory", DEFAULT_WORKSPACE)
    st.text_input("Current Workspace", current_workspace, disabled=True)
    
    # Option to change workspace
    new_workspace = st.text_input("Change Workspace (leave empty to keep current)")
    if new_workspace:
        if os.path.exists(new_workspace):
            memory.update_preference("last_directory", new_workspace)
            st.success(f"Workspace updated to: {new_workspace}")
            st.experimental_rerun()
        else:
            st.error("Directory does not exist.")
    
    # Debug mode toggle
    debug_mode = st.toggle("Developer Mode", value=False, 
                          help="Show technical details like parsing and planning")

# Main interaction area
st.header("What would you like me to do?")

# Input box for user command
user_input = st.text_input("Enter your request", 
                          placeholder="E.g., 'organize my downloads by file type' or 'find PDFs in documents'")

# Process user input when submitted
if user_input:
    # Create a status area
    status_container = st.empty()
    
    # Process the request without showing technical details
    with status_container.container():
        st.info("Processing your request...")
        
        # Understanding phase
        parsed_request = understanding.parse_request(user_input)
        
        # Planning phase
        plan = planner.create_plan(parsed_request)
        
        # Only show the technical details if debug mode is on
        if debug_mode:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Understanding")
                st.json(parsed_request)
            with col2:
                st.subheader("Planning")
                st.json(plan)
    
    # Clear the status message
    status_container.empty()
    
    # Execute immediately if we understand the request
    if plan["action"] != "unknown":
        with st.spinner(f"Executing: {plan['description']}..."):
            try:
                # Execute the plan based on the action type
                if plan["action"] == "organize_by_type":
                    result = executor.organize_by_type(plan["directory"])
                    memory.update_preference("last_directory", plan["directory"])
                    
                elif plan["action"] == "organize_by_date":
                    result = executor.organize_by_date(
                        plan["directory"],
                        plan["use_modified"]
                    )
                    memory.update_preference("last_directory", plan["directory"])
                    
                elif plan["action"] == "find_files_by_type":
                    result = executor.find_files_by_type(
                        plan["directory"],
                        plan["file_type"]
                    )
                    memory.update_preference("last_directory", plan["directory"])
                    
                elif plan["action"] == "find_file_by_name":
                    result = executor.find_file_by_name(
                        plan["directory"],
                        plan["file_name"]
                    )
                    memory.update_preference("last_directory", plan["directory"])
                
                # Only show raw results in debug mode
                if debug_mode:
                    with st.expander("Raw execution results"):
                        st.json(result)
            
            except Exception as e:
                st.error(f"Error during execution: {str(e)}")
                st.stop()
        
        # Display results in a user-friendly format
        if plan["action"] == "organize_by_type":
            st.success(f"✅ Organized {len(result['moved'])} files in {plan['directory']} by type.")
            
            # Show moved files in an expander
            if result['moved']:
                with st.expander("See organized files"):
                    # Group by type for better visualization
                    by_type = {}
                    for item in result['moved']:
                        file_type = item['type']
                        if file_type not in by_type:
                            by_type[file_type] = []
                        by_type[file_type].append(os.path.basename(item['from']))
                    
                    # Display by type
                    for file_type, files in sorted(by_type.items()):
                        st.subheader(f"{file_type}")
                        file_list = [f"- {file}" for file in sorted(files)]
                        st.text("\n".join(file_list))
            
            # Show errors if any
            if result['errors']:
                with st.expander(f"⚠️ Errors ({len(result['errors'])})"):
                    for err in result['errors']:
                        st.error(f"{os.path.basename(err['file'])}: {err['error']}")
        
        elif plan["action"] == "organize_by_date":
            st.success(f"✅ Organized {len(result['moved'])} files in {plan['directory']} by date.")
            
            # Show moved files in an expander
            if result['moved']:
                with st.expander("See organized files"):
                    # Group by date category for better visualization
                    by_date = {}
                    for item in result['moved']:
                        date_cat = item['date_category']
                        if date_cat not in by_date:
                            by_date[date_cat] = []
                        by_date[date_cat].append(os.path.basename(item['from']))
                    
                    # Display by date category
                    for date_cat, files in sorted(by_date.items()):
                        st.subheader(f"{date_cat}")
                        file_list = [f"- {file}" for file in sorted(files)]
                        st.text("\n".join(file_list))
            
            # Show errors if any
            if result['errors']:
                with st.expander(f"⚠️ Errors ({len(result['errors'])})"):
                    for err in result['errors']:
                        st.error(f"{os.path.basename(err['file'])}: {err['error']}")
        
        elif plan["action"] == "find_files_by_type":
            if result["error"]:
                st.error(f"Error while searching: {result['error']}")
            elif len(result["found"]) == 0:
                st.info(f"⚠️ No {plan['file_type']} files found in {plan['directory']}.")
            else:
                st.success(f"✅ Found {len(result['found'])} {plan['file_type']} files in {plan['directory']}.")
                
                # Display files in a clean format
                file_container = st.container()
                with file_container:
                    # Sort files alphabetically
                    sorted_files = sorted(result["found"], key=lambda x: os.path.basename(x).lower())
                    
                    # Display files with optional grouping
                    if len(sorted_files) > 10:
                        with st.expander("View all files"):
                            for file in sorted_files:
                                st.text(f"📄 {os.path.basename(file)}")
                    else:
                        for file in sorted_files:
                            st.text(f"📄 {os.path.basename(file)}")
        
        elif plan["action"] == "find_file_by_name":
            if result["error"]:
                st.error(f"Error while searching: {result['error']}")
            elif len(result["found"]) == 0:
                st.info(f"⚠️ No files matching '{plan['file_name']}' found in {plan['directory']}.")
            else:
                st.success(f"✅ Found {len(result['found'])} files matching '{plan['file_name']}'.")
                
                # Display files in a clean format
                file_container = st.container()
                with file_container:
                    # Sort files alphabetically
                    sorted_files = sorted(result["found"], key=lambda x: os.path.basename(x).lower())
                    
                    # Display files with optional grouping
                    if len(sorted_files) > 10:
                        with st.expander("View all files"):
                            for file in sorted_files:
                                st.text(f"📄 {os.path.basename(file)} (in {os.path.dirname(file)})")
                    else:
                        for file in sorted_files:
                            st.text(f"📄 {os.path.basename(file)}")
                            if debug_mode:
                                st.text(f"   Location: {os.path.dirname(file)}")
    else:
        st.warning("I don't understand what you want me to do. Please try rephrasing your request.")

# Add some example commands for first-time users
if not memory.get_recent_actions(1):
    st.divider()
    st.subheader("Example commands you can try:")
    st.markdown("""
    - "Organize my downloads folder by file type"
    - "Find all PDF files in my documents folder"
    - "Sort my desktop by date modified"
    - "Find files named 'report' in my downloads"
    """)

# Footer
st.divider()
st.markdown("*File Organization Agent* - Powered by Google Gemini 🧠")