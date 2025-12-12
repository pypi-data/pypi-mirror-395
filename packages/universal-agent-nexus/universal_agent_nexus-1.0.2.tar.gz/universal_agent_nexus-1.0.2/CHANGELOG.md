# Changelog

All notable changes to Universal Agent Nexus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

