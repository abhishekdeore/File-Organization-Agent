# File Organization Agent

An intelligent file management assistant that helps organize and locate files using natural language commands. This agent understands simple English requests and executes file operations automatically, making file management tasks more intuitive.

## 📋 Features

- **Natural Language Understanding**: Process requests like "organize downloads by file type" or "find PDFs in documents"
- **File Organization**: 
  - Group files by type (extension)
  - Sort files by date (creation or modification)
- **File Search**:
  - Find files by type (pdf, jpg, etc.)
  - Locate files by name or partial name
- **Multi-platform**: Works on Windows, macOS, and Linux
- **Dual Interfaces**:
  - Command-line interface for quick access
  - Streamlit web application for visual interaction
- **Memory System**: Remembers previous actions and directories

## 🛠️ Technology Stack

- **Python**: Core programming language
- **Google Gemini AI**: Natural language understanding (using Gemini 2.0 Flash model)
- **Streamlit**: Web application framework
- **Pathlib & OS modules**: File system operations

## 🏗️ Architecture

The agent follows a modular design with distinct components:

1. **Understanding Module**: Translates natural language to structured commands using Google's Gemini API
2. **Planning Module**: Converts understood commands into executable plans
3. **Execution Module**: Performs actual file system operations safely
4. **Memory Module**: Maintains context between sessions and tracks user preferences

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/file-organization-agent.git
   cd file-organization-agent
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   DEFAULT_WORKSPACE=your/preferred/directory/path
   ```

### Running the Application

#### Web Interface (Recommended)
```bash
streamlit run app.py
```

#### Command Line Interface
```bash
python main.py
```

#### Configuration UI
```bash
streamlit run setup_ui.py
```

## 📝 Usage Examples

- "Organize my downloads folder by file type"
- "Find all PDF files in my documents"
- "Sort my desktop by date modified"
- "Find files named 'report' in my downloads"

## ⚙️ Configuration

You can configure the agent through:
- The setup UI (`streamlit run setup_ui.py`)
- Directly editing the `.env` file
- Using the settings panel in the Streamlit web app

## 🧩 Project Structure

```
file_organization_agent/
├── agent/
│   ├── __init__.py
│   ├── understanding.py  # Natural language processing
│   ├── planning.py       # Task planning logic
│   ├── execution.py      # File system operations
│   ├── memory.py         # State management
│   └── utils/
│       ├── __init__.py
│       └── file_helpers.py  # File utility functions
├── app.py                # Streamlit web interface
├── config.py             # Configuration management
├── main.py               # Command-line interface
├── run.py                # Application launcher
├── setup.py              # CLI setup utility
├── setup_ui.py           # Web-based setup utility
├── requirements.txt      # Package dependencies
├── .env                  # Environment variables (not in repo)
└── README.md             # Project documentation
```

## 🔒 Security Notes

- API keys are stored locally in the `.env` file and are not shared with the repository
- The agent only operates on files in the specified directories
- No data is sent to external servers except the text of your commands to the Gemini API

## ⚠️ Current Limitations

1. **Limited File Operations**: Currently only supports organization and finding operations, not moving files between different drives, renaming, or deletion
2. **No Undo Functionality**: Actions performed are permanent and cannot be automatically undone
3. **AI Understanding Limits**: While it understands common phrases, very complex or ambiguous requests may be misinterpreted
4. **Performance with Large Directories**: May slow down when processing directories with thousands of files
5. **API Dependency**: Requires internet connection and valid API key for the natural language understanding component
6. **Basic Error Handling**: Some edge cases in file operations may not be handled gracefully
7. **Limited Memory**: Cannot recall complex patterns of user behavior over long periods
8. **Single Language Support**: Currently optimized for English requests only

## 🔮 Future Enhancements

- Add file operation undo functionality
- Implement batch operations across multiple directories
- Add file content searching capabilities
- Create user-defined organization rules
- Improve error handling and recovery
- Add scheduling for automatic organization
- Enhance memory systems for better personalization

## 📜 License

This project is available under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Google for providing the Gemini API
- Streamlit for the web application framework
- All contributors to the Python libraries used in this project

## 📫 Contact

For questions, issues, or contributions, please open an issue on this GitHub repository.
