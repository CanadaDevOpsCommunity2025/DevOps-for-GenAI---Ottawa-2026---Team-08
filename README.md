# AI Observability

**DevOps for GenAI – Ottawa Hackathon Series 2026**
**Team 08**
**Selected Theme:** Unified AI Observability

## Overview

### Elevator Pitch

Obeverfy is a lightweight observability SDK for Python-based AI agents that makes their execution visible in real time. Developers add a simple @traced decorator to agent functions, and Obeverfy automatically captures nested execution spans, inputs, outputs, status, errors, and timing. A live dashboard then visualizes the resulting trace, helping developers understand how multi-step agents behave and where failures occur.

### Problem Statement

AI agents can perform multiple LLM calls, tool calls, and decision-making steps during a single task, making it difficult for developers to understand what happened when an agent behaves unexpectedly. Traditional application logs may show individual events but do not necessarily preserve the parent-child relationships, inputs, outputs, timing, and status of each step in an agent workflow. Obeverfy addresses this by capturing structured traces of agent execution and presenting them as a live hierarchical view.

### Target Users

Developers and Teams building function-based Python AI agents who need visibility into agent execution for debugging, testing, and monitoring.

---

## Architecture

### Architecture Diagram

TODO: Add architecture diagram.

<!-- Example:
![Architecture Diagram](docs/architecture.png)
-->

### Technology Stack

Backend / SDK: Python 3.12, supabase-py, python-dotenv
Testing: pytest
Database / Infrastructure: Supabase Postgres, Row Level Security, Supabase Realtime
Frontend: React 18, Vite, @supabase/supabase-js, CSS
AI: OpenAI Responses API
Observability SDK: custom Obeverfy Python SDK using decorators and contextvars

### AI Tool Inventory

TODO: List AI models, APIs, coding assistants, agents, or other AI tools used in the project.

### AI Usage Disclosure

TODO: Describe where and how AI was used during development, including both AI incorporated into the system and AI-assisted development.

---

## Running the Project

### Working Demo

**Live Demo:** TODO: Add URL if applicable

If no hosted demo is available, follow the setup instructions below to reproduce the project locally.

### Prerequisites

TODO: List required software, versions, accounts, environment requirements, etc.

### Setup

TODO: Add installation and configuration steps.

### Running Locally

TODO: Add commands and instructions required to start the project.

### Configuration and Environment Variables

TODO: Document required environment variables and configuration. Do **not** include real credentials or secrets.

---

## Repository

**GitHub Repository:** TODO: Add repository URL

### Repository Structure

TODO: Add a brief description of important directories and components if useful.

---

## Security

### Threat Model

TODO: Document:

* Key assets that require protection
* Trust boundaries
* Potential threat actors
* Major attack vectors
* Security controls and mitigations
* Remaining risks

### Security and Adversarial Testing

TODO: Add evidence/results from security, abuse-case, prompt-injection, adversarial, or other relevant testing.

### Secrets and Repository Hygiene

TODO: Document secrets-scanning tools/results and repository hygiene checks.

---

## AI Governance

### AI System Card

TODO: Document the AI system's:

* Purpose and intended use
* Model(s) or AI services used
* Inputs and outputs
* Known risks
* Safeguards
* Human oversight
* Limitations

---

## DevOps

### CI/CD Pipeline

TODO: Describe the CI/CD workflow and provide evidence of successful pipeline execution.

### Testing

TODO: Describe the project's testing strategy and provide evidence/results.

Examples may include:

* Unit tests
* Integration tests
* End-to-end tests
* Security tests
* AI/model evaluation tests

### Observability

TODO: Describe implemented logging, metrics, tracing, alerting, dashboards, or other observability capabilities and provide evidence where appropriate.

### SBOM and Dependency Inventory

TODO: Describe how dependencies are tracked and provide an SBOM or dependency inventory where applicable.

---

## Demo and Presentation

**Demo Video:** TODO: Add URL

**Live Presentation:** TODO: Add details if applicable

---

## Known Limitations

Instrumentation requires adding @traced to functions; it does not automatically instrument existing agent frameworks; only synchronous function-based tracing appears to be covered by the current implementation; telemetry currently captures function inputs/outputs without configurable redaction; the dashboard's anonymous access model is intentionally simplified for the hackathon; and the insurance agent is a demonstration rather than a production claims system.

## Future Roadmap

Async-function support, configurable sensitive-data redaction, authentication/access control for dashboards, framework integrations such as LangChain/CrewAI, filtering/searching traces, metrics/aggregation, retention policies, and additional exporters/backends.

---

## Team

|   Team Member   | Role / Contribution |
| --------------- | ------------------- |
| Armando Malpica | Project Lead        |
| Caelen Roberge  | Backend Expert      |
| Yassine Amraoi  | Thought Specialist  |
| Joseph Coakeley | Thought Leader      |

---

## Submission Checklist

* [ ] Project name and selected theme
* [ ] Elevator pitch
* [ ] Problem statement and target users
* [ ] Architecture diagram
* [ ] Working demo / URL or reproducible run
* [ ] GitHub repository
* [ ] Technology and AI-tool inventory
* [ ] AI usage disclosure
* [ ] Security threat model
* [ ] Security/adversarial test evidence
* [ ] Governance / AI system card
* [ ] CI/CD pipeline evidence
* [ ] Testing evidence
* [ ] Observability evidence
* [ ] SBOM/dependency inventory where applicable
* [ ] Secrets scan / repository hygiene evidence
* [ ] Runbook / setup instructions
* [ ] Demo video or live presentation
* [ ] Known limitations and future roadmap
* [Y] Team member list
