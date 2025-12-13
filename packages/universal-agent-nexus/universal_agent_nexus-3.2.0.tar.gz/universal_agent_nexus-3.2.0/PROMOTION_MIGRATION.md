# Promotion Migration: _lib → universal-agent-nexus@3.1.0

**Status:** In Progress  
**Date:** December 2025

## Modules to Migrate

### ✅ Completed
- [x] `runtime/registry/` - ToolRegistry (created)

### ⏳ In Progress
- [ ] `runtime/runtime_base.py` - Base runtime class (created, needs import fix)
- [ ] `runtime/standard_integration.py` - Standard example class
- [ ] `cache_fabric/` - Complete module (10 files)
- [ ] `output_parsers/` - Complete module (7 files)

## Import Updates Required

### runtime_base.py
- ❌ `from ..tools.universal_agent_tools.observability_helper import ...`
- ✅ `from universal_agent_tools.observability import ...`

### standard_integration.py
- ❌ `from ..cache_fabric.base import ...`
- ✅ `from universal_agent_nexus.cache_fabric.base import ...`
- ❌ `from ..output_parsers import ...`
- ✅ `from universal_agent_nexus.output_parsers import ...`

### cache_fabric modules
- All imports should use `universal_agent_nexus.cache_fabric.*`

### output_parsers modules
- All imports should use `universal_agent_nexus.output_parsers.*`

## Next Steps

1. Copy all cache_fabric files with updated imports
2. Copy all output_parsers files with updated imports
3. Update standard_integration.py with correct imports
4. Update nexus __init__.py to export new modules
5. Update pyproject.toml version to 3.1.0

