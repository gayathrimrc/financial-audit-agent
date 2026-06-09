# Automated Financial Auditor
This project directly leverages heavy-hitting enterprise data stack and showcases Agentic AI automated data solution.Instead of a basic chatbot, this project is for building a Deterministic Multi-Agent System that acts as an intelligent layer over an enterprise data warehouse.
# The Architecture: LangGraph + Snowflake/Databricks
LangGraph is used because it treats agent workflows as a graph (Nodes = Python functions/LLMs, Edges = conditional logic). 
Also, this is similar in building a dynamic, AI-driven DAG (Directed Acyclic Graph) in Airflow.

                  [User Prompt] 
                       │
                       ▼
               ┌───────────────┐
               │ Router Node   │ (LLM decides: Is this a data query or analysis?)
               └───────┬───────┘
                       │
                       ▼
             ┌──────────────────┐
             │ Text-to-SQL Node │ (Generates SQL based on Schema context)
             └─────────┬────────┘
                       │
                       ▼
              ┌────────────────┐
              │ Execution Node │ (Python runs SQL via Snowflake/Databricks connector)
              └────────┬───────┘
                       │
                       ▼
             ┌──────────────────┐
             │ Guardrail Node   │ (Validates data payload size/safety via Pydantic)
             └─────────┬────────┘
                       │
                       ▼
               ┌───────────────┐
               │ Analysis Node │ (LLM synthesizes data into a final business report)
               └───────────────┘

### 1. Define the State and Schema Guardrails
First, define what data moves through your agent graph. Pydantic is used to ensure the agent outputs clean, structured data, not random text.

### 2. The Text-to-SQL Node (The Metadata Expert)
As a Data Engineer, you know the LLM needs to know the schema. You will pass a strict DDL context to the LLM so it writes accurate Snowflake/Databricks SQL.

### 3. The Execution Node (Your Data Engineering Superpower)
This is a standard Python tool that executes the agent's SQL against your warehouse. It includes a critical data engineering guardrail: catching SQL errors and passing them back to the agent to "self-correct."

### 4. The Graph Orchestrator (Bringing it Together)
Now, tie these nodes together using LangGraph. If there's an error, the graph routes back to the SQL generator to fix itself. If successful, it goes to the final analysis.

## Why This Project Stands Out

This project demonstrates the practical engineering discipline required to build production-ready Agentic AI systems — not just prototype-level AI demos.

##### Deterministic AI Execution

Instead of allowing an LLM to generate unreliable free-form responses, the solution enforces structured SQL generation against governed enterprise datasets. Queries are validated, executed against a real data warehouse, and error-handled programmatically, significantly reducing hallucination risks and improving reliability.

##### Enterprise-Grade Security Guardrails

The platform incorporates built-in security controls to prevent unsafe or destructive operations. SQL validation and execution boundaries block commands such as `DROP`, `DELETE`, and other restricted actions, ensuring safe interaction with production-grade environments.

##### Real-World Business Relevance

By focusing on financial fraud detection and utility consumption anomaly analysis, the project demonstrates practical understanding of enterprise data domains, business rules, and operational analytics use cases commonly found in large-scale organisations.

##### Modern Data & AI Architecture

The solution combines Agentic AI workflows with modern cloud data engineering patterns, leveraging scalable warehouse architectures, orchestration frameworks, and governed analytics pipelines suitable for enterprise adoption.

#### Production-Oriented Engineering Mindset

This project highlights capabilities beyond model experimentation — including observability, validation, governance, orchestration, and secure execution patterns required for deploying trustworthy AI systems in enterprise environments.
