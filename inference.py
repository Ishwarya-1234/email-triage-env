import os
from openai import OpenAI
from tasks import TASKS
from environment import EmailTriageEnv

API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

env = EmailTriageEnv()

def get_agent_action(state):
    prompt = f"""You are an expert email triage agent for a tech company support system.

Analyze this email and classify it:

Email ID: {state.email_id}
From: {state.sender}
Time: {state.timestamp}
Subject: {state.email_subject}
Body: {state.email_body}

Rules:
- Priority "urgent": production issues, security vulnerabilities, data loss, system down
- Priority "normal": billing questions, account issues, how-to questions
- Priority "low": general feedback, vague follow-ups, non-critical inquiries

- Category "bug_report": crashes, errors, broken features
- Category "billing": invoices, refunds, pricing, payments
- Category "feature_request": new features, API questions, future plans
- Category "complaint": dissatisfaction, negative feedback
- Category "general": everything else

Respond ONLY in this exact format, nothing else:
priority: urgent/normal/low
category: bug_report/billing/feature_request/complaint/general"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.1
    )

    text = response.choices[0].message.content.strip()
    lines = text.split("\n")

    action = {}
    for line in lines:
        if "priority:" in line:
            action["priority"] = line.split(":")[1].strip()
        if "category:" in line:
            action["category"] = line.split(":")[1].strip()

    return action

print("[START]")

total_reward = 0
levels = ["easy", "medium", "hard"]

for level in levels:
    state = env.reset(level)
    action = get_agent_action(state)
    _, reward, _, _ = env.step(action)
    total_reward += reward

    print(f"[STEP] task_level={level} email_id={state.email_id} action={action} reward={reward}")

avg_reward = total_reward / len(levels)
print(f"[END] avg_reward={avg_reward}")