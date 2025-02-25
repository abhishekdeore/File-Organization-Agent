from config import DEFAULT_WORKSPACE
import os

class Planner:
    def __init__(self, memory):
        self.memory = memory
        
    def create_plan(self, parsed_request):
        """Create execution plan from parsed request"""
        intent = parsed_request["intent"]
        parameters = parsed_request["parameters"]
        
        # Resolve directory path
        directory = self._resolve_directory(parameters.get("directory", DEFAULT_WORKSPACE))
        
        if intent == "organize_by_type":
            return {
                "action": "organize_by_type",
                "directory": directory,
                "description": f"Organizing files in {directory} by file type"
            }
            
        elif intent == "organize_by_date":
            use_modified = parameters.get("use_modified", True)
            date_type = "modification" if use_modified else "creation"
            return {
                "action": "organize_by_date",
                "directory": directory,
                "use_modified": use_modified,
                "description": f"Organizing files in {directory} by {date_type} date"
            }
            
        elif intent == "find_files_by_type":
            file_type = parameters.get("file_type", "")
            return {
                "action": "find_files_by_type",
                "directory": directory,
                "file_type": file_type,
                "description": f"Finding {file_type} files in {directory}"
            }

        elif intent == "find_file_by_name":
            file_name = parameters.get("file_name", "")
            return {
                "action": "find_file_by_name",
                "directory": directory,
                "file_name": file_name,
                "description": f"Finding files matching '{file_name}' in {directory}"
            }
            
        else:
            return {
                "action": "unknown",
                "description": "Sorry, I don't understand what you want me to do."
            }
        


            
    def _resolve_directory(self, directory_name):
        """Resolve directory name to absolute path"""
        # Handle special names
        if directory_name.lower() in ["downloads", "download"]:
            from pathlib import Path
            return os.path.join(Path.home(), "Downloads")
            
        elif directory_name.lower() in ["desktop"]:
            from pathlib import Path
            return os.path.join(Path.home(), "Desktop")
            
        elif directory_name.lower() in ["documents", "docs"]:
            from pathlib import Path
            return os.path.join(Path.home(), "Documents")
            
        # Handle relative paths
        if not os.path.isabs(directory_name):
            return os.path.abspath(directory_name)
            
        return directory_name