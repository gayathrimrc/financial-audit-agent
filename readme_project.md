# Enterprise Multi-Agent Financial Auditor (Text-to-SQL & Self-Healing DAG)

An autonomous multi-agent system built with **LangGraph** and **Pydantic AI** designed to connect securely with enterprise data platforms (Snowflake/Databricks) to perform safe, read-only analytics and financial anomaly auditing.

This project demonstrates how data engineering design patterns (state orchestration, validation, security boundaries) translate directly into production-grade Agentic AI.

## 🛠️ Architecture & Design Patterns

- **Deterministic Orchestration:** Built with LangGraph using a state-machine topology instead of unpredictable linear chains.
- **Self-Healing Data Loops:** If generated SQL errors out at the database warehouse layer, the execution stack trace is safely bubbled back up to the LLM agent to instantly correct its syntax and re-execute.
- **Rigid Security Guardrails:** Includes runtime execution layers that explicitly scan for and isolate destructive SQL dialects (DML/DDL commands like `DROP` or `DELETE`) before passing queries to cloud clusters.
- **Type-Safe Outputs:** Enforces structural integrity of compliance summaries via Pydantic model validation.

## 🗂️ Setup Instructions

1. Clone the repository and initialize a virtual environment:
   ```bash
   git clone [https://github.com/your-username/financial-audit-agent.git](https://github.com/your-username/financial-audit-agent.git)
   cd financial-audit-agent
   python3 -m venv .venv
   source .venv/bin/activate
   
2. Install production dependencies:
   ```bash
   pip install -r requirements.txt

3. Configure your keys:
   ```bash
   cp .env.example .env
   # Open .env and populate your OpenAI and Snowflake account credentials

4. Run the application pipeline:
   ```bash
    python -m src.graph
