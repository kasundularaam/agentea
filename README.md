# Agentea

Agentea is a multi-agent API development starter project designed to help you build scalable and maintainable AI agent systems. It leverages Domain-Driven Design (DDD) and Hexagonal Architecture (Ports and Adapters) principles to ensure clean separation of concerns and testability.

## 🚀 Features

- **Multi-Agent Architecture**: Built to support complex chains and interactions between multiple agents.
- **DDD & Hexagonal Design**: clearly separates Core Domain, Application Logic, and Infrastructure (Ports & Adapters).
- **Dependency Injection**: Fully wired using [dependency-injector](https://python-dependency-injector.ets-labs.org/) for modularity and easy testing.
- **Modern Python Stack**: built with Python 3.12+, **uv** for fast package management, and **FastAPI**.
- **Pre-included Services**:
  - **Vector Database**: Milvus
  - **SQL Database**: Trino
  - **LLM Embeddings**: Google Gemini
  - **Observability & Evaluation**: Opik

## 🛠️ Technology Stack

- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Web Framework**: FastAPI (with Uvicorn)
- **Dependency Injection**: dependency-injector
- **Validation**: Pydantic
- **AI/ML**: Google Cloud Vertex AI (Gemini), LangChain/Google ADK (implied by ADKAgentsChain)

## 📂 Project Structure

The project follows a strict Hexagonal Architecture structure:

```
src/
├── application/       # Application layer (Use Cases)
│   └── reply_message.py
├── domain/            # Core Domain logic (Entities, Ports, Interfaces)
│   ├── agents/
│   ├── entities/
│   └── ports/         # Abstract interfaces for infrastructure
├── infrastructure/    # Adapters (Implementations of Ports)
│   ├── repositories/
│   ├── services/      # External services (Milvus, Trino, Opik, Gemini)
│   └── routers/       # API Adapters (FastAPI routers)
└── routers/           # HTTP Entry-points (FastAPI)
```

## ⚡ Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) installed
- Access to Google Cloud Vertex AI and other services (Milvus/Trino/Opik)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd agentea
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Environment Setup**:
   Create a `.env` file in the root directory and configure your service credentials.
   
   *Key variables likely needed (check `.env.example` if available or the code):*
   - `VERTEX_AI_PROJECT_ID`
   - `GOOGLE_CLOUD_LOCATION`
   - Connection strings for Milvus, Trino, Opik.

### Running the Application

Start the development server:

```bash
uv run app.py
```
Or directly with Python if dependencies are activated:
```bash
python app.py
```

The API will be available at `http://localhost:8000`.

## 🔌 API Endpoints

- **POST /reply**: Blocking endpoint to get a response from the agent chain.
  - Query Param: `new_message` (str)
- **POST /stream**: Streaming endpoint (SSE) to get real-time tokens from the agent.
  - Query Param: `new_message` (str)

## 🧩 Architecture Details

### Dependency Injection
The project uses `dependency-injector` to manage components. The container is defined in `injection.py`.

- **BaseContainer**: Defines the abstract dependencies (Ports).
- **DevContainer**: Wires the concrete implementations (Adapters) for development, such as `MilvusVectorDBService`, `TrinoDatabaseService`, etc.

### Adding New Services
1. Define a Port in `src/domain/ports/`.
2. Implement the Adapter in `src/infrastructure/services/`.
3. Register the service in `injection.py`.
