# Study Assistant — Multi-Agent System using LangChain & LangGraph

Design and implementation of a multi-agent system using LangChain, LangGraph, and Qwen3-32B model via LiteLLM/vLLM.

## Project Overview

StudyCoder Assistant is an intelligent educational assistant designed for programming students.  
The system consists of **5 specialized agents** working together:

- **Router Agent** — classifies user queries into categories (theory, code, planning, general)
- **Theory Agent** — explains theoretical concepts (algorithms, data structures, machine learning)
- **Code Agent** — writes, comments, and tests Python code
- **Planner Agent** — creates personalized study plans
- **General Agent** — handles general questions and provides information about the system

The system implements the **Router + Specialized Agents** pattern using **LangGraph** for stateful workflow management.  
It includes session memory, 3 custom tools with tool calling, and detailed execution logging.

## Technologies

- Python 3.10+
- LangChain 1.x
- LangGraph 1.x
- LiteLLM (local server with Qwen3-32B via vLLM)
- Pydantic, python-dotenv

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/studycoder-assistant.git
cd studycoder-assistant
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

## Usage
### Option 1: Full project demonstration (tests + interactive mode)
```
python src/main.py
```
This will:
- Verify connection to the LLM
- Run 6 predefined test queries
- Display statistics and classification accuracy
- Launch interactive mode

### Option 2: Interactive mode only
```
python run_demo.py
```

Available commands in chat:
- stats / statistics — show session statistics
- history / hist — show recent interactions
- info / system — show system information
- exit / quit — exit

## Project Structure
```
mullti-agent-study-assistant/
├── src/                    # Core source code
│   ├── config.py           # LLM configuration
│   ├── tools.py            # Custom tools (code execution, knowledge search, study planner)
│   ├── memory.py           # Session memory management
│   ├── agents.py           # Multi-agent system and LangGraph workflow
│   ├── utils.py            # Interactive demo utilities
│   └── main.py             # Full lab execution and testing
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md     # Architecture description + Mermaid diagram
├── requirements.txt        # Python dependencies
└── task4_reflection        # Detailes analysis of the project
├── run_demo.py             # Quick interactive demo entry point
└── README.md               # This file
```

## Features
- Conditional routing via LangGraph
- Tool calling with 3 custom tools
- Session memory with context-aware responses
- Detailed logging and execution statistics
- Clean and modular code structure
