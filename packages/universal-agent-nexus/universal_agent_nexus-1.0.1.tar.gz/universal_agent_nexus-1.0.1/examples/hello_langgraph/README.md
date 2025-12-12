# Hello LangGraph example

Minimal proof-of-concept for running a UAA manifest through the LangGraph adapter.

## Setup

1) Install dependencies (langgraph + observability extras):
```bash
pip install -e ".[langgraph,observability]"
```

2) Start Postgres (example):
```bash
docker run --name uaa-postgres -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=uaa_dev -p 5432:5432 -d postgres:16
```

3) Set OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
```

4) Run example:
```bash
cd examples/hello_langgraph
python run.py
```

Expected output: router node logs and a final response stored in context.
