----
title: Int Module
description: Int Module types and functions
order: 2
----


## `type t = int`
- name: t
- type: type
- signature: `type t = int`
- doc: Integer type using arbitrary precision integers (Z.t from Zarith)
- pattern: N\A


## `val mod_zero_prod : int -> int -> int -> bool`
- name: mod_zero_prod
- type: axiom
- signature: `val mod_zero_prod : int -> int -> int -> bool`
- doc: N\A
- pattern: N\A


## `val mod_sub_id : int -> int -> bool`
- name: mod_sub_id
- type: axiom
- signature: `val mod_sub_id : int -> int -> bool`
- doc: N\A
- pattern: N\A


## `val (/) : int -> int -> int`
- name: /
- type: function
- signature: `val (/) : int -> int -> int`
- doc: Division operator for integers
- pattern: Integer division with truncation toward zero


## `val (mod) : int -> int -> int`
- name: mod
- type: function
- signature: `val (mod) : int -> int -> int`
- doc: Modulo operator for integers
- pattern: Computing remainders and wrapping values


## `val (<) : int -> int -> bool`
- name: <
- type: function
- signature: `val (<) : int -> int -> bool`
- doc: Less than comparison operator
- pattern: Numeric ordering comparison


## `val (+) : int -> int -> int`
- name: +
- type: function
- signature: `val (+) : int -> int -> int`
- doc: Addition operator for integers
- pattern: Basic arithmetic addition


## `val (-) : int -> int -> int`
- name: -
- type: function
- signature: `val (-) : int -> int -> int`
- doc: Subtraction operator for integers
- pattern: Basic arithmetic subtraction


## `val (~-) : int -> int`
- name: ~-
- type: function
- signature: `val (~-) : int -> int`
- doc: Unary negation operator for integers
- pattern: Negating a number


## `val (*) : int -> int -> int`
- name: *
- type: function
- signature: `val (*) : int -> int -> int`
- doc: Multiplication operator for integers
- pattern: Basic arithmetic multiplication


## `val (<=) : int -> int -> bool`
- name: <=
- type: function
- signature: `val (<=) : int -> int -> bool`
- doc: Less than or equal comparison operator
- pattern: Numeric ordering and equality comparison


## `val (>) : int -> int -> bool`
- name: >
- type: function
- signature: `val (>) : int -> int -> bool`
- doc: Greater than comparison operator
- pattern: Numeric ordering comparison


## `val (>=) : int -> int -> bool`
- name: >=
- type: function
- signature: `val (>=) : int -> int -> bool`
- doc: Greater than or equal comparison operator
- pattern: Numeric ordering and equality comparison


## `val min : int -> int -> int`
- name: min
- type: function
- signature: `val min : int -> int -> int`
- doc: Returns the minimum of two integers
- pattern: Finding smaller of two values


## `val max : int -> int -> int`
- name: max
- type: function
- signature: `val max : int -> int -> int`
- doc: Returns the maximum of two integers
- pattern: Finding larger of two values


## `val abs : int -> int`
- name: abs
- type: function
- signature: `val abs : int -> int`
- doc: Returns absolute value of an integer
- pattern: Getting magnitude of a number


## `val to_string : int -> string`
- name: to_string
- type: function
- signature: `val to_string : int -> string`
- doc: Converts non-negative integer to string representation
- pattern: String formatting and display of numbers


## `val compare : int -> int -> int`
- name: compare
- type: function
- signature: `val compare : int -> int -> int`
- doc: Returns -1 if x < y, 0 if x = y, 1 if x > y
- pattern: Three-way comparison for sorting and ordering


## `val equal : 'a -> 'a -> bool`
- name: equal
- type: function
- signature: `val equal : 'a -> 'a -> bool`
- doc: Tests equality of two integers
- pattern: Value equality comparison


## `val pow : int -> int -> int`
- name: pow
- type: function
- signature: `val pow : int -> int -> int`
- doc: Computes x raised to power n
- pattern: Exponential calculations


