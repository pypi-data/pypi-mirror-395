----
title: Result Module
description: Result Module types and functions
order: 5
----


## `type ('a, 'b) t = ('a, 'b) result`
- name: t
- type: type
- signature: `type ('a, 'b) t = ('a, 'b) result`
- doc: The result type represents either success (Ok) or failure (Error) outcomes.
- pattern: N\A


## `val return : 'a -> ('a, 'b) result`
- name: return
- type: function
- signature: `val return : 'a -> ('a, 'b) result`
- doc: wraps a value [x] in an Ok result
- pattern: Converting raw values into success results for validation chains and computation sequences


## `val fail : 'a -> ('b, 'a) result`
- name: fail
- type: function
- signature: `val fail : 'a -> ('b, 'a) result`
- doc: wraps a value [s] in an Error result
- pattern: Converting error information into error results during validation or error handling


## `val map : ('b -> 'c) -> ('b, 'a) result -> ('c, 'a) result`
- name: map
- type: function
- signature: `val map : ('b -> 'c) -> ('b, 'a) result -> ('c, 'a) result`
- doc: applies function [f] to the value inside [e] if it's Ok, otherwise propagates the Error
- pattern: Applying transformations to success values while preserving error state


## `val map_err : ('a -> 'c) -> ('b, 'a) result -> ('b, 'c) result`
- name: map_err
- type: function
- signature: `val map_err : ('a -> 'c) -> ('b, 'a) result -> ('b, 'c) result`
- doc: applies function [f] to the error value if [e] is Error, otherwise propagates the Ok value
- pattern: Converting between error types while preserving success values


## `val get_or : default:'a -> ('a, 'b) result -> 'a`
- name: get_or
- type: function
- signature: `val get_or : default:'a -> ('a, 'b) result -> 'a`
- doc: extracts the Ok value from [e], or returns [default] if [e] is Error
- pattern: Extracting values with fallback for error cases


## `val map_or : default:'a -> ('c -> 'a) -> ('c, 'b) result -> 'a`
- name: map_or
- type: function
- signature: `val map_or : default:'a -> ('c -> 'a) -> ('c, 'b) result -> 'a`
- doc: applies [f] to the Ok value in [e], or returns [default] if [e] is Error
- pattern: Transforming success values with a fallback for error cases


## `val (>|=) : ('b, 'a) result -> ('b -> 'c) -> ('c, 'a) result`
- name: >|=
- type: function
- signature: `val (>|=) : ('b, 'a) result -> ('b -> 'c) -> ('c, 'a) result`
- doc: is an infix operator alias for [Result.map]
- pattern: Infix syntax for transforming success values


## `val flat_map : ('b -> ('c, 'a) result) -> ('b, 'a) result -> ('c, 'a) result`
- name: flat_map
- type: function
- signature: `val flat_map : ('b -> ('c, 'a) result) -> ('b, 'a) result -> ('c, 'a) result`
- doc: applies [f] to the Ok value in [e] to produce a new result, or propagates the Error
- pattern: Chaining operations that can fail


## `val (>>=) : ('b, 'a) result -> ('b -> ('c, 'a) result) -> ('c, 'a) result`
- name: >>=
- type: function
- signature: `val (>>=) : ('b, 'a) result -> ('b -> ('c, 'a) result) -> ('c, 'a) result`
- doc: is an infix operator alias for [Result.flat_map]
- pattern: Infix syntax for chaining fallible operations


## `val fold : ('b -> 'c) -> ('a -> 'c) -> ('b, 'a) result -> 'c`
- name: fold
- type: function
- signature: `val fold : ('b -> 'c) -> ('a -> 'c) -> ('b, 'a) result -> 'c`
- doc: applies [ok] to the value if [x] is Ok, or applies [error] if [x] is Error
- pattern: Converting both success and error cases to a single type


## `val is_ok : ('a, 'b) result -> bool`
- name: is_ok
- type: function
- signature: `val is_ok : ('a, 'b) result -> bool`
- doc: returns true if [x] is Ok, false otherwise
- pattern: Testing if a result represents success


## `val is_error : ('a, 'b) result -> bool`
- name: is_error
- type: function
- signature: `val is_error : ('a, 'b) result -> bool`
- doc: returns true if [x] is Error, false otherwise
- pattern: Testing if a result represents failure


## `val monoid_product : ('a, 'b) result -> ('c, 'b) result -> ('a * 'c, 'b) result`
- name: monoid_product
- type: function
- signature: `val monoid_product : ('a, 'b) result -> ('c, 'b) result -> ('a * 'c, 'b) result`
- doc: combines two results into a tuple if both are Ok, otherwise returns the first Error encountered
- pattern: Combining two independent results into a tuple result


## `val let+ : ('c, 'a) result`
- name: let+
- type: function
- signature: `val let+ : ('c, 'a) result`
- doc: is a binding operator alias for [>|=] (map)
- pattern: Binding syntax for transforming success values


## `val and+ : (('a * 'c), 'b) result`
- name: and+
- type: function
- signature: `val and+ : (('a * 'c), 'b) result`
- doc: is a binding operator alias for [Result.monoid_product]
- pattern: Binding syntax for combining independent results


## `val let* : ('c, 'a) result`
- name: let*
- type: function
- signature: `val let* : ('c, 'a) result`
- doc: is a binding operator alias for [>>=] (flat_map)
- pattern: Binding syntax for chaining fallible operations


## `val and* : (('a * 'c), 'b) result`
- name: and*
- type: function
- signature: `val and* : (('a * 'c), 'b) result`
- doc: is a binding operator alias for [Result.monoid_product]
- pattern: Alternative binding syntax for combining results


