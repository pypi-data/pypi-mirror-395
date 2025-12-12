----
title: Termination Proofs
description: Termination proof reference
order: 6
----


## Overview

ImandraX requires all recursive functions to be proven terminating for soundness. Non-terminating functions are rejected to maintain logical consistency.

## Core Principles

1. **Every recursive function must terminate** - This ensures the logic remains consistent
2. **ImandraX uses ordinals** - Termination is proven by showing recursive calls decrease along a well-founded ordering
3. **Conservative extensions** - All admitted functions preserve consistency

## Automatic Termination

ImandraX automatically proves termination for:
- Non-recursive functions
- Structural recursion on algebraic data types
- Simple decreasing integer arguments

### Examples that work automatically:

```iml
let rec sum_lst = function
 | [] -> 0
 | x :: xs -> x + sum_lst xs

let rec sum x =
 if x <= 0 then 0
 else x + sum(x-1)
```

## Manual Termination Hints

### Lexicographic Ordering (`@@adm`)

Use when arguments decrease lexicographically (measures up to ω^ω).

**Syntax:** `[@@adm arg1, arg2, ...]`

**Example - Ackermann function:**
```iml
let rec ack m n =
  if m <= 0 then n + 1
  else if n <= 0 then ack (m-1) 1
  else ack (m-1) (ack m (n-1))
  [@@adm m,n]
```

### Custom Measures (`@@measure`)

Use when lexicographic ordering is insufficient. Measures must return `Ordinal.t`.

**Syntax:** `[@@measure measure_fn arg1 arg2 ...]`

**Example - left_pad:**
```iml
let left_pad_measure n xs =
  Ordinal.of_int (n - List.length xs)

let rec left_pad c n xs =
  if List.length xs >= n then xs
  else left_pad c n (c :: xs)
[@@measure left_pad_measure n xs]
```

## Ordinal Module Reference

### Type
```iml
type t = Int of int | Cons of t * int * t
```

### Key Functions

| Function | Signature | Purpose |
|----------|-----------|---------|
| `of_int` | `int -> t` | Convert integer to ordinal |
| `~$` | `int -> t` | Infix for `of_int` |
| `<<` | `t -> t -> bool` | Well-founded ordering relation |
| `plus` / `+` | `t -> t -> t` | Ordinal addition (non-commutative) |
| `pair` | `t -> t -> t` | Create ordinal pair |
| `triple` | `t -> t -> t -> t` | Create ordinal triple |
| `quad` | `t -> t -> t -> t -> t` | Create ordinal quad |
| `of_list` | `t list -> t` | Create ordinal from list |

### Constants
- `zero` - Ordinal 0
- `one` - Ordinal 1
- `omega` - ω
- `omega_omega` - ω^ω

## Decision Tree

```
Is the function recursive?
├─ No → Automatically admitted
└─ Yes → Does it structurally recurse on algebraic datatypes?
    ├─ Yes → Automatically admitted
    └─ No → Does it have simple decreasing integer arguments?
        ├─ Yes → Automatically admitted
        └─ No → Do arguments decrease lexicographically?
            ├─ Yes → Use [@@adm arg1, arg2, ...]
            └─ No → Define custom measure function
                    Use [@@measure fn arg1 arg2 ...]
```

## Common Patterns

### Pattern 1: List length decreasing
```iml
let measure xs = Ordinal.of_int (List.length xs)
```

### Pattern 2: Difference of two values
```iml
let measure n x = Ordinal.of_int (n - x)
```

### Pattern 3: Lexicographic pairs
```iml
[@@adm m, n]  (* m primarily, then n *)
```

## Best Practices

1. **Use minimal measures** - Include only arguments that actually decrease
2. **Prefer automatic admission** - Structure code for structural recursion when possible
3. **Lexicographic before custom** - Try `@@adm` before writing custom measures
4. **Guard conditions matter** - Ensure measure stays non-negative under recursive call guards
