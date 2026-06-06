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

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YEsh-DEV/Currency_Conversion-.git
cd Currency_Conversion-
```

### 2. Create Virtual Environment

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file from the provided template:

```bash
cp .env.example .env
```

Fill in the required values:

```env
API_KEY=your_api_key_here
EXCHANGE_RATE_PROVIDER=provider_name
```

> Never commit real API keys or secrets to GitHub.

---

## ▶️ Running the Application

Start the FastAPI server:

```bash
uvicorn backend.app:app --reload --port 8001
```

The API will be available at:

```text
http://localhost:8001
```

---

## 📖 API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```text
http://localhost:8001/docs
```

### ReDoc

```text
http://localhost:8001/redoc
```

---

## 🔗 API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

### Currency Conversion

```http
POST /convert
```

Request Example:

```json
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "EUR"
}
```

Example Response:

```json
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "EUR",
  "converted_amount": 92.45,
  "exchange_rate": 0.9245
}
```

> Actual response structure may vary based on implementation in `schemas.py`.

---

## 🧪 Running Tests

Run all tests:

```bash
pytest
```

Run with detailed output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_converter.py
```

---

## 🐳 Docker Support

### Build Docker Image

```bash
docker build -t currency-conv:dev .
```

### Run Container

```bash
docker run --rm -p 8001:8000 --env-file .env currency-conv:dev
```

### Using Docker Compose

```bash
docker-compose up --build
```

---

## 🔄 Development Workflow

```bash
git pull origin main

# Make changes

git add .
git commit -m "Describe your changes"
git push origin main
```

---

## 🏗 Architecture Overview

```text
Client
   │
   ▼
FastAPI Application
   │
   ├── Request Validation (Pydantic)
   ├── Currency Conversion Logic
   ├── Exchange Rate Provider
   ├── Cache Layer
   └── Future AI Agent Layer
```

---

## 🔮 Future Enhancements

* Live exchange-rate provider integration
* LangChain agent support
* Gemini API integration
* Historical exchange rate analysis
* Currency trend forecasting
* Authentication & authorization
* Rate limiting
* Monitoring & observability
* CI/CD pipeline deployment

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## 📜 License

This project is available under the MIT License.

---

## 👨‍💻 Author

Developed by **YEsh-DEV**

If you find this project useful, consider giving it a ⭐ on GitHub.
