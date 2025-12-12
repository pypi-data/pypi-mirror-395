---
description: Audit .reference/ directory to ensure all implementation claims match actual source code
argument-hint: ""
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Edit"]
---

# Reference Audit - Bi-Directional Verification

I'm going to audit the .reference/ directory using a **two-way verification process** to ensure documentation matches reality and reality is fully documented.

## PHASE 1: Documentation → Implementation (Forward Verification)

### Step 1.1: Discover Documentation
- Read `.reference/README.md` (ONLY hardcoded path)
- List all documentation files
- Understand each file's purpose from README

### Step 1.2: Categorize Each Document

**Type A: Specification Documentation** (what is X?)
- Technical facts: ports, models, dimensions, counts, names
- Verification: Search/grep for values, verify accuracy

**Type B: Procedural Documentation** (how to do X?)
- Setup guides, deployment workflows, step-by-step procedures
- **Verification: MUST find and read implementation script line-by-line**
  - Discover script location (grep for keywords/prompts from doc)
  - Read main() execution flow completely
  - Compare EVERY step (order, prompts, defaults, outputs)
  - Bi-directional check:
    - Every doc step → exists in script
    - Every script step → exists in doc

### Step 1.3: Verify and Fix
- For Type A: Search for claimed values, verify accuracy, fix errors
- For Type B: Full script comparison, fix ALL discrepancies
  - Wrong step order → fix
  - Missing prompts → add
  - Wrong defaults → fix
  - Wrong output → fix

## PHASE 2: Implementation → Documentation (Reverse Discovery)

**PURPOSE:** Find undocumented or changed implementation that needs documentation.

### Step 2.1: Discover All User-Facing Implementation

**Search for setup/deployment scripts:**
```
glob: scripts/*.py
glob: deploy/**/*.py
grep: "def main" + "if __name__ == '__main__'"
```

**Search for deployment configurations:**
```
glob: docker-compose*.yml
glob: config/*.yaml, config/*.example.yaml
glob: deploy/docker/**
```

**Search for package configuration:**
```
read: pyproject.toml (entry points, scripts, dependencies)
```

**Search for CLI implementation:**
```
glob: src/cli_commands/*.py
grep: @click.command, @click.group
```

**Search for MCP implementation:**
```
glob: src/mcp/*.py
grep: @mcp.tool
```

### Step 2.2: Create Implementation Inventory

List everything discovered:
- All Python scripts with main() functions
- All deployment configurations (dev, test, prod, cloud)
- All CLI command groups
- All MCP tools
- All entry points from pyproject.toml

### Step 2.3: Gap Analysis

**For each implementation found, check:**
- Is it documented in .reference/?
- If yes: Already verified in Phase 1
- If no: FLAG as potentially undocumented

**Create gap report:**

**Undocumented Implementation Found:**
- scripts/new_deployment_method.py - not mentioned in any guide
- docker-compose.dev.yml - not documented in INSTALLATION.md
- New CLI commands - not in CLI_GUIDE.md

**Stale Documentation Found:**
- Doc references scripts/old_thing.py - file doesn't exist
- Doc mentions deployment method X - no implementation found

### Step 2.4: User Decision Points

For each gap found:
- Report: "Found X in implementation, not documented in .reference/"
- Ask: Should this be documented? (don't auto-create docs)
- If stale: Flag for removal/update

## Verification Standards

### ❌ INSUFFICIENT (Don't do this)
- "Grepped for port 54320, found it, declared verified"
- "Checked a few technical specs"
- "Sampled some values"

### ✅ REQUIRED (Do this)
- "Read entire setup.py (1365 lines), found 18 steps, doc has 10 steps, fixed discrepancies"
- "Discovered 3 scripts in scripts/, verified all are documented"
- "Found docker-compose.dev.yml not documented, flagged for review"

## Completion Checklist

**Phase 1 - For each documented topic:**
- [ ] Categorized as Type A or Type B
- [ ] Found implementation (searched, didn't assume path)
- [ ] Verified accuracy
- [ ] Fixed errors

**Phase 1 - For Type B (procedural) docs specifically:**
- [ ] Found implementation script
- [ ] Read main() function completely
- [ ] Listed all script steps
- [ ] Listed all doc steps
- [ ] Compared both directions
- [ ] Fixed all discrepancies (order, prompts, defaults, outputs)

**Phase 2 - Implementation discovery:**
- [ ] Searched for all scripts (glob scripts/*.py, deploy/**/*.py)
- [ ] Searched for all configs (glob docker-compose*, config/*)
- [ ] Searched for CLI commands (grep @click)
- [ ] Searched for MCP tools (grep @mcp.tool)
- [ ] Checked pyproject.toml entry points
- [ ] Created implementation inventory
- [ ] Compared inventory to documentation
- [ ] Flagged gaps (undocumented features, stale docs)

## Final Report Structure

1. **Documentation Verification Results** (Phase 1)
   - Errors found and fixed per file
   - Type B verification details (scripts read, steps compared)

2. **Implementation Discovery Results** (Phase 2)
   - Complete implementation inventory
   - Undocumented features found
   - Stale documentation found
   - Recommendations for user

Starting the bi-directional audit now.
