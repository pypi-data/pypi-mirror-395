----
title: String Module
description: String Module types and functions
order: 7
----


## `type String.t = string`
- name: t
- type: type
- signature: `type String.t = string`
- doc: These strings correspond to OCaml native strings, and do not have a particular unicode encoding. Rather, they should be seen as sequences of bytes, and it is also this way that Imandra considers them.
- pattern: N\A


## `val empty : string`
- name: empty
- type: function
- signature: `val empty : string`
- doc: Returns an empty string
- pattern: Initializing an empty string, like "" in other languages


## `val length : String.t -> int`
- name: length
- type: function
- signature: `val length : String.t -> int`
- doc: Length of the string, i.e. its number of bytes
- pattern: Getting string length, similar to .length or len() in other languages


## `val append : String.t -> String.t -> String.t`
- name: append
- type: function
- signature: `val append : String.t -> String.t -> String.t`
- doc: String concatenation
- pattern: Joining two strings together, like + operator or concat() in other languages


## `val concat : string -> String.t list -> string`
- name: concat
- type: function
- signature: `val concat : string -> String.t list -> string`
- doc: [concat sep l] concatenates strings in [l] with [sep] inserted between each element. - [concat sep [] = ""]
- [concat sep [x] = x]
- [concat sep [x;y] = x ^ sep ^ y]
- [concat sep (x :: tail) = x ^ sep ^ concat sep tail]
- pattern: Joining array/list of strings with separator, like join() or String.join() in other languages


## `val prefix : String.t -> String.t -> bool`
- name: prefix
- type: function
- signature: `val prefix : String.t -> String.t -> bool`
- doc: [prefix a b] returns [true] iff [a] is a prefix of [b] (or if [a=b])
- pattern: Checking if string starts with another string, like startsWith() in other languages


## `val suffix : String.t -> String.t -> bool`
- name: suffix
- type: function
- signature: `val suffix : String.t -> String.t -> bool`
- doc: [suffix a b] returns [true] iff [a] is a suffix of [b] (or if [a=b])
- pattern: Checking if string ends with another string, like endsWith() in other languages


## `val contains : String.t -> String.t -> bool`
- name: contains
- type: function
- signature: `val contains : String.t -> String.t -> bool`
- doc: [String.contains s1 s2] tests if [s2] appears as a substring within [s1]
- pattern: Checking if string contains substring, like includes() or contains() in other languages


## `val unsafe_sub : String.t -> int -> int -> String.t`
- name: unsafe_sub
- type: function
- signature: `val unsafe_sub : String.t -> int -> int -> String.t`
- doc: [String.unsafe_sub s pos len] extracts substring of [s] starting at [pos] of length [len]. No bounds checking - use [String.sub] for safe substring extraction
- pattern: Low-level substring extraction without bounds checking, like internal substring operations


## `val sub : string -> int -> int -> String.t option`
- name: sub
- type: function
- signature: `val sub : string -> int -> int -> String.t option`
- doc: [String.sub s i len] returns the string [s[i], s[i+1],…,s[i+len-1]].
- pattern: Safe substring extraction with bounds checking, like substring() in other languages


## `val of_int : int -> string`
- name: of_int
- type: function
- signature: `val of_int : int -> string`
- doc: String representation of an integer
- pattern: Converting integer to string, like toString() or str() in other languages


## `val unsafe_to_nat : String.t -> int`
- name: unsafe_to_nat
- type: function
- signature: `val unsafe_to_nat : String.t -> int`
- doc: [String.unsafe_to_nat s] converts string [s] to natural number without validation. Use [String.to_nat] for safe conversion
- pattern: Low-level string to number conversion without validation


## `val to_nat : string -> int option`
- name: to_nat
- type: function
- signature: `val to_nat : string -> int option`
- doc: Parse a string into a nonnegative number, or return [None]
- pattern: Safe conversion of string to natural number, like parseInt() with validation


## `val is_nat : string -> bool`
- name: is_nat
- type: function
- signature: `val is_nat : string -> bool`
- doc: [String.is_nat s] tests if string [s] represents a valid natural number
- pattern: Validating if string represents non-negative integer, like input validation


## `val is_int : string -> bool`
- name: is_int
- type: function
- signature: `val is_int : string -> bool`
- doc: [String.is_int s] tests if string [s] represents a valid integer
- pattern: Validating if string represents any integer (positive/negative), like input validation


## `val unsafe_to_int : string -> int`
- name: unsafe_to_int
- type: function
- signature: `val unsafe_to_int : string -> int`
- doc: [String.unsafe_to_int s] converts string [s] to integer without validation. Use [String.to_int] for safe conversion
- pattern: Low-level string to integer conversion without validation


## `val to_int : string -> int option`
- name: to_int
- type: function
- signature: `val to_int : string -> int option`
- doc: [String.to_int s] safely converts string [s] to integer. Returns None if [s] is not a valid integer
- pattern: Safe conversion of string to integer with validation, like parseInt() with error handling


