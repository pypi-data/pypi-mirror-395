# Changelog

All notable changes to Universal Agent Nexus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.1] - 2025-12-07

### Fixed

#### Runtime API Mismatch
- **Fixed**: Runtime was calling `await compiler.compile_async()` but v3.0.0 compiler only has synchronous `compile()`
- Changed `runtime.py` line 136: `await compiler.compile_async()` → `compiler.compile()`

### Added

#### LangGraph Compiler Tests
- Added comprehensive unit tests for the v3.0.0 compiler
- Tests path map building, router creation, condition detection, LLM config extraction
- Tests skip gracefully when LangGraph not installed

---

## [3.0.0] - 2025-12-07

### ⚠️ BREAKING CHANGES

#### LangGraph Compiler Rewrite - Let LangGraph Do the Heavy Lifting
- **Reduced from 453 → 195 lines** (57% less code)
- **State shape changed**: `AgentState` → `MessagesState` (LangGraph's built-in)
- **Removed**: Custom expression evaluation (simpleeval no longer used in compiler)
- **Removed**: Complex routing logic - now uses simple route key matching
- **Removed**: Manual tool invocation wrappers

#### Philosophy Change
The compiler now follows the principle: **YAML → LangGraph translation only**.
LangGraph handles: routing, state management, message history, error recovery.

#### Migration Guide
```python
# Before (v2.x) - Custom state
state = {"context": {...}, "history": [...], "current_node": "..."}

# After (v3.0) - LangGraph MessagesState  
state = {"messages": [HumanMessage(...), AIMessage(...)]}
```

#### What's Simpler Now
- Router nodes just invoke LLM and return response
- Routing matches route keys against last message content
- No custom state negotiation
- No expression evaluation complexity

---

## [2.0.6] - 2025-12-07

### Fixed

#### Compiler Now Checks Both router_ref and router Attributes
- **Fixed**: Compiler was checking `node_spec.router` (AgentManifest schema) but IR uses `node_spec.router_ref`
- Now checks `router_ref` first (IR/NodeIR), then falls back to `router` (AgentManifest) for backwards compatibility
- Fixes router nodes not finding their LLM configuration when using IR-based workflows

---

## [2.0.5] - 2025-12-07

### Fixed

#### YAML Parser Now Supports Both Ref Formats
- Parser now accepts both nested and flat formats for router/tool references:
  ```yaml
  # Nested format (standard)
  router:
    name: "my_router"
  
  # Flat format (also works now)
  router_ref: "my_router"
  ```
- Added `_get_ref_value()` helper for flexible ref parsing

---

## [2.0.4] - 2025-12-07

### Fixed

#### LLMFactory Default URL Override Bug
- **Fixed**: `base_url: None` was being passed explicitly to `LLMFactory`, overriding its default `http://localhost:11434` for Ollama
- Now only includes `base_url` and `api_key` in config when explicitly set (truthy)
- Allows `LLMFactory` defaults to work correctly without manual config

---

## [2.0.3] - 2025-12-07

### Fixed

#### Router Node LLM Configuration Fallback
- **Router nodes now support multiple configuration sources** with cascading fallback:
  1. Standard `router: {name: ...}` → `routers[]` lookup (recommended)
  2. Inline config via `metadata.llm` and `metadata.system_message`
  3. Inline config via `inputs.llm` and `inputs.system_message`

- **Fixed**: `router_ref` was returning `None` when YAML used string format instead of object
- **Added**: Support for both `RouterRef` object and string format
- **Improved**: Better error messages when LLM configuration is missing

```yaml
# Option 1: Standard (recommended)
nodes:
  - id: risk_assessment
    kind: router
    router:
      name: risk_router

routers:
  - name: risk_router
    default_model: "ollama://qwen3:8b"
    system_message: "Classify risk..."

# Option 2: Inline via metadata (simpler DX)
nodes:
  - id: risk_assessment
    kind: router
    metadata:
      llm: "ollama://qwen3:8b"
      system_message: "Classify risk..."
```

---

## [2.0.2] - 2025-12-07

### Added

#### LLMFactory for Multi-Provider Support
- **LLMFactory**: Provider-aware LLM instantiation for LangGraph adapter
- Supports connection string format: `provider://model_name`
- Providers: `openai`, `ollama`, `local`, `anthropic`

```python
from universal_agent_nexus.adapters.langgraph import LLMFactory

llm = LLMFactory.create("ollama://llama3")
llm = LLMFactory.create("local://qwen3", {"base_url": "http://localhost:1234/v1"})
llm = LLMFactory.create("anthropic://claude-3-sonnet")
```

#### Router Config Options
- Routers now support `config` block for LLM settings:
  - `temperature`: float
  - `base_url`: endpoint override
  - `api_key`: API key override

```yaml
routers:
  - name: "classifier"
    default_model: "ollama://llama3"
    config:
      temperature: 0.2
      base_url: "http://localhost:11434"
```

### Dependencies

- New optional dependency groups:
  - `pip install universal-agent-nexus[ollama]` → `langchain-ollama>=0.2.0`
  - `pip install universal-agent-nexus[anthropic]` → `langchain-anthropic>=0.2.0`
- `[all]` extra now includes `ollama` and `anthropic`

---

## [2.0.1] - 2025-12-07

### Fixed

#### LangGraph Router Edge Processing Bug
- **BREAKING BUG FIX**: Router nodes with multiple outgoing edges were causing concurrent execution instead of conditional routing
- Root cause: Compiler processed edges individually, calling `add_edge()` for each edge from the same node
- Multiple `add_edge()` calls from same node = parallel execution in LangGraph (not conditional)
- `condition.expression` and `condition.route` were completely ignored

#### Solution
- Group edges by `from_node` before processing
- Use topology-based `_requires_routing()` to detect branching needs
- Generate routing function that evaluates conditions in priority order:
  1. Error handlers (if state has error)
  2. Expression conditions (evaluated safely via simpleeval)
  3. Route key matching (string/semantic match)
  4. Unconditional/default edges
  5. Fallback to END
- Call `add_conditional_edges()` once per router with path map

### Security

#### Eliminated eval() RCE Vulnerability (Project-Wide)
- Replaced ALL dangerous `eval()` calls with `simpleeval` library
- Prevents Remote Code Execution from malicious manifest expressions
- Fixed in:
  - `LangGraphCompiler._evaluate_expression_safe()`
  - `EdgeCondition.evaluate()`
  - `ConstantFolding._try_evaluate()`

### Dependencies

- Added `simpleeval>=1.0.0` as core dependency (safe AST-based expression evaluation)

---

## [2.0.0] - 2025-12-07

### 🎯 Major Release: Full Ecosystem Integration

This release completes the integration between Universal Agent Nexus, Fabric, and Architecture,
making the UAA Kernel a first-class compilation target with full cross-runtime state portability.

### Added

#### UAA Native Adapter (`--target uaa`)
- **UAANativeGenerator**: Compiles ManifestIR directly to UAA AgentManifest format
- **UAANativeRuntime**: Executes manifests through the UAA GraphEngine
- **UAANativeRuntimeBuilder**: Builder pattern for dependency injection
- Registered as target `uaa` with aliases `uaa_native`, `kernel`

```bash
# Compile directly for UAA Kernel
nexus compile agent.yaml --target uaa --output kernel_manifest.yaml
```

#### Universal State Bridge (`bridges/universal_state.py`)
- **NormalizedGraphState**: Canonical state representation across all runtimes
- **NormalizedHistoryEntry**: Full execution history preservation
- **normalize()**: Convert LangGraph/AWS state → UAA format
- **denormalize()**: Convert UAA format → LangGraph/AWS
- **sync_state()**: Direct runtime-to-runtime state translation
- **detect_format()**: Auto-detect source runtime format

```python
from universal_agent_nexus.bridges import normalize, denormalize, StateFormat

# Normalize LangGraph checkpoint to UAA format
normalized = normalize(langgraph_checkpoint)

# Convert to AWS Step Functions format
aws_input = denormalize(normalized, StateFormat.AWS)
```

#### ContractRegistry (in universal-agent-arch)
- Service locator for UAA contract implementations
- Support for ITaskStore, ITaskQueue, IToolExecutor, ILLMClient
- Lazy factory registration for deferred instantiation
- Environment variable configuration (`UAA_TASK_STORE`, etc.)
- Dynamic type registry for config-driven instantiation

```python
from universal_agent_architecture.runtime import ContractRegistry, get_global_registry

registry = get_global_registry()
registry.configure_from_env()
```

### Changed

- **Ecosystem diagram** in README updated to show complete integration flow
- **Package exports** now include state normalization at top level
- **Dependencies**: Updated to `universal-agent-arch>=0.3.0`, `universal-agent-fabric>=0.2.1`

### Ecosystem Integration

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FABRIC (Composition)                                 │
│   Role + Domain + Policy → NexusEnricher → Enriched Manifest                │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────────────┐
│                         NEXUS  │ (Compiler)                                  │
│   ✅ LangGraph   ✅ AWS   ✅ MCP   ✅ UAA Native (NEW)                       │
│   ✅ State Normalization Bridge (NEW)                                        │
└────────────────────────────────┼────────────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────────────┐
│                    ARCHITECTURE│ (Kernel)                                    │
│   GraphEngine + Handlers + PolicyEngine + ContractRegistry (NEW)            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## [1.0.0] - 2025-12-05

### 🚀 First Production Release

Universal Agent Nexus is now production-ready with an IR-based compiler architecture,
comprehensive validation, and benchmarked performance.

### Added

#### IR-Based Compiler
- **LLVM-style architecture**: Parser → IR → Transform → Generator
- **Bidirectional translation**: LangGraph ↔ AWS ↔ UAA YAML
- **PassManager**: Optimization levels O0-O3 (like GCC/Clang)
- **Transformation passes**:
  - Dead node elimination
  - Edge deduplication
  - Condition simplification
  - Constant folding
  - Router/Tool validation
  - Cycle detection

#### Comprehensive Validation
- **IRValidator**: 5-pass validation system
- **Error codes**: E001-E203 (errors), W301-W304 (warnings)
- **Source locations**: File:line:column in error messages
- **Hints**: Actionable suggestions for fixing errors

#### Performance Optimizations
- `boto3 + asyncio.to_thread` instead of aioboto3 (30% faster)
- DynamoDB batch operations (25x faster bulk writes)
- Postgres prepared statements (2-3x faster queries)
- Connection pooling (max_pool_connections=50)

#### Testing & Benchmarks
- 55 unit tests passing
- 5 performance benchmarks
- Full compiler pipeline: 0.4-0.5ms (2,000 compiles/sec)

#### Infrastructure
- Terraform modules for AWS deployment
- Lambda functions for tool execution
- GitHub Actions CI/CD

### Performance Numbers

| Operation | Time | Throughput |
|-----------|------|------------|
| IR Parsing | 0.45ms | 2,200/sec |
| Transform Passes | 0.07ms | 15,500/sec |
| Code Generation | 0.03-0.07ms | 14,000-33,000/sec |
| Full Compile | 0.4-0.5ms | 2,000/sec |
| Validation | 0.03ms | 31,000/sec |

### Breaking Changes

- Removed `translators/` directory (use `ir/parser.py` instead)
- Removed libCST dependency (using stdlib `ast` - 20x faster)
- Removed `LangGraphCheckpointerBridge` (use `AsyncPostgresSaver` directly)
- Removed `aioboto3` dependency (using `boto3 + asyncio.to_thread`)

### Migration Guide

**From translators to IR:**
```python
# Old (removed)
from universal_agent_nexus.translators import translate_to_uaa

# New
from universal_agent_nexus.compiler import compile
result = compile("agent.py", target="uaa")
```

**From aioboto3 to boto3:**
```python
# Old (removed)
import aioboto3
session = aioboto3.Session()
async with session.client("stepfunctions") as client:
    await client.start_execution(...)

# New
import boto3
import asyncio
client = boto3.client("stepfunctions")
await asyncio.to_thread(client.start_execution, ...)
```

---

## [0.2.0] - 2025-12-05

### Added
- LangGraph adapter with Postgres checkpointing
- AWS Step Functions adapter with DynamoDB
- MCP server adapter
- OpenTelemetry observability
- Nexus ↔ Fabric integration

### Changed
- Replaced aioboto3 with boto3 + asyncio.to_thread
- Direct AsyncPostgresSaver usage (removed bridge)

---

## [0.1.0] - 2025-12-04

### Added
- Initial project structure
- Basic UAA manifest schema
- CLI scaffolding
- Terraform infrastructure templates

