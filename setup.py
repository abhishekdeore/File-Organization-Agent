import os
import json
from pathlib import Path
from getpass import getpass

def setup_config():
    print("=" * 60)
    print("  File Organization Agent - Initial Setup")
    print("=" * 60)
    
    # Check if .env file exists
    env_path = ".env"
    if os.path.exists(env_path):
        print("An existing configuration was found.")
        change = input("Do you want to update the configuration? (y/n): ")
        if change.lower() != "y":
            print("Setup cancelled. Using existing configuration.")
            return
    
    # Get Google API key
    api_key = getpass("Enter your Google Gemini API key (input will be hidden): ")
    
    # Get default workspace
    default_dir = input("Enter default workspace directory (leave blank for Documents folder): ")
    if not default_dir:
        default_dir = os.path.join(Path.home(), "Documents", "agent_workspace")
    
    # Create .env file
    with open(env_path, "w") as f:
        f.write(f"GOOGLE_API_KEY={api_key}\n")
        f.write(f"DEFAULT_WORKSPACE={default_dir}\n")
    
    # Create default workspace if it doesn't exist
    os.makedirs(default_dir, exist_ok=True)
    
    print("\nConfiguration saved successfully!")
    print(f"Default workspace set to: {default_dir}")
    print("=" * 60)

if __name__ == "__main__":
    setup_config()