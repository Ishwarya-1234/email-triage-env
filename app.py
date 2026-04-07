import uvicorn
from fastapi import FastAPI
from environment import EmailTriageEnv
from tasks import TASKS, run_task

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
    return {"state": state, "reward": reward, "done": done}

@app.get("/tasks")
def get_tasks():
    return TASKS

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()