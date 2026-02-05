# 🛡️ AegisAI – Multi-Agent Operations & Quality Platform

AegisAI is a production-style AI operations platform designed to orchestrate multi-agent AI systems while ensuring output quality, observability, and human oversight.

Unlike simple chatbots, AegisAI focuses on reliability, evaluation, and governance of LLM-powered workflows.

## Short Demo Walkthrough

1. A user message is sent to the FastAPI endpoint.
2. The CoordinatorAgent orchestrates intent detection, execution, and evaluation.
3. AI outputs are scored automatically for quality.
4. Low-confidence outputs are escalated to a human review dashboard.
5. Human decisions are persisted and used for future analysis.
6. Regression tests validate AI behavior before deployment.


# 🚀 Key Capabilities

# Multi-Agent Orchestration

# Role-based agents (Coordinator, Inbox, Action, Reviewer)

Clear separation of responsibilities

LLM-Powered Intelligence

# GPT-based intent classification

Tool-assisted execution (knowledge base, CRM)

Observability & Tracing

# Request-level trace IDs

Agent-level latency tracking

Persistent trace storage (SQLite)

# Automated Quality Evaluation

Confidence-aware quality scoring

Pass / warn / escalate decision gates

# Human-in-the-Loop Review

Streamlit dashboard for reviewing low-quality outputs

Persistent approval/rejection decisions

# Regression Testing for LLMs

Golden dataset testing

Detects intent and quality regressions before deployment