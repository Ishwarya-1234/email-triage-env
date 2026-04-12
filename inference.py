import os
from openai import OpenAI
from environment import EmailTriageEnv

# =========================
# Environment Variables
# =========================
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

env = EmailTriageEnv()

# =========================
# Agent Logic
# =========================
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

    action = {"priority": "normal", "category": "general"}

    for line in text.split("\n"):
        if "priority:" in line:
            action["priority"] = line.split(":")[1].strip()
        elif "category:" in line:
            action["category"] = line.split(":")[1].strip()

    return action

# =========================
# Main Execution Loop
# =========================
levels = ["easy", "medium", "hard"]

for level in levels:
    state = env.reset(level)
    task_name = f"email_triage_{level}"

    print(f"[START] task={task_name} env=email-triage-env model={MODEL_NAME}")

    step = 0
    rewards = []
    done = False

    try:
        while not done:
            step += 1

            action = get_agent_action(state)

            state, reward, done, _ = env.step(action)

            # ✅ Clamp reward between 0 and 1
            reward = max(0.0, min(1.0, reward))
            reward_str = f"{reward:.2f}"
            rewards.append(reward_str)

            # ✅ Safe action string (no spaces/newlines issues)
            action_str = f"priority={action.get('priority','unknown')},category={action.get('category','unknown')}"

            print(
                f"[STEP] step={step} action={action_str} "
                f"reward={reward_str} done={str(done).lower()} error=null"
            )

        # ✅ Close environment BEFORE END
        env.close()

        print(
            f"[END] success=true steps={step} rewards={','.join(rewards)}"
        )

    except Exception as e:
        error_msg = str(e).replace("\n", " ").replace("\r", " ")

        print(
            f"[STEP] step={step+1} action=null reward=0.00 done=false error={error_msg}"
        )

        print(
            f"[END] success=false steps={step+1} rewards={','.join(rewards) if rewards else '0.00'}"
        )
