# 🌍 Multi-Agent AI Travel Planner

A Python-based CLI application that uses a team of specialized AI agents to plan your dream vacation. Built with **LangGraph**, **LangChain**, and **Ollama**, this system runs entirely locally, meaning it's 100% free and private!

## ✨ Features
* **100% Local & Free:** Powered by Ollama using the incredibly lightweight and fast `qwen2.5:0.5b` model. No API keys required, and your data never leaves your machine.
* **Multi-Agent Orchestration:** Uses LangGraph to orchestrate a team of three distinct AI agents:
  1. ✈️ **Destination Expert:** Analyzes your travel request and suggests the top 3 spots.
  2. 📅 **Itinerary Planner:** Takes those spots and builds a cohesive day-by-day schedule.
  3. 💰 **Budget Analyzer:** Reviews the itinerary, estimates a rough cost, and provides practical travel tips.
* **State Management:** Seamlessly passes context between agents using a shared LangGraph State.

## 🛠️ Prerequisites
* **Python 3.8+**
* **Ollama** installed on your machine. ([Download Ollama](https://ollama.com/download))

## 🚀 Setup Instructions

1. **Clone/Navigate to the project directory**
   ```bash
   cd path/to/your/project
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install langgraph langchain-core langchain-community python-dotenv pydantic
   ```
   *(Note: The `langchain-ollama` package is recommended for newer versions of LangChain).*

4. **Pull the Local LLM**
   Make sure the Ollama application is running, then open your terminal and pull the lightweight model used by the script:
   ```bash
   ollama pull qwen2.5:0.5b
   ```

## 💻 Usage

Run the script from your terminal:
```bash
python multi_agent_system.py
```

When prompted, type out your dream trip! For example:
> `A 10 day trip in south of france`

Sit back and watch as the three agents collaborate in real-time to research spots, build your itinerary, and calculate your budget. 

## 🧠 Architecture Overview
The system is built using a linear **LangGraph Workflow**:
1. **State Definition:** An `AgentState` dictionary acts as a shared clipboard tracking the `user_request`, `destinations`, `itinerary`, and `final_plan`.
2. **Nodes (Agents):** Each agent is a Python function that reads from the state, prompts the local LLM using a specific persona, and returns updates to the state.
3. **Edges:** The graph connects the agents sequentially: `Expert -> Planner -> Analyzer -> END`.

## 🤝 Customization
Want to change the model? It's easy!
1. Pull your desired model via Ollama (e.g., `ollama pull llama3.2`).
2. Open `multi_agent_system.py`.
3. Change the `model` parameter in the `ChatOllama` initialization block to your new model name.
