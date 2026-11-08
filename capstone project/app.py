import time
import json
import uuid
import logging
from typing import Dict
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from crew_agents import apply_input_guardrails
from dataset import check_loan_application_status
from rag_core import grounded_rag_lookup

app = FastAPI(title="Cred Domain Support Agent API")

logger = logging.getLogger("cred_structured_logger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

RESPONSE_CACHE: Dict[str, dict] = {}
CACHE_STATS = {"hits": 0, "misses": 0}

class QueryRequest(BaseModel):
    query: str = Field(..., example="What are the KYC document requirements?")
    record_id: str = Field(..., example="CRED-LN-1005")

class QueryResponse(BaseModel):
    trace_id: str
    policy_response: str
    record_status: str
    escalation_required: bool
    execution_time_ms: float
    cached: bool

@app.post("/ask", response_model=QueryResponse)
async def ask_agent(request: QueryRequest):
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    
    if len(request.query) > 500:
        raise HTTPException(status_code=400, detail="Cost Budget Exceeded: Request size is too large.")

    try:
        masked_query = apply_input_guardrails(request.query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    cache_key = f"{masked_query.strip().lower()}_{request.record_id}"
    if cache_key in RESPONSE_CACHE:
        CACHE_STATS["hits"] += 1
        cached_result = RESPONSE_CACHE[cache_key]
        execution_time = (time.time() - start_time) * 1000
        return QueryResponse(
            trace_id=trace_id,
            policy_response=cached_result["policy_response"],
            record_status=cached_result["record_status"],
            escalation_required=cached_result["escalation_required"],
            execution_time_ms=round(execution_time, 2),
            cached=True
        )

    CACHE_STATS["misses"] += 1

    # Fetch the precise dynamic policy matching the user query from rag_core
    rag_check = grounded_rag_lookup(masked_query)
    
    # Securely query account registers for status and escalation metrics from dataset.py
    status_data = check_loan_application_status(request.record_id)
    record_status_str = status_data.get("status", "Unknown")
    escalation_flag = status_data.get("recommend_escalation", False)

    # Directly pass the cleanly formatted structured fields to the API layer
    result_data = {
        "policy_response": rag_check,
        "record_status": record_status_str,
        "escalation_required": escalation_flag
    }

    RESPONSE_CACHE[cache_key] = result_data
    execution_time = (time.time() - start_time) * 1000

    log_entry = {
        "trace_id": trace_id,
        "timestamp": time.time(),
        "masked_query": masked_query,
        "record_id": request.record_id,
        "cache": "MISS",
        "execution_time_ms": round(execution_time, 2)
    }
    logger.info(json.dumps(log_entry))

    return QueryResponse(
        trace_id=trace_id,
        policy_response=result_data["policy_response"],
        record_status=result_data["record_status"],
        escalation_required=result_data["escalation_required"],
        execution_time_ms=round(execution_time, 2),
        cached=False
    )

@app.websocket("/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    trace_id = str(uuid.uuid4())
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            user_query = payload.get("query", "")
            record_id = payload.get("record_id", "CRED-LN-1005")
            try:
                masked_query = apply_input_guardrails(user_query)
                status_data = check_loan_application_status(record_id)
                response_payload = {
                    "trace_id": trace_id,
                    "policy_response": f"Processed multi-turn session turn for query: {masked_query}",
                    "record_status": status_data.get("status", "Unknown"),
                    "escalation_required": status_data.get("recommend_escalation", False)
                }
            except Exception as inner_err:
                response_payload = {"error": str(inner_err)}
            await websocket.send_text(json.dumps(response_payload))
    except WebSocketDisconnect:
        logger.info(json.dumps({"event": "WebSocket client disconnected", "trace_id": trace_id}))
