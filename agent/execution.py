import os
from pathlib import Path
from agent.utils.file_helpers import (
    get_file_type, get_file_size_category, get_file_date_category,
    list_files_in_directory, safe_create_directory, safe_move_file
)

class Executor:
    def __init__(self, memory):
        self.memory = memory
        
    def organize_by_type(self, directory):
        """Organize files in directory by their type"""
        results = {"moved": [], "errors": []}
        
        try:
            files = list_files_in_directory(directory)
            
            for file_path in files:
                try:
                    file_type = get_file_type(file_path)
                    type_dir = os.path.join(directory, file_type)
                    safe_create_directory(type_dir)
                    
                    file_name = os.path.basename(file_path)
                    destination = os.path.join(type_dir, file_name)
                    moved_to = safe_move_file(file_path, destination)
                    
                    results["moved"].append({
                        "from": file_path,
                        "to": moved_to,
                        "type": file_type
                    })
                    
                except Exception as e:
                    results["errors"].append({
                        "file": file_path,
                        "error": str(e)
                    })
            
            # Log the action
            self.memory.add_action(
                "organize_by_type",
                {
                    "directory": directory,
                    "files_moved": len(results["moved"]),
                    "errors": len(results["errors"])
                },
                success=(len(results["errors"]) == 0)
            )
            
            return results
            
        except Exception as e:
            self.memory.add_action(
                "organize_by_type",
                {"directory": directory, "error": str(e)},
                success=False
            )
            raise
            
    def organize_by_date(self, directory, use_modified=True):
        """Organize files in directory by their date"""
        results = {"moved": [], "errors": []}
        
        try:
            files = list_files_in_directory(directory)
            
            for file_path in files:
                try:
                    date_category = get_file_date_category(file_path, use_modified)
                    date_dir = os.path.join(directory, date_category)
                    safe_create_directory(date_dir)
                    
                    file_name = os.path.basename(file_path)
                    destination = os.path.join(date_dir, file_name)
                    moved_to = safe_move_file(file_path, destination)
                    
                    results["moved"].append({
                        "from": file_path,
                        "to": moved_to,
                        "date_category": date_category
                    })
                    
                except Exception as e:
                    results["errors"].append({
                        "file": file_path,
                        "error": str(e)
                    })
            
            # Log the action
            self.memory.add_action(
                "organize_by_date",
                {
                    "directory": directory,
                    "use_modified": use_modified,
                    "files_moved": len(results["moved"]),
                    "errors": len(results["errors"])
                },
                success=(len(results["errors"]) == 0)
            )
            
            return results
            
        except Exception as e:
            self.memory.add_action(
                "organize_by_date",
                {"directory": directory, "error": str(e)},
                success=False
            )
            raise
            
    def find_files_by_type(self, directory, file_type):
        """Find all files of a specific type"""
        results = {"found": [], "error": None}
        
        try:
            files = list_files_in_directory(directory)
            
            for file_path in files:
                if get_file_type(file_path) == file_type:
                    results["found"].append(file_path)
            
            # Log the action
            self.memory.add_action(
                "find_files_by_type",
                {
                    "directory": directory,
                    "file_type": file_type,
                    "files_found": len(results["found"])
                },
                success=True
            )
            
            return results
            
        except Exception as e:
            self.memory.add_action(
                "find_files_by_type",
                {"directory": directory, "file_type": file_type, "error": str(e)},
                success=False
            )
            results["error"] = str(e)
            return results
    
    # Add this method to your Executor class in agent/execution.py

    def find_file_by_name(self, directory, file_name):
        """Find files that match a full or partial name"""
        results = {"found": [], "error": None}
        
        try:
            all_files = []
            
            # Walk through directory including subdirectories
            for root, _, files in os.walk(directory):
                for file in files:
                    if file_name.lower() in file.lower():
                        file_path = os.path.join(root, file)
                        results["found"].append(file_path)
            
            # Log the action
            self.memory.add_action(
                "find_file_by_name",
                {
                    "directory": directory,
                    "file_name": file_name,
                    "files_found": len(results["found"])
                },
                success=True
            )
            
            return results
            
        except Exception as e:
            self.memory.add_action(
                "find_file_by_name",
                {"directory": directory, "file_name": file_name, "error": str(e)},
                success=False
            )
            results["error"] = str(e)
            return results