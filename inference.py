import os
from openai import OpenAI
from environment import EmailTriageEnv

# Environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

env = EmailTriageEnv()

def get_agent_action(state):
    prompt = f"""You are an expert email triage agent.

Analyze this email:
Subject: {state.email_subject}
Body: {state.email_body}
Sender: {state.sender}

Classify it strictly as:
priority: urgent/normal/low
category: bug_report/billing/feature_request/complaint/general

Respond ONLY in this exact format:
priority: <value>
category: <value>"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.1
    )

    text = response.choices[0].message.content.strip()
    action = {}
    for line in text.split("\n"):
        if "priority:" in line:
            action["priority"] = line.split(":")[1].strip()
        if "category:" in line:
            action["category"] = line.split(":")[1].strip()
    return action

levels = ["easy", "medium", "hard"]

for level in levels:
    state = env.reset(level)
    task_name = f"email_triage_{level}"
    
    print(f"[START] task={task_name} env=email-triage-env model={MODEL_NAME}")
    
    try:
        action = get_agent_action(state)
        _, reward, done, _ = env.step(action)
        
        action_str = f"triage(priority='{action.get('priority','unknown')}',category='{action.get('category','unknown')}')"
        
        print(f"[STEP] step=1 action={action_str} reward={reward:.2f} done={str(done).lower()} error=null")
        print(f"[END] success={str(done).lower()} steps=1 rewards={reward:.2f}")
        
    except Exception as e:
        print(f"[STEP] step=1 action=null reward=0.00 done=false error={str(e)}")
        print(f"[END] success=false steps=1 rewards=0.00")