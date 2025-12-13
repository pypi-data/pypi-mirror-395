# Changelog

All notable changes to Universal Agent Nexus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

