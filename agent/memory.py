import json
import os
from datetime import datetime
from config import MEMORY_FILE

class Memory:
    def __init__(self):
        self.memory_file = MEMORY_FILE
        self.session_actions = []
        self.load_memory()
        
    def load_memory(self):
        """Load existing memory if available"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.long_term_memory = json.load(f)
            except:
                self.long_term_memory = {"actions": [], "preferences": {}}
        else:
            self.long_term_memory = {"actions": [], "preferences": {}}
            
    def save_memory(self):
        """Save memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.long_term_memory, f, indent=2)
            
    def add_action(self, action_type, details, success=True):
        """Record an action taken by the agent"""
        action = {
            "type": action_type,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "success": success
        }
        self.session_actions.append(action)
        self.long_term_memory["actions"].append(action)
        self.save_memory()
        
    def get_recent_actions(self, limit=5):
        """Get most recent actions from memory"""
        return self.session_actions[-limit:] if len(self.session_actions) > 0 else []
        
    def update_preference(self, key, value):
        """Save user preferences"""
        self.long_term_memory["preferences"][key] = value
        self.save_memory()
        
    def get_preference(self, key, default=None):
        """Retrieve user preferences"""
        return self.long_term_memory["preferences"].get(key, default)