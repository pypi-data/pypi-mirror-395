<div align="center">

# **Universal Agent Nexus**

### *The Translation Layer: Build Once, Run Anywhere*

**Compile universal agent architectures to LangGraph, AWS Step Functions, or MCP—without rewriting code.**

[![PyPI version](https://img.shields.io/pypi/v/universal-agent-nexus.svg)](https://pypi.org/project/universal-agent-nexus/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/mjdevaccount/universal_agent_nexus/actions/workflows/test.yml/badge.svg)](https://github.com/mjdevaccount/universal_agent_nexus/actions)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

[**Quick Start**](#-quick-start) • [**Documentation**](docs/) • [**Examples**](examples/) • [**Report Bug**](https://github.com/mjdevaccount/universal_agent_nexus/issues)

</div>

---

## 🎯 **What is Universal Agent Nexus?**

### **For the Impatient (TL;DR)**

Universal Agent Nexus is a **compilation framework** that takes your agent definition (a single YAML manifest) and outputs production-ready code for:

- **LangGraph** (local development with Postgres checkpointing)
- **AWS Step Functions** (serverless state machines with DynamoDB)
- **MCP** (Model Context Protocol for Claude/Cursor/VS Code)

**Write once. Deploy everywhere.**

```bash
# Define your agent once
cat manifest.yaml

# Compile to LangGraph
nexus compile manifest.yaml --target langgraph --output ./graph.py

# OR compile to AWS Step Functions
nexus compile manifest.yaml --target aws --output ./state_machine.json

# OR expose as MCP server
nexus serve manifest.yaml --protocol mcp --transport stdio
```

**That's it. No vendor lock-in. No rewrites.**

---

### **For the Curious (Deeper Dive)**

**The Problem:**

You've built an AI agent that orchestrates LLM calls, tool invocations, and multi-step workflows. Now you need to:

1. **Develop locally** with fast iteration (LangGraph)
2. **Deploy to production** at scale (AWS Step Functions)
3. **Expose to AI clients** like Claude Desktop (MCP)

**Traditional approach:** Write three separate implementations. Maintain three codebases. Deal with divergence.

**Universal Agent Nexus approach:** Write a **Universal Agent Architecture (UAA) manifest** once. Let the compiler handle the rest.

```yaml
# manifest.yaml - Your single source of truth
name: content-moderation-pipeline
graphs:
  - name: moderate_content
    nodes:
      - id: risk_assessment
        kind: router
        label: "AI Risk Classifier"
      - id: policy_check
        kind: tool
        label: "Policy Validator"
      - id: human_review
        kind: task
        label: "Escalate to Human"
    edges:
      - from_node: risk_assessment
        to_node: policy_check
        condition: { expression: "risk_level > 0.3" }
```

**The compiler generates:**
- **LangGraph:** Python StateGraph with Postgres checkpointing
- **AWS:** Step Functions state machine (ASL) + Lambda functions + DynamoDB
- **MCP:** Tool definitions for Claude/Cursor integration

---

## 🚀 **Quick Start**

### **Prerequisites**

```bash
# Python 3.11+
python --version

# Docker (for local Postgres/DynamoDB)
docker --version
```

### **Installation**

```bash
# Install base package
pip install universal-agent-nexus

# Install with all adapters (LangGraph, AWS, MCP)
pip install "universal-agent-nexus[all]"

# Or install specific adapters
pip install "universal-agent-nexus[langgraph]"  # LangGraph only
pip install "universal-agent-nexus[aws]"        # AWS only
pip install "universal-agent-nexus[mcp]"        # MCP only
```

### **Hello World (30 seconds)**

```bash
# 1. Create a manifest
cat > hello.yaml << EOF
name: hello-agent
version: "1.0.0"
graphs:
  - name: main
    entry_node: greet
    nodes:
      - id: greet
        kind: task
        label: "Say Hello"
    edges: []
EOF

# 2. Compile to LangGraph
nexus compile hello.yaml --target langgraph --output hello_graph.py

# 3. Run locally
python hello_graph.py
```

**Output:**
```
✅ LangGraph runtime initialized
Executing graph: main
Result: Hello from Universal Agent Nexus!
```

---

## 📚 **Core Concepts**

### **1. Universal Agent Architecture (UAA)**

The **Universal Agent Architecture** is a specification for defining multi-step agent workflows as portable, runtime-agnostic manifests.

**Key components:**

- **Graph:** A directed graph of nodes (tasks, routers, tools) connected by edges
- **Node:** A single execution unit (LLM call, tool invocation, conditional logic)
- **Edge:** Transition between nodes (with optional conditions)
- **Tool:** External capability (API, database, MCP server)
- **Router:** Decision point that chooses next action(s) dynamically

### **2. Compilation Targets (Adapters)**

| Target | Best For | Execution Model | State Storage |
|--------|----------|-----------------|---------------|
| **LangGraph** | Local dev, debugging | Python async | PostgreSQL |
| **AWS** | Production scale | Step Functions, Lambda | DynamoDB |
| **MCP** | AI client integration | stdio transport | In-memory |

### **3. The IR-Based Compiler (v1.0.0)**

Universal Agent Nexus uses an **LLVM-style IR architecture** for bidirectional translation:

```
┌────────────────────────────────────────────────────────────┐
│                     FRONTENDS (Parsers)                    │
│  LangGraph → IR  |  AWS → IR  |  YAML → IR                │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                  INTERMEDIATE REPRESENTATION               │
│            ManifestIR { GraphIR, ToolIR, RouterIR }        │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                   TRANSFORMATION PASSES                    │
│  Dead code elimination | Edge deduplication | Validation   │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                    BACKENDS (Generators)                   │
│  IR → LangGraph  |  IR → AWS  |  IR → YAML                │
└────────────────────────────────────────────────────────────┘
```

**Bidirectional translation:**
```bash
# LangGraph → AWS
nexus translate agent.py --to aws --out state_machine.json

# AWS → LangGraph (REVERSE!)
nexus translate state_machine.json --to langgraph --out agent.py
```

---

## 🔌 **Adapters**

### **LangGraph Adapter**

**Purpose:** Local development with full debugging capabilities

**Features:**
- ✅ Async Python execution with asyncio
- ✅ Postgres checkpointing (AsyncPostgresSaver)
- ✅ MCP tool integration
- ✅ LLM router nodes (OpenAI, Anthropic)

```python
from universal_agent_nexus.adapters.langgraph import LangGraphRuntime, load_manifest

manifest = load_manifest("manifest.yaml")
runtime = LangGraphRuntime(
    postgres_url="postgresql://localhost:5432/uaa_dev",
    enable_checkpointing=True
)

await runtime.initialize(manifest, graph_name="main")
result = await runtime.execute(
    execution_id="exec-001",
    input_data={"context": {"query": "Hello!"}}
)
```

---

### **AWS Adapter**

**Purpose:** Production deployment at enterprise scale

**Components:**
- **Step Functions** - State machine execution
- **Lambda** - Tool execution functions
- **DynamoDB** - State persistence (single-table design)
- **CloudWatch** - Logging and metrics
- **X-Ray** - Distributed tracing

```bash
# Compile to AWS Step Functions
nexus compile manifest.yaml --target aws --output state_machine.json

# Deploy with Terraform
cd terraform/environments/prod
terraform apply
```

---

### **MCP Adapter**

**Purpose:** Expose agents as tools to AI clients (Claude, Cursor, VS Code)

```bash
# Start MCP server
nexus serve manifest.yaml --protocol mcp --transport stdio
```

**Claude Desktop configuration:**
```json
{
  "mcpServers": {
    "uaa-agent": {
      "command": "nexus",
      "args": ["serve", "/path/to/manifest.yaml", "--protocol", "mcp"]
    }
  }
}
```

---

## ✨ **Features**

### **Core Features**
- ✅ **Write Once, Run Anywhere** - Single manifest compiles to LangGraph, AWS, MCP
- ✅ **Production-Ready** - Built-in state persistence, error handling, observability
- ✅ **Type-Safe** - Pydantic schemas with full validation
- ✅ **Async-Native** - asyncio throughout, no blocking calls

### **Observability**
- ✅ **OpenTelemetry** - Distributed tracing across all adapters
- ✅ **Structured Logging** - JSON logs with execution context
- ✅ **CloudWatch Integration** - Automatic log/metric export (AWS)
- ✅ **X-Ray Tracing** - End-to-end request tracing (AWS)

```python
from universal_agent_nexus.observability import setup_tracing, trace_execution

setup_tracing(service_name="my-agent", environment="production")

async with trace_execution("execute_graph", execution_id="exec-001"):
    result = await runtime.execute(...)
```

### **IR Validation (v1.0.0)**

Comprehensive validation with error codes and source locations:

```python
from universal_agent_nexus.ir.validation import validate_ir, validate_and_raise

errors = validate_ir(ir)
for error in errors:
    print(error)
# error[E001]: Entry node 'start' not found
#   = hint: Add a node with id='start'

# Or raise on any error
validate_and_raise(ir, strict=True)
```

**Error codes:**
| Code | Category | Description |
|------|----------|-------------|
| `E001-E004` | Structural | Missing nodes, bad edges |
| `E101-E104` | Type | Missing refs, unknown tools |
| `E201-E203` | Semantic | No outgoing edges |
| `W301-W304` | Warnings | Unreachable nodes, no terminal |

### **PassManager (v1.0.0)**

LLVM-style optimization levels:

```python
from universal_agent_nexus.compiler import compile
from universal_agent_nexus.ir.pass_manager import OptimizationLevel

# No optimization (fastest compile)
compile("agent.py", target="aws", opt_level=OptimizationLevel.NONE)

# Aggressive optimization (slowest compile, best output)
compile("agent.py", target="aws", opt_level=OptimizationLevel.AGGRESSIVE)
```

Available passes:
- Dead node elimination
- Edge deduplication
- Condition simplification
- Constant folding
- Router/Tool validation
- Cycle detection

---

## ⚡ **Performance**

### **Compiler Benchmarks (v1.0.0)**

| Operation | Time | Throughput |
|-----------|------|------------|
| **IR Parsing** | 0.45ms | 2,200/sec |
| **Transform Passes** | 0.07ms | 15,500/sec |
| **Code Generation** | 0.03-0.07ms | 14,000-33,000/sec |
| **Full Compile Pipeline** | **0.4-0.5ms** | **2,000/sec** |
| **Validation** | 0.03ms | 31,000/sec |

### **Runtime Benchmarks**

| Metric | LangGraph (Local) | AWS (Serverless) |
|--------|-------------------|------------------|
| **Cold Start** | 50ms | 200-300ms (Lambda) |
| **Warm Execution** | 10-20ms/node | 15-25ms/node |
| **State Persistence** | 5ms (Postgres) | 3ms (DynamoDB) |
| **Throughput** | 1,000 req/sec | 10,000+ req/sec |

### **Optimizations (v1.0.0)**
- ✅ **boto3 + asyncio.to_thread** - 30% faster than aioboto3
- ✅ **DynamoDB batch operations** - 25x faster bulk writes
- ✅ **Postgres prepared statements** - 2-3x faster queries
- ✅ **Connection pooling** - max_pool_connections=50
- ✅ **Direct AsyncPostgresSaver** - no bridge overhead

---

## 📁 **Project Structure**

```
universal_agent_nexus/
├── universal_agent_nexus/      # Core package
│   ├── adapters/               # Runtime adapters
│   │   ├── langgraph/          # LangGraph adapter
│   │   ├── aws/                # AWS adapter
│   │   └── mcp/                # MCP adapter
│   ├── cli/                    # CLI interface
│   └── observability/          # Tracing & logging
├── terraform/                  # Infrastructure as Code
│   ├── modules/                # Reusable modules
│   └── environments/           # Environment configs
├── lambda/                     # Lambda function code
├── examples/                   # Example manifests
└── tests/                      # Test suite
```

---

## 🧪 **Testing**

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests (requires Docker)
docker-compose up -d postgres
pytest tests/integration/

# With coverage
pytest --cov=universal_agent_nexus --cov-report=html
```

**Current status:** 55 tests + 5 benchmarks passing

---

## 🚀 **Deployment**

### **Local Development**

```bash
# Start Postgres
docker run -d -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=uaa_dev \
  postgres:16-alpine

# Run agent locally
python examples/hello_langgraph/run.py
```

### **AWS Production**

```bash
# Compile manifest
nexus compile manifest.yaml --target aws \
  --output terraform/environments/prod/state_machine.json

# Deploy with Terraform
cd terraform/environments/prod
terraform init
terraform apply

# Execute
aws stepfunctions start-execution \
  --state-machine-arn $(terraform output -raw state_machine_arn) \
  --input '{"context": {"query": "Hello!"}}'
```

---

## ⚙️ **Configuration**

### **Environment Variables**

```bash
# LangGraph
UAA_POSTGRES_URL=postgresql://localhost:5432/uaa_dev
UAA_LOG_LEVEL=INFO

# AWS
AWS_REGION=us-east-1
AWS_DYNAMODB_TABLE=uaa-agent-state

# Observability
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=universal-agent-nexus

# LLM APIs
OPENAI_API_KEY=sk-...
```

---

## 🤝 **Contributing**

We welcome contributions! 

```bash
# Clone repository
git clone https://github.com/mjdevaccount/universal_agent_nexus.git
cd universal_agent_nexus

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format .
ruff check . --fix
```

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

Built with inspiration from:
- **LangChain/LangGraph** - Agent orchestration patterns
- **AWS Step Functions** - State machine execution model
- **Model Context Protocol (MCP)** - AI client integration standard
- **Terraform** - Infrastructure as code principles

---

<div align="center">

**Made with ❤️ by the Universal Agent Nexus team**

⭐ **Star us on GitHub** if this project helps you!

</div>
