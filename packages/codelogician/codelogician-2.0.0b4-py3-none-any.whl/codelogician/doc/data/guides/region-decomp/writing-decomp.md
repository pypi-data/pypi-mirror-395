---
title: Writing Decomposition Requests
description: Complete syntax guide for writing decomposition annotations with all parameters
order: 2
---

## Writing Decomposition

This doc is about how to write `[@@decomp top ()]`

### Basic Syntax

Attach `[@@decomp top ()]` to a function:

```iml
let classify x =
  if x < 0 then "negative"
  else if x = 0 then "zero"
  else "positive"
[@@decomp top ()]
```

### Type Signature of top

```iml
val top :
  ?assuming:identifier ->
  ?basis:identifier list ->
  ?rule_specs:identifier list ->
  ?prune:bool ->
  ?ctx_simp:bool ->
  unit ->
  m
```

All parameters are optional. The final `unit` parameter requires calling with `()`.

### Parameters

#### ~assuming: Focus on Valid Inputs

Restricts analysis to inputs satisfying a precondition.

```iml
let is_valid_score x = x >= 0 && x <= 100

let grade x =
  if x >= 90 then "A"
  else if x >= 80 then "B"
  else "F"
[@@decomp top ~assuming:[%id is_valid_score] ()]
```

Requirements:
- Assumption function must have identical parameter signature (count, order, names)
- Use `[%id function_name]` syntax

Common error: Mismatched signatures cause `TacticEvalErr`.

#### ~basis: Keep Functions Symbolic

Prevents expansion of specified functions during decomposition.

```iml
let compute_tax amount = amount *. 0.15

let total_price amount discount =
  let base = amount -. discount in
  compute_tax base
[@@decomp top ~basis:[[%id compute_tax]] ()]
```

Result: invariants contain `compute_tax base` instead of expanded `base *. 0.15`.

Use case: analyze control flow structure without implementation details.

Common error: incorrect List Syntax for ~basis

```iml
(* WRONG *)
~basis:[%id func1; %id func2]

(* CORRECT *)
~basis:[[%id func1]; [%id func2]]
```

#### ~prune: Remove Infeasible Regions

Automatically removes regions with unsatisfiable constraints.

```iml
let process x y =
  if x > y then
    if x < y then "impossible"  (* infeasible *)
    else "x greater"
  else "y greater or equal"
[@@decomp top ~prune:true ()]
```

#### ~ctx_simp: Contextual Simplification

Enables value propagation and expression rewriting.

```iml
let compare x y =
  if x <> y then
    if x > y then "x greater"
    else "y greater"
  else "equal"
[@@decomp top ~ctx_simp:true ()]
```

#### ~rule_specs: Custom Rewrite Rules

Applies custom algebraic rules during decomposition.

```iml
let double_rule x = 2 * x = x + x [@@rw] [@@imandra_rule_spec]

let categorize x =
  if 2 * x > 100 then "high"
  else "low"
[@@decomp top ~rule_specs:[[%id double_rule]] ()]
```
