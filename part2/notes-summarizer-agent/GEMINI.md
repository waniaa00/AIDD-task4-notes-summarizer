


AI Study Assistant: Technical Implementation Guide
Project Summary:
Build an intelligent study tool that transforms PDFs into summaries and generates quizzes using Gemini 2.0 Flash, OpenAI Agents SDK, Streamlit, and Context7 MCP.

Core Capabilities:

Convert PDF documents into structured study notes
Create quiz questions (multiple choice or mixed format) from source material
Lightweight memory system using JSON storage


Technology Stack:

AI Model: Gemini 2.0 Flash via OpenAI-compatible API
Framework: OpenAI Agents SDK
UI: Streamlit
Tools: Context7 MCP Server for SDK documentation
PDF Processing: PyPDF library



Mandatory Requirements:


Simplicity First
Write only essential code. Include nothing beyond:

PDF text extraction
Summary generation
Quiz creation
JSON-based memory
Streamlit interface
Agent setup (Gemini via OpenAI SDK)
Gemini Configuration
Configure OpenAI SDK to use Gemini endpoints:

python:
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
api_key = GEMINI_API_KEY  # from .env file
model = "gemini-2.0-flash"


Required SDK Components:
Import only these from agents:
AsyncOpenAI
Agent
RunConfig
Runner
OpenAIChatCompletionsModel


Troubleshooting Steps:

When errors occur:

Stop execution immediately
Query Context7 MCP: get-library-docs
Fix code using official documentation only
Avoid assumptions or workarounds

Package Installation:
Use uv package manager exclusively:

bash
uv add streamlit pypdf python-dotenv openai-agents
```

---

## Project Structure
```
project-root/
├── agent.py      # Agent configuration and interface
├── app.py        # Streamlit UI and application logic
├── tools.py      # Tool definitions
├── memory.json   # Simple storage
├── .env          # API credentials
└── GEMINI.md     # This documentation
Keep everything in the root directory—no subdirectories.

Agent Configuration (agent.py):
Purpose: Initialize and expose the Gemini-powered agent

Implementation Pattern:

python:
import os
from dotenv import load_dotenv
from agents import Agent, RunConfig, AsyncOpenAI, Runner, OpenAIChatCompletionsModel

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)
Provide a clean run_agent(prompt) function for the UI layer.

Application Logic (app.py):
User Workflow
Step 1: Upload PDF

User uploads document
Extract text using PyPDF
Store temporarily in memory
Optionally log metadata to JSON
Step 2: Generate Summary

User clicks "Generate Summary"
Send to agent: "Summarize the following PDF text: {extracted_text}"
Display result in user-selected layout (card/block/container)
Step 3: Create Quiz

User clicks "Create Quiz"
Send to agent: "Generate a quiz based ONLY on the following full PDF text. Produce MCQs or mixed-style questions: {extracted_text}"
Display generated questions
Forbidden Features
Do NOT implement:

Multi-agent systems
Vector databases or embeddings
Retrieval mechanisms
Text chunking strategies
Response caching
Streaming responses
Complex session management


Context7 MCP Integration:


The MCP server provides:

get-library-docs - Essential for debugging SDK issues
Additional reference tools as available
Register all MCP tools with the agent exactly as exposed. These function as callable methods during agent execution.

Running the Application:

cmd:
streamlit run app.py
Initialization Sequence:

Agent connects to Gemini 2.0 Flash via OpenAI SDK
MCP tools registered
UI becomes available


Runtime Flow:

User uploads PDF → Text extracted
User requests summary → Agent generates response
User requests quiz → Agent creates questions
Results displayed in UI
Memory updates as needed


Development Guidelines:


When writing code:

Keep functions minimal and focused
Follow SDK documentation precisely
Verify unclear syntax using Context7 MCP
Avoid helper classes or abstractions
Write only agent + UI logic 


Testing Checklist:


Validate in this order:

✓ PDF upload and text extraction
✓ Summary generation
✓ Quiz generation
✓ Memory updates
✓ MCP tool availability
✓ Model confirmation (should be gemini-2.0-flash)

Project Completion Standards:

The project is ready when:

✓ Streamlit runs without errors
✓ PDFs upload and extract correctly
✓ Agent generates summaries successfully
✓ Agent creates quizzes from original content
✓ JSON memory functions properly
✓ No code bloat or unnecessary features
✓ All openai-agents imports work
✓ Agent correctly uses Gemini endpoints









