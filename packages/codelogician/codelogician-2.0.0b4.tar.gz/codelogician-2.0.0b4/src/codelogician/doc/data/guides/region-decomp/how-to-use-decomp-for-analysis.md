---
title: Using Decomposition for Analysis
description: Strategic guide on when and how to use region decomposition effectively
order: 3
---

## When to Use Decomposition

Region decomposition is a **program analysis technique** that automatically partitions a function's input space into disjoint regions. But when should you actually use it? And how should you think about applying it to your problems?

This guide helps you recognize opportunities for decomposition and develop intuition for using it effectively.

## The Core Question: "What are ALL the scenarios?"

Region decomposition shines when you ask questions like:
- "What are **ALL** the ways this function behaves?"
- "Have I handled **every possible case**?"
- "What combinations of inputs lead to **each outcome**?"
- "Are there **hidden edge cases** I'm missing?"

If you find yourself trying to enumerate cases manually, you're probably looking at a decomposition problem.

## Five Primary Use Cases

### 1. Exhaustive Scenario Enumeration

**When to use**: You need to enumerate all possible behaviors or outcomes.

**Example thought process**:
```
"I have a pricing function with volume discounts, loyalty tiers,
seasonal sales, and a maximum cap. How many distinct pricing
scenarios actually exist?"

Manual approach: Try to list combinations... get to 10-15...
probably missing some...

Decomposition: Reveals 20+ regions automatically, each with
concrete examples.
```

**Real example**: `complex_discount.iml`
```iml
let calculate_final_price base_price quantity tier is_sale_season = ...
[@@decomp top ~basis:[[%id volume_discount]; [%id loyalty_discount]] ()]
```

**Output shows**:
- 4 distinct regions with different discount formulas
- Exactly which combinations hit the 40% cap
- Edge case: base_price < 50 → no discounts apply

**Thinking framework**:
- **Triggers**: "How many different ways...?", "What are all the cases where...?"
- **Benefit**: Get complete enumeration without manual case-by-case analysis
- **Key insight**: Each region's `model_str` is a concrete test case

### 2. Verification of Complex Decision Logic

**When to use**: You have nested conditionals with multiple interacting criteria and want to verify correctness.

**Example thought process**:
```
"I have loan approval logic with credit score, debt ratio,
employment, and down payment. If credit says 'approve' but
debt ratio says 'reject', what happens? Are there contradictions?"

Manual approach: Draw decision tree, trace through logic...
easy to miss interactions...

Decomposition: Shows ALL decision paths, reveals conflicts.
```

**Real example**: `loan_approval.iml`
```iml
let evaluate_loan credit_score debt_ratio employment_years
                  down_payment_pct is_existing_perfect_customer = ...
[@@decomp top ~prune:true ()]
```

**Output shows**:
- 15+ regions for different approval scenarios
- Exactly which combinations → Approved vs ManualReview vs Rejected
- Key insight: "existing perfect customer" overrides some rules but not others
- No contradictory regions (pruning worked!)

**Thinking framework**:
- **Triggers**: "Does this logic have contradictions?", "What happens when rule A conflicts with rule B?"
- **Benefit**: See ALL decision paths, verify no gaps or conflicts
- **Key technique**: Use `~prune:true` to eliminate impossible combinations
- **Analysis strategy**: Count regions by `invariant_str` to see outcome distribution

### 3. State Machine Analysis

**When to use**: You have complex state transitions with multiple conditions.

**Example thought process**:
```
"My order system has 6 states and transitions based on payment,
inventory, time, and customer actions. From Confirmed state,
what are ALL the possible next states? Can we reach a stuck state?"

Manual approach: Draw state diagram... gets messy with conditions...

Decomposition: Enumerate all valid transitions from each state.
```

**Real example**: `order_state_machine.iml`
```iml
let next_order_state current_state payment inventory
                     hours_elapsed customer_action =
  match current_state with
  | Pending -> ...
  | Confirmed -> ...
  ...
[@@decomp top ()]
```

**Output shows**:
- 20+ regions representing all valid state transitions
- From Confirmed: can go to Cancelled, Pending, Shipped, or stay Confirmed
- Edge case revealed: Confirmed → Pending when inventory becomes OutOfStock
- All terminal states identified (Refunded always stays Refunded)

**Thinking framework**:
- **Triggers**: "What are all possible state transitions?", "Can we reach X from Y?"
- **Benefit**: Complete state machine coverage, find unreachable states
- **Key technique**: Use `~assuming` to focus on transitions from specific states
- **Analysis strategy**: Group regions by `current_state` in constraints

### 4. Finding Hidden Edge Cases

**When to use**: You suspect there are edge cases but can't enumerate them all.

**Example thought process**:
```
"I've written access control logic. I think I've covered all cases,
but what if I missed something? Can a Guest ever access
Confidential data?"

Manual approach: Try to think of edge cases... test a few...

Decomposition: Automatically reveals ALL access scenarios.
```

**Real example**: `access_control.iml`
```iml
let can_access role resource is_owner = ...
[@@decomp top ()]
```

**Output reveals**:
- 12+ regions for different access scenarios
- Edge case: User + Confidential + is_owner = "granted" (owner exception)
- Verification: No region where Guest + Confidential = "granted" ✓
- Surprising: Manager cannot access Secret resources even as owner

**Thinking framework**:
- **Triggers**: "What edge cases am I missing?", "Is there a way to bypass this check?"
- **Benefit**: Reveals unexpected combinations automatically
- **Analysis strategy**: Look for regions with surprising invariants
- **Verification**: Assert properties by checking no regions violate them

### 5. Test Case Generation

**When to use**: You need comprehensive test coverage for complex logic.

**Example thought process**:
```
"I need to test my medical dosage calculator. What test cases
ensure I've covered all age groups, weights, and medical conditions?"

Manual approach: Write tests based on intuition... probably miss combinations...

Decomposition: Each region provides a concrete test case.
```

**Real example**: `medical_dosage.iml`
```iml
let calculate_dosage age weight_kg has_kidney_issues = ...
[@@decomp top ~basis:[[%id calculate_adult_dosage]] ()]
```

**Output provides**:
- 10+ regions covering all dosage scenarios
- Each `model_str` is a test input: `{age: 1, weight_kg: 10, has_kidney_issues: false}`
- Each `model_eval_str` is expected output: `10`
- Edge cases included: `age: 0`, negative inputs, boundary values

**Thinking framework**:
- **Triggers**: "What test cases cover all scenarios?", "How do I know I've tested everything?"
- **Benefit**: Automatic test case generation with expected outputs
- **Key technique**: Extract (model_str, model_eval_str) pairs as (input, expected) tests
- **Coverage**: Each region represents a distinct equivalence class


## Practical Patterns

### Pattern 1: Validating Preconditions

Use `~assuming` when a function operates under specific input constraints:

```iml
let is_positive x = x > 0

let safe_inverse x =
  1.0 /. Real.of_int x
[@@decomp top ~assuming:[%id is_positive] ()]
```

Analysis focuses only on positive inputs, avoiding division-by-zero scenarios.

### Pattern 2: Modular Analysis

Use `~basis` to analyze function structure while keeping helper functions abstract:

```iml
let helper x y = (* complex logic *)

let main a b c =
  if a > b then
    helper a c
  else
    helper b c
[@@decomp top ~basis:[[%id helper]] ()]
```

This separates control flow analysis from helper implementation details.

### Pattern 3: Combining Parameters

Multiple parameters can be combined for comprehensive analysis:

```iml
let is_valid x y = x >= 0 && y >= 0

let my_func x y =
  if x + y > 100 then "high"
  else "low"
[@@decomp top ~assuming:[%id is_valid] ~prune:true ~ctx_simp:true ()]
```

This restricts to valid inputs, removes infeasible branches, and simplifies constraints.



## Typical Workflow

1. Model the problem in IML
   - Define types, functions, and logic
   - Use pure functions (no side effects)
   - Refer to iml-docs for IML basics

2. Validate with eval check
   - Ensure IML is syntactically and semantically valid
   ```bash
   codelogician-tools eval check file.iml
   ```

3. Add decomposition requests based on analysis goals
   - Start with basic `[@@decomp top ()]`
   - Choose parameters based on analysis goals

4. Run and analyze
   ```bash
   # List all decompositions
   codelogician-tools eval list-decomp file.iml

   # Check specific decomposition
   codelogician-tools eval check-decomp --index 1 file.iml

   # Check all decompositions
   codelogician-tools eval check-decomp --check-all file.iml

   # Get JSON output for programmatic analysis
   # Some decomp can be long to run, so sometimes it's better to save the output for later analysis (eg using jq)
   codelogician-tools eval check-decomp --json --index 1 file.iml
   ```

5. Iterate
   - Fix issues in code and re-run decomposition
   - Adjust decomp arguments eg. ~basis or ~assuming according to the analysis. Try different parameters for alternative views
   - Analyze decomp outputs and re-evaluate analysis goals.
  

### JSON Output for Programmatic Analysis

```bash
codelogician-tools eval check-decomp --json --check-all file.iml > output.json
```

## Working with codelogician-tools

### Basic Commands

```bash
# List all decomposition requests
codelogician-tools eval list-decomp file.iml

# Check specific decomposition by index
codelogician-tools eval check-decomp --index 1 file.iml

# Check all decompositions
codelogician-tools eval check-decomp --check-all file.iml

# JSON output
codelogician-tools eval check-decomp --json --index 1 file.iml
```

`NotImplementedError: Composition operators not supported`:
- Don't use `|>>`, `<<`, `<|<`, `~|`
- Use parameter form: `~prune:true` instead of `|>> prune`

## Quick Reference

| Feature | Syntax | Purpose |
|---------|--------|---------|
| Basic decomposition | `top ()` | Partition function into regions |
| Add precondition | `top ~assuming:[%id func] ()` | Only analyze valid inputs |
| Keep function symbolic | `top ~basis:[[%id func]] ()` | Don't expand certain functions |
| Prune infeasible | `top ~prune:true ()` | Remove unsatisfiable regions |
| Enable simplification | `top ~ctx_simp:true ()` | Apply contextual rewrites |
| Custom rules | `top ~rule_specs:[[%id rule]] ()` | Use algebraic rewrite rules |
