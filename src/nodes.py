import os
import snowflake.connector
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from .schema import AuditState, FinancialAuditReport

load_dotenv()

def generate_sql_node(state: AuditState) -> dict:
    """Evaluates the prompt and metadata to generate safe, contextual SQL."""
    # Using low temperature for deterministic SQL generation
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    schema_context = """
    Target Database: SNOWFLAKE (TRANS_DB.PUBLIC)
    Table: TRANSACTIONS
    Columns: 
      - TXN_ID (VARCHAR)
      - ACCOUNT_ID (VARCHAR)
      - AMOUNT (NUMBER)
      - TXN_DATE (DATE)
      - MERCHANT_CATEGORY (VARCHAR)
    """
    
    # If a previous run failed, inject the error log so the LLM fixes its mistake
    feedback_loop = ""
    if state.get("error_log"):
        feedback_loop = f"\nYour previous query failed with this error: {state['error_log']}. Please correct the syntax."

    prompt = f"""
    You are an expert Data Engineer and Financial Auditor. 
    Based on the schema below, write a read-only SQL query to answer the user's request.
    Do not invent columns. Return ONLY the raw SQL query without markdown formatting, backticks, or explanations.{feedback_loop}
    
    Schema: {schema_context}
    User Request: {state['user_prompt']}
    """
    
    response = llm.invoke(prompt)
    return {"generated_sql": response.content.strip(), "error_log": None}


def execute_query_node(state: AuditState) -> dict:
    """Executes generated SQL against Snowflake with explicit data engineering guardrails."""
    sql = state["generated_sql"]
    
    # Data Engineering Guardrail: Prevent destructive Data Modification Language (DML)
    forbidden_keywords = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "ALTER", "GRANT"]
    if any(kw in sql.upper() for kw in forbidden_keywords):
        return {"error_log": "Security Violation: Unauthorized DML/DDL operations detected."}
    
    try:
        ctx = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        cs = ctx.cursor()
        cs.execute(sql)
        results = cs.fetchall()
        cs.close()
        ctx.close()
        
        return {"query_results": results, "error_log": None}
        
    except Exception as e:
        # Pass the database stack trace back to the state graph for self-healing
        return {"error_log": f"Database Execution Failure: {str(e)}"}


def analyze_results_node(state: AuditState) -> dict:
    """Synthesizes raw database payloads into structured, compliant JSON objects."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    structured_llm = llm.with_structured_output(FinancialAuditReport)
    
    prompt = f"""
    Analyze the raw database results matching the user query. Format your response exactly to the schema constraints.
    
    User Request: {state['user_prompt']}
    SQL Executed: {state['generated_sql']}
    Raw Data Payload: {state['query_results']}
    """
    
    report = structured_llm.invoke(prompt)
    return {"final_report": report}
