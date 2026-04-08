from fastapi import FastAPI
from environment import EmailTriageEnv
from tasks import TASKS, run_task
from fastapi import Request

app = FastAPI()
env = EmailTriageEnv()

@app.get("/")
def root():
    return {"status": "Email Triage Environment Running"}

@app.post("/reset")
def reset(task_level: str = "easy"):
    state = env.reset(task_level)
    return state

@app.get("/state")
def state():
    return env.get_state()

@app.post("/step")
def step(action: dict):
    state, reward, done, info = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done
    }

@app.get("/tasks")
def get_tasks():
    tasks_with_graders = []
    for t in TASKS:
        tasks_with_graders.append({
            "id": t["id"],
            "level": t["level"],
            "description": t["description"],
            "has_grader": True
        })
    return tasks_with_graders

@app.api_route("/run_task", methods=["GET", "POST"])
async def run_task_endpoint(request: Request, task_id: str = None, action: dict = None):
    from fastapi import Request
    if request.method == "POST":
        body = await request.json()
        task_id = body.get("task_id")
        action = body.get("action", {})
    result = run_task(task_id, action or {})
    return result