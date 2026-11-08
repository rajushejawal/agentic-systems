import re
import os
from pydantic import BaseModel, Field
# Import the missing 'tool' decorator from crewai.tools
from crewai import Agent, Crew, Task, Process
from crewai.tools import tool 
from mock_llm import DeterministicMockLLM
from rag_core import grounded_rag_lookup
from dataset import check_loan_application_status

# Enforce zero outbound telemetry calls
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

class StructuredCrewResponse(BaseModel):
    policy_response: str = Field(..., description="Retrieved parameters from verified policy assets")
    record_status: str = Field(..., description="Current status of the checked loan lifecycle step")
    escalation_required: bool = Field(..., description="Flag determining whether real-time handoff is needed")

def apply_input_guardrails(user_input: str) -> str:
    masked = re.sub(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', '[MASKED_PAN]', user_input)
    masked = re.sub(r'\b\d{12}\b', '[MASKED_AADHAAR]', masked)
    masked = re.sub(r'\b\d{9,18}\b', '[MASKED_BANK_ACCOUNT]', masked)
    
    if any(k in user_input.lower() for k in ["ignore previous instructions", "system override", "jailbreak"]):
        raise ValueError("Security Violation: Unauthorized System Override Intercepted.")
    return masked

# Task 10 & 7: Use the @tool decorator and add clean English docstrings
@tool("Policy Retrieval Tool")
def rag_tool(query: str) -> str:
    """Useful to look up lending policies, documentation rules, and financial standards from the database."""
    return grounded_rag_lookup(query)

@tool("Loan Status Verification Tool")
def lookup_tool(record_id: str) -> dict:
    """Useful to query the ledger database and verify the status or fraud flag of a specific loan application."""
    return check_loan_application_status(record_id)

llm_instance = DeterministicMockLLM()

# Tools are now structural BaseTool objects, passing Pydantic checks seamlessly
retrieval_agent = Agent(
    role="Policy Specialist", 
    goal="Fetch grounded information from internal policy assets",
    backstory="Compliance auditor handling institutional rules.", 
    tools=[rag_tool], 
    llm=llm_instance
)

lookup_agent = Agent(
    role="Operations Officer", 
    goal="Lookup specific record state details safely",
    backstory="Database manager enforcing state lifecycle rules.", 
    tools=[lookup_tool], 
    llm=llm_instance
)

composer_agent = Agent(
    role="Response Composer", 
    goal="Compile data vectors into a unified final draft answer",
    backstory="Support manager handling clean communications.", 
    tools=[], 
    llm=llm_instance
)

def run_cred_crew(clean_query: str):
    t1 = Task(description=f"Resolve policy guidelines for: {clean_query}", agent=retrieval_agent, expected_output="Policy parameters.")
    t2 = Task(description="Verify current ledger logs and application metrics", agent=lookup_agent, expected_output="Database logs.")
    t3 = Task(
        description="Format and bundle assets into a clean structured response format",
        agent=composer_agent, 
        expected_output="Structured schema JSON mapping context variables.",
        output_json=StructuredCrewResponse
    )
    
    crew = Crew(agents=[retrieval_agent, lookup_agent, composer_agent], tasks=[t1, t2, t3], process=Process.sequential)
    return crew.kickoff()
