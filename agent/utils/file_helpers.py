import os
import shutil
from datetime import datetime
from pathlib import Path

def get_file_type(file_path):
    """Get file type from extension"""
    extension = os.path.splitext(file_path)[1].lower().lstrip('.')
    if not extension:
        return "no_extension"
    return extension

def get_file_size_category(file_path):
    """Categorize file by size"""
    size_bytes = os.path.getsize(file_path)
    if size_bytes < 1024 * 100:  # Less than 100KB
        return "tiny"
    elif size_bytes < 1024 * 1024:  # Less than 1MB
        return "small"
    elif size_bytes < 1024 * 1024 * 10:  # Less than 10MB
        return "medium"
    elif size_bytes < 1024 * 1024 * 100:  # Less than 100MB
        return "large"
    else:
        return "huge"

def get_file_date_category(file_path, use_modified=True):
    """Categorize file by date (created or modified)"""
    if use_modified:
        timestamp = os.path.getmtime(file_path)
    else:
        timestamp = os.path.getctime(file_path)
    
    file_date = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    
    if file_date.year < now.year:
        return f"{file_date.year}"
    elif (now - file_date).days > 30:
        return f"{file_date.year}_{file_date.month:02d}"
    elif (now - file_date).days > 7:
        return "last_month"
    else:
        return "this_week"

def list_files_in_directory(directory):
    """List all files (not directories) in a directory"""
    return [os.path.join(directory, f) for f in os.listdir(directory) 
            if os.path.isfile(os.path.join(directory, f))]

def safe_create_directory(directory):
    """Create directory if it doesn't exist"""
    os.makedirs(directory, exist_ok=True)
    return directory

def safe_move_file(source, destination):
    """Move file with conflict resolution"""
    if not os.path.exists(destination):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(source, destination)
        return destination
    
    # Handle name conflict
    base, extension = os.path.splitext(destination)
    counter = 1
    while os.path.exists(destination):
        destination = f"{base}_{counter}{extension}"
        counter += 1
    
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    shutil.move(source, destination)
    return destination