---
title: Region Decomposition Quick Start
description: Analyze functions by automatically partitioning input space into disjoint regions
order: 1
---

# Region Decomposition Quick Start

## Introduction

Region decomposition analyzes a function by automatically partitioning its input space into disjoint regions. Each region represents a distinct execution path characterized by input constraints and a simplified output expression. This enables exhaustive case enumeration, edge case discovery, and verification of complex decision logic.

Use decomposition when you need to answer "what are ALL the scenarios?" - whether verifying business rules, analyzing state machines, finding hidden edge cases, or generating comprehensive test cases.

## Core Concepts

### Region
A region is one partition of the input space, consisting of:
- Constraints: conditions on inputs (forming a conjunction)
- Invariant: simplified symbolic output expression
- Model: concrete example input satisfying the constraints

### Decomposition Output
The decomposition transforms a function into disjunctive normal form (DNF): `if constraints₁ then invariant₁ else if constraints₂ then invariant₂ ...`

Regions are:
- Disjoint: no input satisfies multiple regions
- Exhaustive: every input belongs to exactly one region (unless using ~assuming)

### State Machine
For functions using pattern matching on types/enums, regions naturally represent state transitions with their conditions.

## Basic Example

```iml
let classify x =
  if x < 0 then "negative"
  else if x = 0 then "zero"
  else "positive"
[@@decomp top ()]
```

Run:
```bash
codelogician-tools eval check-decomp --index 1 file.iml
```

Output: 3 regions
- `x >= 1` → `"positive"`
- `x = 0` → `"zero"`
- `x <= -1` → `"negative"`

## Common Parameters

### Focus on valid inputs

```iml
let is_valid x = x >= 0 && x <= 100

let grade x = ...
[@@decomp top ~assuming:[%id is_valid] ()]
```

Important: `is_valid` must have same parameters as `grade`.

### Keep helpers abstract

```iml
let helper x = x * x + 1

let main x = if x < 0 then helper x else helper x + 10
[@@decomp top ~basis:[[%id helper]] ()]
```

Result: invariants contain `helper x` instead of `x * x + 1`.

### Remove impossible branches

```iml
let process x y = ...
[@@decomp top ~prune:true ()]
```

## Typical Workflow

1. Model problem in IML (refer to [[iml-overview.md]] for IML basics)
2. Check it compiles: `codelogician-tools eval check file.iml`
3. Add `[@@decomp top ()]` for initial decomposition on the function you want to analyze
4. Run: `codelogician-tools eval check-decomp ...` to run decomposition
5. Analyze decomp output
6. Iterate: adjust parameters to analyze different aspects of the problem or fix errors

## When to Use

Ask yourself:
- "What are ALL the ways this behaves?"
- "Have I handled every case?"
- "What are hidden edge cases?"
- "How many distinct scenarios exist?"

If yes → use decomposition.

## Common Errors

Mismatched ~assuming signature:
```iml
(* WRONG *)
let is_valid x = x > 0
let process x y = x + y
[@@decomp top ~assuming:[%id is_valid] ()]  (* Error! *)

(* CORRECT *)
let is_valid x y = x > 0 && y > 0
let process x y = x + y
[@@decomp top ~assuming:[%id is_valid] ()]  (* Works *)
```

Type mismatch:
```iml
(* WRONG - mixing int and real *)
let is_valid score = score >= 0.0  (* if score is int *)

(* CORRECT *)
let is_valid score = score >= 0
```

## `codelogician-tools` CLI

```bash
# Check IML file is valid
codelogician-tools eval check file.iml

# List all decomposition requests
codelogician-tools eval list-decomp file.iml

# Run specific decomposition
codelogician-tools eval check-decomp --index 1 file.iml

# Run all decompositions
codelogician-tools eval check-decomp --check-all file.iml

# Get JSON output for automation
codelogician-tools eval check-decomp --json --check-all file.iml
```


## Next Steps

- Full guide: [region-decomposition.md](region-decomposition.md)
- Strategic guide on when and how to use decomposition: [how-to-use-decomp-for-analysis.md](how-to-use-decomp-for-analysis.md)
- Simple examples: `../sample1_basic/`
- Real problems: `../real_world_examples/`
