from langchain_core.tools import tool
import random

# A registry to hold all our skills
SKILL_REGISTRY = []

def register_skill(func):
    """Decorator to register a tool in our centralized Middle-Manager skill registry."""
    t = tool(func)
    SKILL_REGISTRY.append(t)
    return t

# ==========================================
# 1. 战略与分发类 (Strategy & Dispatch) - 20 Tools
# ==========================================
@register_skill
def decompose_okr(okr_text: str) -> str:
    """Decomposes a top-level CEO OKR into atomic tasks."""
    return f"Decomposed '{okr_text}' into 5 atomic tasks."

@register_skill
def auto_assign_task(task_id: str, team_members: list) -> str:
    """Automatically assigns a task to the best fit employee based on past performance."""
    best_fit = random.choice(team_members) if team_members else "Employee_X"
    return f"Assigned task {task_id} to {best_fit} based on velocity metrics."

@register_skill
def estimate_velocity(task_desc: str) -> str:
    """Estimates the completion time for a task based on historical data."""
    return "Estimated time: 3 days with 85% confidence."

# (Generating remaining 17 mock tools for Category 1...)
for i in range(4, 21):
    def make_strategy_tool(index):
        @register_skill
        def strategy_tool(input_data: str) -> str:
            f"""Strategy tool {index} for advanced planning."""
            return f"Strategy Tool {index} executed on {input_data}"
        strategy_tool.__name__ = f"strategy_tool_{index}"
        return strategy_tool
    make_strategy_tool(i)

# ==========================================
# 2. 进度与风控类 (Progress & Risk Control) - 20 Tools
# ==========================================
@register_skill
def detect_blocker(project_id: str) -> str:
    """Scans the project for cross-department blockers."""
    return f"No major blockers detected for project {project_id}. 1 minor API delay."

@register_skill
def generate_auto_standup(team_id: str) -> str:
    """Generates an automatic daily standup report without a meeting."""
    return f"Auto-standup generated for team {team_id}: 3 PRs merged, 0 blockers."

@register_skill
def alert_scope_creep(repo_url: str) -> str:
    """Monitors commits and PRs to detect scope creep."""
    return "Scope creep alert: Feature X was added but not in original OKR."

for i in range(24, 41):
    def make_progress_tool(index):
        @register_skill
        def progress_tool(input_data: str) -> str:
            f"""Progress and Risk Tool {index}."""
            return f"Progress Tool {index} executed."
        progress_tool.__name__ = f"progress_tool_{index}"
        return progress_tool
    make_progress_tool(i)

# ==========================================
# 3. 人力与绩效类 (HR & Performance) - 20 Tools
# ==========================================
@register_skill
def calculate_objective_score(employee_id: str) -> str:
    """Calculates a 100% objective performance score based on Git/Jira data."""
    return f"Employee {employee_id} score: 92/100 (Top 5%)."

@register_skill
def generate_pip(employee_id: str, weak_points: list) -> str:
    """Generates an objective 30-day Performance Improvement Plan."""
    return f"30-day PIP generated for {employee_id} focusing on {weak_points}."

@register_skill
def predict_flight_risk(employee_id: str) -> str:
    """Predicts if a core employee is likely to leave in the next 30 days."""
    return f"Flight risk for {employee_id}: LOW (12%)."

@register_skill
def process_leave_request(employee_id: str, dates: str) -> str:
    """Auto-approves leave and redistributes tasks."""
    return f"Leave approved for {employee_id} on {dates}. Tasks redistributed."

for i in range(45, 61):
    def make_hr_tool(index):
        @register_skill
        def hr_tool(input_data: str) -> str:
            f"""HR and Performance Tool {index}."""
            return f"HR Tool {index} executed."
        hr_tool.__name__ = f"hr_tool_{index}"
        return hr_tool
    make_hr_tool(i)

# ==========================================
# 4. 办公与秘书类 (Office & Secretary) - 20 Tools
# ==========================================
@register_skill
def draft_company_announcement(topic: str) -> str:
    """Drafts a company-wide announcement with perfect tone."""
    return f"Announcement drafted for topic: {topic}"

@register_skill
def schedule_meeting(participants: list, agenda: str) -> str:
    """Finds a common time and schedules a meeting for participants."""
    return f"Meeting scheduled for {participants} regarding {agenda} at 2:00 PM."

for i in range(63, 81):
    def make_office_tool(index):
        @register_skill
        def office_tool(input_data: str) -> str:
            f"""Office and Secretary Tool {index}."""
            return f"Office Tool {index} executed."
        office_tool.__name__ = f"office_tool_{index}"
        return office_tool
    make_office_tool(i)

# ==========================================
# 5. 外部系统与 MCP 扩展类 (External & MCP) - 20 Tools
# ==========================================
@register_skill
def call_mcp_server(server_name: str, tool_name: str, params: dict) -> str:
    """Dynamically calls an external MCP server tool."""
    return f"MCP server '{server_name}' executed '{tool_name}' with {params}."

@register_skill
def fetch_github_prs(repo: str) -> str:
    """Fetches latest Pull Requests from GitHub."""
    return f"Fetched 5 open PRs from {repo}."

for i in range(83, 101):
    def make_ext_tool(index):
        @register_skill
        def ext_tool(input_data: str) -> str:
            f"""External System Integration Tool {index}."""
            return f"Ext Tool {index} executed."
        ext_tool.__name__ = f"ext_tool_{index}"
        return ext_tool
    make_ext_tool(i)

def get_all_skills():
    return SKILL_REGISTRY
