----
title: Real Module
description: Real Module types and functions
order: 6
----


## `type t = real`
- name: t
- type: type
- signature: `type t = real`
- doc: The real number type representing arbitrary precision real numbers
- pattern: Representing exact decimal numbers without floating point imprecision


## `val of_int : int -> real`
- name: of_int
- type: function
- signature: `val of_int : int -> real`
- doc: Converts an integer [i] to a real number
- pattern: Converting integer values to real numbers for exact decimal arithmetic


## `val _to_int_round_down : real -> int`
- name: _to_int_round_down
- type: function
- signature: `val _to_int_round_down : real -> int`
- doc: Converts a real number [r] to an integer by rounding down. Internal helper function.
- pattern: Internal function for floor rounding in integer conversion


## `val to_int : real -> int`
- name: to_int
- type: function
- signature: `val to_int : real -> int`
- doc: Converts a real number [r] to an integer by rounding towards zero
- pattern: Converting real numbers to integers when decimal precision is no longer needed


## `val (+) : real -> real -> real`
- name: +
- type: function
- signature: `val (+) : real -> real -> real`
- doc: Adds two real numbers
- pattern: Performing exact decimal addition without floating point errors


## `val (-) : real -> real -> real`
- name: -
- type: function
- signature: `val (-) : real -> real -> real`
- doc: Subtracts two real numbers
- pattern: Performing exact decimal subtraction without floating point errors


## `val (~-) : real -> real`
- name: ~-
- type: function
- signature: `val (~-) : real -> real`
- doc: Negates a real number
- pattern: Changing the sign of a real number while preserving its magnitude


## `val (*) : real -> real -> real`
- name: *
- type: function
- signature: `val (*) : real -> real -> real`
- doc: Multiplies two real numbers
- pattern: Performing exact decimal multiplication without floating point errors


## `val (/) : real -> real -> real`
- name: /
- type: function
- signature: `val (/) : real -> real -> real`
- doc: Divides two real numbers
- pattern: Performing exact decimal division without floating point errors


## `val (<) : real -> real -> bool`
- name: <
- type: function
- signature: `val (<) : real -> real -> bool`
- doc: Tests if one real number is less than another
- pattern: Comparing real numbers for strict ordering relationships


## `val (<=) : real -> real -> bool`
- name: <=
- type: function
- signature: `val (<=) : real -> real -> bool`
- doc: Tests if one real number is less than or equal to another
- pattern: Comparing real numbers for non-strict ordering relationships


## `val (>) : real -> real -> bool`
- name: >
- type: function
- signature: `val (>) : real -> real -> bool`
- doc: Tests if one real number is greater than another
- pattern: Comparing real numbers for strict ordering relationships


## `val (>=) : real -> real -> bool`
- name: >=
- type: function
- signature: `val (>=) : real -> real -> bool`
- doc: Tests if one real number is greater than or equal to another
- pattern: Comparing real numbers for non-strict ordering relationships


## `val abs : real -> real`
- name: abs
- type: function
- signature: `val abs : real -> real`
- doc: Returns the absolute value of real number [r]
- pattern: Getting the magnitude of a real number regardless of sign


## `val min : real -> real -> real`
- name: min
- type: function
- signature: `val min : real -> real -> real`
- doc: Returns the minimum of two real numbers
- pattern: Finding the smaller of two real numbers in comparisons


## `val max : real -> real -> real`
- name: max
- type: function
- signature: `val max : real -> real -> real`
- doc: Returns the maximum of two real numbers
- pattern: Finding the larger of two real numbers in comparisons


## `val of_float : float -> real`
- name: of_float
- type: function
- signature: `val of_float : float -> real`
- doc: Converts a float [f] to a real number
- pattern: Converting approximate floating point numbers to exact real numbers


## `val pow : real -> int -> real`
- name: pow
- type: function
- signature: `val pow : real -> int -> real`
- doc: Raises real number [base] to integer power [exp]
- pattern: Computing exact integer powers of real numbers


