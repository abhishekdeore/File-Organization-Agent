import os
from agent.memory import Memory
from agent.understanding import Understanding
from agent.planning import Planner
from agent.execution import Executor
from config import DEFAULT_WORKSPACE

def print_welcome():
    print("=" * 60)
    print("  File Organization Agent - Your Personal File Assistant")
    print("=" * 60)
    print("You can ask me to:")
    print("  - Organize files by type: 'organize my downloads by file type'")
    print("  - Organize files by date: 'sort my desktop by date modified'")
    print("  - Find files: 'find all PDFs in my documents folder'")
    print("\nType 'exit' to quit.")
    print("=" * 60)

def format_response(result, plan):
    """Format execution results into user-friendly message"""
    if plan["action"] == "organize_by_type":
        return (f"I organized {len(result['moved'])} files in {plan['directory']} by type.\n"
                f"Created folders: {', '.join(set([item['type'] for item in result['moved']]))}")
                
    elif plan["action"] == "organize_by_date":
        return (f"I organized {len(result['moved'])} files in {plan['directory']} by date.\n"
                f"Created date categories: {', '.join(set([item['date_category'] for item in result['moved']]))}")
                
    elif plan["action"] == "find_files_by_type":
        if result["error"]:
            return f"Error while searching: {result['error']}"
        elif len(result["found"]) == 0:
            return f"I couldn't find any {plan['file_type']} files in {plan['directory']}."
        else:
            files_list = "\n  - ".join([os.path.basename(f) for f in result["found"]])
            return f"I found {len(result['found'])} {plan['file_type']} files in {plan['directory']}:\n  - {files_list}"

    elif plan["action"] == "find_file_by_name":
        if result["error"]:
            return f"Error while searching: {result['error']}"
        elif len(result["found"]) == 0:
            return f"I couldn't find any files matching '{plan['file_name']}' in {plan['directory']}."
        else:
            files_list = "\n  - ".join([f"{os.path.basename(f)} (in {os.path.dirname(f)})" for f in result["found"]])
            return f"I found {len(result['found'])} files matching '{plan['file_name']}':\n  - {files_list}"

# Update the main function in main.py to remove the confirmation step

def main():
    memory = Memory()
    understanding = Understanding(memory)
    planner = Planner(memory)
    executor = Executor(memory)
    
    print_welcome()
    
    while True:
        try:
            user_input = input("\nWhat would you like me to do? > ")
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Thank you for using File Organization Agent! Goodbye.")
                break
                
            # Parse user request
            parsed_request = understanding.parse_request(user_input)
            
            # Create plan
            plan = planner.create_plan(parsed_request)
            
            if plan["action"] == "unknown":
                print(plan["description"])
                continue
                
            # Execute plan immediately without confirmation
            print(f"Executing: {plan['description']}...")
            
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
                
            # Print results
            print(format_response(result, plan))
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            
if __name__ == "__main__":
    main()