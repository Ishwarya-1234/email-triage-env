---
title: Email Triage Env
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Email Triage Environment

An OpenEnv-compatible RL environment where an AI agent learns to triage emails by priority and category.

## Overview
The agent reads emails and must classify them by:
- **Priority**: urgent / normal / low
- **Category**: bug_report / billing / general

## Tasks
- **Easy**: Single critical bug report email
- **Medium**: Billing inquiry email
- **Hard**: Ambiguous follow-up email

## API Endpoints
- `POST /reset` - Reset environment with task level
- `GET /state` - Get current email state
- `POST /step` - Submit agent action and get reward
- `GET /tasks` - List all tasks

## Reward
- Correct priority: +0.5
- Correct category: +0.5