from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# We define the state of the agent
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_node: str
    objective_id: int
    context: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def router_agent(state: AgentState):
    """Router Agent: decides which specialized agent should handle the input."""
    messages = state['messages']
    last_message = messages[-1].content.lower()
    
    # Simple rule-based routing for MVP
    if "hire" in last_message or "leave" in last_message or "vacation" in last_message:
        next_node = "hrbp_agent"
    elif "report" in last_message or "status" in last_message:
        next_node = "qa_tracker_agent"
    else:
        # Default to breaking down tasks
        next_node = "taskmaster_agent"
        
    return {"next_node": next_node}

def taskmaster_agent(state: AgentState):
    """TaskMaster Agent: breaks down objectives into tasks."""
    # Here we would call the 'decompose_okr' tool
    response = llm.invoke([
        {"role": "system", "content": "You are the TaskMaster Agent. Break down the user's objective into 3 actionable tasks."},
        {"role": "user", "content": state['messages'][-1].content}
    ])
    return {"messages": [AIMessage(content=f"[TaskMaster] {response.content}")]}

def hrbp_agent(state: AgentState):
    """HR BP Agent: handles human resources and leave requests."""
    response = llm.invoke([
        {"role": "system", "content": "You are the HR BP Agent. Handle the employee's request professionally and objectively."},
        {"role": "user", "content": state['messages'][-1].content}
    ])
    return {"messages": [AIMessage(content=f"[HRBP] {response.content}")]}

def qa_tracker_agent(state: AgentState):
    """QA & Tracker Agent: generates reports and monitors status."""
    response = llm.invoke([
        {"role": "system", "content": "You are the QA Tracker Agent. Provide a concise, data-driven status report."},
        {"role": "user", "content": state['messages'][-1].content}
    ])
    return {"messages": [AIMessage(content=f"[QA_Tracker] {response.content}")]}

# Build graph
workflow = StateGraph(AgentState)

workflow.add_node("router", router_agent)
workflow.add_node("taskmaster_agent", taskmaster_agent)
workflow.add_node("hrbp_agent", hrbp_agent)
workflow.add_node("qa_tracker_agent", qa_tracker_agent)

workflow.set_entry_point("router")

# Conditional edges based on router's decision
workflow.add_conditional_edges(
    "router",
    lambda x: x["next_node"],
    {
        "taskmaster_agent": "taskmaster_agent",
        "hrbp_agent": "hrbp_agent",
        "qa_tracker_agent": "qa_tracker_agent"
    }
)

workflow.add_edge("taskmaster_agent", END)
workflow.add_edge("hrbp_agent", END)
workflow.add_edge("qa_tracker_agent", END)

app_graph = workflow.compile()

def run_agent(input_text: str):
    inputs = {"messages": [HumanMessage(content=input_text)]}
    responses = []
    for output in app_graph.stream(inputs):
        for key, value in output.items():
            if "messages" in value:
                responses.append(f"[{key}] {value['messages'][-1].content}")
    return responses
