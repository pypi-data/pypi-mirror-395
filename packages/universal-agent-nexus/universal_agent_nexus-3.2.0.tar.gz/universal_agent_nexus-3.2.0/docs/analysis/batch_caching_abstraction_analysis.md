# Anthropic Batch + Prompt Caching in Universal Agent Nexus

## Executive Summary

Your architecture has **exactly** the abstractions needed to layer in Batch + Prompt Caching. The critical question is not "what abstractions do I need?" but rather "where do I inject the compilation logic?"

**Short answer:** The IR + Adapter pattern is perfectly positioned for this. You compile once, optimize at compile-time, then execute with batching.

---

## Your Architecture: Three Layers

```
┌──────────────────────────────────────────────────────────────┐
│                      FABRIC (Composition)                     │
│  Roles + Domains + Policies → manifest.yaml                  │
└─────────────────────────────────┬──────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────┐
│                    NEXUS (Compilation IR)                     │
│  manifest.yaml → IR → Transforms → LangGraph/AWS/MCP         │
│                                                              │
│  ManifestIR, GraphIR, NodeIR, ToolIR, RouterIR              │
└─────────────────────────────────┬──────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────┐
│                   ARCHITECTURE (Runtime)                      │
│  LangGraph | AWS Step Functions | MCP                        │
│                                                              │
│  Adapter: LangGraph + Postgres checkpointing                │
└──────────────────────────────────────────────────────────────┘
```

**The magic:** Between IR and Adapter execution is where you apply batching + caching optimizations.

---

## Where Batch + Caching Fits: Compilation Pipeline

See full docs for complete implementation details.

## Summary: Do You Have the Abstractions?

| Abstraction | Location | Status | Notes |
|-------------|----------|--------|-------|
| **IR Annotations** | `ir/annotations.py` | ✅ Exists | Add `BatchAnnotation` class (30 LOC) |
| **Transformation Pass** | `ir/passes/` | ✅ Exists | Add `BatchOptimizationPass` (100 LOC) |
| **Adapter Extensions** | `adapters/langgraph/` | ✅ Exists | Extend `LangGraphRuntime` with batch logic (300 LOC) |
| **Factory Pattern** | `ir/factories.py` | ✅ Exists | Can customize tool/router creation |
| **Visitor Pattern** | `ir/visitor.py` | ✅ Exists | Can traverse IR for analysis |
| **Compiler Builder** | `builder.py` | ✅ Exists | Can compose custom compilers |

**Answer: YES. You have all the abstractions.**

The only missing piece is:
1. **BatchAnnotation** (new annotation class)
2. **BatchOptimizationPass** (new pass)
3. **BatchAwareLangGraphRuntime** (extend LangGraph adapter)
4. **Wiring it together** (register pass + use new adapter)
