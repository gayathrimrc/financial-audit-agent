from typing import TypedDict, Optional, List
from pydantic import BaseModel, Field

class FinancialAuditReport(BaseModel):
    """Structured schema for the final audit response."""
    summary: str = Field(description="High-level business summary of the analytical findings.")
    anomalies_found: bool = Field(description="Set to True if data deviates significantly from normal thresholds.")
    sql_queries_used: List[str] = Field(description="The exact read-only SQL executed for the audit trail.")
    recommended_action: str = Field(description="Recommended compliance or mitigation steps for the risk team.")

class AuditState(TypedDict):
    """Maintains state transitions across the LangGraph workflow."""
    user_prompt: str
    generated_sql: Optional[str]
    query_results: Optional[List]
    error_log: Optional[str]
    final_report: Optional[FinancialAuditReport]
