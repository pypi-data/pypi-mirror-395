---
title: Verification Goals Quick Start
description: Get started with formally verifying properties of IML code using automated reasoning
order: 1
---

# Verification Goals (VG) Quick Start

## Introduction

Verification Goals (VG) allow you to formally verify properties of your IML code using automated reasoning. VGs enable you to prove correctness, find counterexamples, or discover concrete instances that satisfy specific properties.

Use VGs when you need to answer questions like "does this property always hold?", "can I find an input that satisfies this condition?", or "what are the edge cases that violate my assumptions?"

## Core Concepts

### Verification Goal Types

There are two types of verification goals in IML:

1. **`verify`**: Attempts to prove a property holds for all possible inputs. If the property holds, it is proven. If the property is disproven, a counterexample is returned showing inputs that violate the property.

2. **`instance`**: Searches for a concrete example that satisfies a given property. Returns specific input values that make the property true, if such values exist.

### Property Format

Both `verify` and `instance` take a lambda function that represents a logical property:

```iml
verify (fun param1 param2 ... -> boolean_expression)
instance (fun param1 param2 ... -> boolean_expression)
```

The lambda parameters represent the free variables being reasoned about, and the body must be a boolean expression.

Reciprocal Relationship: `verify` and `instance` are reciprocal operations. When `verify` refutes a property, the counterexample it returns is equivalent to what `instance` would find for the negated property.

## Basic Examples

### Example 1: Universal Property with `verify`

```iml
let add (x : int) (y : int) : int = x + y

(* Verify that adding positive numbers gives a positive result *)
verify (fun x y -> x > 0 && y > 0 ==> add x y > 0)
```

**Expected output:** ✅ Proven (property holds for all inputs)

### Example 2: Finding Counterexamples

```iml
let add (x : int) (y : int) : int = x + y

(* This property is false - adding two numbers isn't always >= x *)
verify (fun x y -> add x y >= x)
```

**Expected output:** ❌ Counterexample found
```
x = 0
y = -1
```

This shows that `add 0 (-1) = -1` which is NOT `>= 0`, disproving the property.

### Example 3: Finding Instances

```iml
let add (x : int) (y : int) : int = x + y

(* Find two numbers that sum to 10 *)
instance (fun x y -> add x y = 10)
```

**Expected output:** ✅ Instance found
```
x = 10
y = 0
```

## Common Patterns

### Using Logical Implication (`==>`)

The implication operator `==>` is crucial for stating "if precondition then postcondition" properties:

```iml
let divide (x : int) (y : int) : int = x / y

(* If y is non-zero, then division works as expected *)
verify (fun x y -> y <> 0 ==> divide x y * y = x)
```

Note: This property may not hold due to integer division truncation, which the verifier might catch!

### Verifying Function Relationships

```iml
let max_value (x : int) (y : int) : int =
  if x >= y then x else y

(* Verify max returns a value at least as large as both inputs *)
verify (fun x y ->
  let result = max_value x y in
  result >= x && result >= y)

(* Verify max must equal one of the inputs *)
verify (fun x y ->
  let result = max_value x y in
  result = x || result = y)
```

**Expected output:** ✅ Both properties proven

### Verifying Properties and Finding Edge Cases

```iml
let absolute (x : int) : int =
  if x >= 0 then x else -x

(* Verify: absolute value is always non-negative *)
verify (fun x -> absolute x >= 0)

(* Verify: absolute value is idempotent *)
verify (fun x -> absolute (absolute x) = absolute x)

(* Find a negative number with absolute value 15 *)
instance (fun x -> x < 0 && absolute x = 15)
```

**Expected output:**
- ✅ Both verify goals proven
- ✅ Instance found: `x = -15`
