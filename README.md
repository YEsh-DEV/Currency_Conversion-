# 💱 Currency Conversion Backend

A modern backend service for currency conversion built with **FastAPI**, **Python**, and a modular architecture designed for scalability and future AI-powered integrations.

The project provides REST APIs for currency conversion, health monitoring, and future support for intelligent currency-related workflows using Large Language Models (LLMs).

---

## 🚀 Features

* FastAPI-powered REST API
* Real-time currency conversion architecture
* Modular and maintainable codebase
* Environment-based configuration
* Docker support
* Automated testing support
* Health monitoring endpoint
* Ready for LangChain & Gemini integration
* Scalable backend design

---

## 📂 Project Structure

```text
currency_conversion/
│
├── backend/
│   ├── app.py
│   ├── app_clean.py
│   ├── agent.py
│   ├── llm.py
│   ├── schemas.py
│   │
│   ├── tools/
│   │   └── get_rate.py
│   │
│   └── utils/
│       └── cache.py
│
├── tests/
│   ├── test_agent_flow.py
│   ├── test_converter.py
│   ├── test_parser.py
│   └── mocks/
│
├── .github/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠 Tech Stack

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Core Programming Language |
| FastAPI               | REST API Framework        |
| Pydantic              | Data Validation           |
| Uvicorn               | ASGI Server               |
| Docker                | Containerization          |
| Pytest                | Testing                   |
| LangChain *(Planned)* | AI Orchestration          |
| Gemini *(Planned)*    | LLM Integration           |

---
