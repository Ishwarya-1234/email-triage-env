from environment import EmailTriageEnv

env = EmailTriageEnv()

TASKS = [
    {
        "id": "task_easy_1",
        "level": "easy",
        "description": "Classify an urgent production outage email",
        "categories": ["bug_report", "billing", "general", "feature_request", "complaint"],
        "priorities": ["urgent", "normal", "low"]
    },
    {
        "id": "task_easy_2",
        "level": "easy",
        "description": "Classify a critical app crash report",
        "categories": ["bug_report", "billing", "general", "feature_request", "complaint"],
        "priorities": ["urgent", "normal", "low"]
    },
    {
        "id": "task_medium_1",
        "level": "medium",
        "description": "Classify a billing inquiry email",
        "categories": ["bug_report", "billing", "general", "feature_request", "complaint"],
        "priorities": ["urgent", "normal", "low"]
    },
    {
        "id": "task_medium_2",
        "level": "medium",
        "description": "Classify a refund request email",
        "categories": ["bug_report", "billing", "general", "feature_request", "complaint"],
        "priorities": ["urgent", "normal", "low"]
    },
    {
        "id": "task_hard_1",
        "level": "hard",
        "description": "Classify an ambiguous follow-up email",
        "categories": ["bug_report", "billing", "general", "feature_request", "complaint"],
        "priorities": ["urgent", "normal", "low"]
    },
    {
        "id": "task_hard_2",
        "level": "hard",
        "description": "Classify a vague feedback email",
        "categories": ["bug_report", "billing", "general", "feature_request", "complaint"],
        "priorities": ["urgent", "normal", "low"]
    }
]

def run_task(task_id: str, action: dict):
    # Create fresh env for each task call
    local_env = EmailTriageEnv()
    task = next((t for t in TASKS if t["id"] == task_id), None)
    if not task:
        return {"error": "Task not found"}
    state = local_env.reset(task["level"])
    _, reward, _, _ = local_env.step(action)
    reward = max(0.001, min(reward, 0.999))
    return {
        "task_id": task_id,
        "reward": reward,
        "score": reward,
        "passed": 0.001 < reward < 0.999
    }