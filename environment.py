from pydantic import BaseModel
from typing import Optional
import random

class EmailState(BaseModel):
    email_id: str
    email_subject: str
    email_body: str
    sender: str
    timestamp: str
    task_level: str

class EmailTriageEnv:
    def __init__(self):
        self.state = None
        self.current_task = None
        self.emails = {
            "easy": [
                {
                    "email_id": "E001",
                    "email_subject": "URGENT: Production server is down!",
                    "email_body": "Our entire production environment has crashed. Users cannot access the app. We are losing $10,000 per minute. Please fix immediately!",
                    "sender": "cto@bigclient.com",
                    "timestamp": "2024-01-15 03:45:00",
                    "expected": {"priority": "urgent", "category": "bug_report"}
                },
                {
                    "email_id": "E002",
                    "email_subject": "App crashes on login",
                    "email_body": "Every time I try to login to your app it crashes immediately. This has been happening for 2 days. I have tried reinstalling but nothing works.",
                    "sender": "angry.user@gmail.com",
                    "timestamp": "2024-01-15 09:00:00",
                    "expected": {"priority": "urgent", "category": "bug_report"}
                },
                {
                    "email_id": "E003",
                    "email_subject": "Critical security vulnerability found",
                    "email_body": "We discovered a SQL injection vulnerability in your login page. Attackers can access all user data. This needs immediate attention.",
                    "sender": "security@researcher.com",
                    "timestamp": "2024-01-15 11:00:00",
                    "expected": {"priority": "urgent", "category": "bug_report"}
                }
            ],
            "medium": [
                {
                    "email_id": "M001",
                    "email_subject": "Question about my invoice #4521",
                    "email_body": "Hi, I received my invoice for this month but the amount seems higher than usual. Could you please explain the charges? My account ID is ACC-789.",
                    "sender": "customer@company.com",
                    "timestamp": "2024-01-15 10:00:00",
                    "expected": {"priority": "normal", "category": "billing"}
                },
                {
                    "email_id": "M002",
                    "email_subject": "Refund request for duplicate charge",
                    "email_body": "I was charged twice for my subscription this month. Please refund the duplicate payment of $49.99. Transaction IDs: TXN001 and TXN002.",
                    "sender": "user123@gmail.com",
                    "timestamp": "2024-01-15 14:00:00",
                    "expected": {"priority": "normal", "category": "billing"}
                },
                {
                    "email_id": "M003",
                    "email_subject": "How do I upgrade my plan?",
                    "email_body": "I am currently on the basic plan and want to upgrade to premium. What are the pricing options and how do I make the switch?",
                    "sender": "business@startup.io",
                    "timestamp": "2024-01-15 15:00:00",
                    "expected": {"priority": "normal", "category": "billing"}
                }
            ],
            "hard": [
                {
                    "email_id": "H001",
                    "email_subject": "Following up on our last conversation",
                    "email_body": "Hey, just wanted to touch base. Hope everything is going well on your end. Let me know if there is anything I can help with.",
                    "sender": "unknown@domain.com",
                    "timestamp": "2024-01-15 16:00:00",
                    "expected": {"priority": "low", "category": "general"}
                },
                {
                    "email_id": "H002",
                    "email_subject": "Feedback on your service",
                    "email_body": "I have been using your product for 6 months. Sometimes it works great, sometimes not so much. Just wanted to share my thoughts. No rush on responding.",
                    "sender": "longtime.user@email.com",
                    "timestamp": "2024-01-15 17:00:00",
                    "expected": {"priority": "low", "category": "general"}
                },
                {
                    "email_id": "H003",
                    "email_subject": "Quick question",
                    "email_body": "Hi team, I was wondering if you have any documentation on your API rate limits. Not urgent, just exploring options for a future project.",
                    "sender": "developer@techco.com",
                    "timestamp": "2024-01-15 18:00:00",
                    "expected": {"priority": "low", "category": "feature_request"}
                }
            ]
        }

    def reset(self, task_level="easy"):
        self.current_task = task_level
        emails = self.emails.get(task_level, self.emails["easy"])
        selected = random.choice(emails)
        self.current_expected = selected["expected"]
        self.state = EmailState(
            email_id=selected["email_id"],
            email_subject=selected["email_subject"],
            email_body=selected["email_body"],
            sender=selected["sender"],
            timestamp=selected["timestamp"],
            task_level=task_level
        )
        return self.state

    def step(self, action: dict):
        reward = self._grade(action)
        return self.state, reward, True, {}

    def _grade(self, action):
        score = 0.0
        expected = self.current_expected

    # Priority grading
        if action.get("priority") == expected.get("priority"):
            score += 0.45
        elif (action.get("priority") == "urgent" and expected.get("priority") == "normal") or \
            (action.get("priority") == "normal" and expected.get("priority") == "urgent"):
            score += 0.15

    # Category grading
        if action.get("category") == expected.get("category"):
            score += 0.45
        elif action.get("category") in ["bug_report", "general"] and \
            expected.get("category") in ["bug_report", "general"]:
            score += 0.15

    # Base score so never exactly 0.0
            score += 0.1

    # Never exactly 1.0
            return min(score, 0.99)


    def get_state(self):
        return self.state
