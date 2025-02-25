import os
import json
import re
import google.generativeai as genai
from config import GOOGLE_API_KEY

class Understanding:
    def __init__(self, memory):
        self.memory = memory
        # Configure the Gemini API
        genai.configure(api_key=GOOGLE_API_KEY)
        
    def parse_request(self, user_input):
        """Parse user input into intent and parameters using Google's Gemini API"""
        # Get recent actions to provide context
        recent_actions = self.memory.get_recent_actions(3)
        recent_context = ""
        
        if recent_actions:
            recent_context = "Recent actions:"
            for action in recent_actions:
                recent_context += f"\n- {action['type']}: {json.dumps(action['details'])}"
        
        # Create prompt for the LLM
        system_prompt = """
        You are an AI assistant that helps with file organization tasks.
        Your job is to analyze the user's request and extract the intent and parameters.
        
        Valid intents are:
        1. organize_by_type - Organize files by their file extension
        2. organize_by_date - Organize files by their creation or modification date
        3. find_files_by_type - Find files of a specific type
        4. find_file_by_name - Find a specific file by name or partial name
        5. unknown - If you can't determine the intent
        
        Parameters to extract:
        - directory: The directory to operate on (can be "downloads", "desktop", "documents", or a specific path)
        - file_type: For find_files_by_type, the type of file to find (pdf, jpg, txt, etc.)
        - use_modified: For organize_by_date, whether to use modification date (true) or creation date (false)
        - file_name: For find_file_by_name, the name or partial name to search for
        
        Respond with a JSON object containing intent and parameters. ONLY respond with the JSON.
        Example response: {"intent": "find_files_by_type", "parameters": {"directory": "downloads", "file_type": "pdf"}}
        """
        
        user_message = f"""
        User request: {user_input}
        
        {recent_context}
        
        Parse this request into intent and parameters.
        """
        
        try:
            # Set up the model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Create a chat session
            chat = model.start_chat(history=[
                {"role": "user", "parts": [system_prompt]},
                {"role": "model", "parts": ["I understand. I'll extract the intent and parameters from user requests and respond with a JSON object."]}
            ])
            
            # Get response from the model
            response = chat.send_message(user_message)
            content = response.text
            
            # Find JSON in the response
            json_match = re.search(r'({[\s\S]*})', content)
            
            if json_match:
                try:
                    parsed_json = json.loads(json_match.group(1))
                    # Validate the response
                    if "intent" in parsed_json and "parameters" in parsed_json:
                        return parsed_json
                except json.JSONDecodeError:
                    # Fallback to default parsing if JSON is invalid
                    pass
            
            # Default fallback intent if LLM fails
            return {
                "intent": "unknown",
                "parameters": {}
            }
            
        except Exception as e:
            print(f"Error using Gemini API: {str(e)}")
            # Fallback to a simple rule-based parsing as a backup
            return self._fallback_parse(user_input)
    
    def _fallback_parse(self, user_input):
        """Simple rule-based parsing as fallback"""
        user_input = user_input.lower()
        
        if "organize" in user_input or "sort" in user_input:
            if "type" in user_input:
                return {"intent": "organize_by_type", "parameters": {"directory": "downloads"}}
            elif "date" in user_input:
                return {"intent": "organize_by_date", "parameters": {"directory": "downloads", "use_modified": True}}
        
        elif "find" in user_input:
            if "pdf" in user_input:
                return {"intent": "find_files_by_type", "parameters": {"directory": "downloads", "file_type": "pdf"}}
            
            # Check for specific file name search
            words = user_input.split()
            for word in words:
                if "." in word:
                    return {"intent": "find_file_by_name", "parameters": {"directory": "downloads", "file_name": word}}
        
        return {"intent": "unknown", "parameters": {}}