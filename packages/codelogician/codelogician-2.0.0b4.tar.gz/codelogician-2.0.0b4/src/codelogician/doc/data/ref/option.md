----
title: Option Module
description: Option Module types and functions
order: 8
----


## `type 'a t = 'a option`
- name: t
- type: type
- signature: `type 'a t = 'a option`
- doc: The option type representing optional values. Can be either [None] representing absence of a value, or [Some x] containing a value [x] of type ['a].
- pattern: N\A


## `val map : ('a -> 'b) -> 'a option -> 'b option`
- name: map
- type: function
- signature: `val map : ('a -> 'b) -> 'a option -> 'b option`
- doc: Transforms an optional value by applying function [f] to the contained value. If [x] is [None], returns [None]. If [x] is [Some v], returns [Some (f v)]. This allows transforming the value while preserving the optional structure.
- pattern: Transforming optional values without having to explicitly handle the None case


## `val map_or : default:'a -> ('b -> 'a) -> 'b option -> 'a`
- name: map_or
- type: function
- signature: `val map_or : default:'a -> ('b -> 'a) -> 'b option -> 'a`
- doc: Transforms an optional value into a definite value. If [x] is [Some v], applies [f] to [v]. If [x] is [None], returns the [default] value. This ensures a value is always returned, handling the None case with a default.
- pattern: Converting optional values to non-optional with a fallback value


## `val is_some : 'a option -> bool`
- name: is_some
- type: function
- signature: `val is_some : 'a option -> bool`
- doc: Checks if an option contains a value. Returns [true] if [x] is [Some _], [false] if [x] is [None]. Useful for checking presence of optional values without extracting them.
- pattern: Testing if an optional value is present before attempting to use it


## `val is_none : 'a option -> bool`
- name: is_none
- type: function
- signature: `val is_none : 'a option -> bool`
- doc: Checks if an option is empty. Returns [true] if [x] is [None], [false] if [x] is [Some _]. Complement of [Option.is_some].
- pattern: Testing if an optional value is absent/null/undefined


## `val return : 'a -> 'a option`
- name: return
- type: function
- signature: `val return : 'a -> 'a option`
- doc: Wraps a value in [Some] constructor. This is the fundamental way to create an optional value containing something. Always returns [Some x] for any input [x].
- pattern: Converting regular values into optional values for optional-aware functions


## `val (>|=) : 'a option -> ('a -> 'b) -> 'b option`
- name: >|=
- type: function
- signature: `val (>|=) : 'a option -> ('a -> 'b) -> 'b option`
- doc: An infix operator version of [Option.map]. Allows writing [x >|= f] instead of [Option.map f x] for more natural composition syntax.
- pattern: Chaining transformations on optional values in a pipeline style


## `val flat_map : ('a -> 'b option) -> 'a option -> 'b option`
- name: flat_map
- type: function
- signature: `val flat_map : ('a -> 'b option) -> 'a option -> 'b option`
- doc: Applies a function that returns an option to an optional value. If [x] is [None], returns [None]. If [x] is [Some v], returns [f v]. Used for composing operations that may each produce optional results.
- pattern: Chaining multiple operations that each might fail/return nothing


## `val (>>=) : 'a option -> ('a -> 'b option) -> 'b option`
- name: >>=
- type: function
- signature: `val (>>=) : 'a option -> ('a -> 'b option) -> 'b option`
- doc: An infix operator version of [Option.flat_map]. Allows writing [x >>= f] instead of [Option.flat_map f x]. Standard monadic bind operator for options.
- pattern: Chaining optional computations in a pipeline style


## `val or_ : 'a option -> 'a option -> 'a option`
- name: or_
- type: function
- signature: `val or_ : 'a option -> 'a option -> 'a option`
- doc: Provides a fallback option. Returns [a] if it contains a value, otherwise returns [b]. Useful for providing default optional values.
- pattern: Providing fallback values when the primary optional value is None


## `val (<+>) : 'a option -> 'a option -> 'a option`
- name: <+>
- type: function
- signature: `val (<+>) : 'a option -> 'a option -> 'a option`
- doc: An infix operator version of [Option.or_]. Allows writing [a <+> b] instead of [Option.or_ a b] for more natural fallback syntax.
- pattern: Chaining multiple fallback options in order of preference


## `val exists : ('a -> bool) -> 'a option -> bool`
- name: exists
- type: function
- signature: `val exists : ('a -> bool) -> 'a option -> bool`
- doc: Tests if the value in an option satisfies a predicate. Returns [false] if [x] is [None], otherwise returns [p v] where [v] is the contained value. Similar to [List.exists] but for a single optional value.
- pattern: Testing properties of optional values without explicit None handling


## `val for_all : ('a -> bool) -> 'a option -> bool`
- name: for_all
- type: function
- signature: `val for_all : ('a -> bool) -> 'a option -> bool`
- doc: Tests if the value in an option satisfies a predicate. Returns [true] if [x] is [None], otherwise returns [p v] where [v] is the contained value. Similar to [List.for_all] but for a single optional value.
- pattern: Validating properties of optional values with None considered valid


## `val get_or : default:'a -> 'a option -> 'a`
- name: get_or
- type: function
- signature: `val get_or : default:'a -> 'a option -> 'a`
- doc: Safely extracts the value from an option with a fallback. Returns the value contained in [x] if present, otherwise returns the [default] value. Ensures a value is always returned without risk of exceptions.
- pattern: Safely extracting values from optionals with a default value


## `val fold : ('a -> 'b -> 'a) -> 'a -> 'b option -> 'a`
- name: fold
- type: function
- signature: `val fold : ('a -> 'b -> 'a) -> 'a -> 'b option -> 'a`
- doc: Reduces an optional value using an accumulator. If [x] is [None], returns [acc] unchanged. If [x] is [Some v], returns [f acc v]. Similar to [List.fold_left] but for a single optional value.
- pattern: Accumulating/reducing optional values into a single result


## `val (<$>) : ('a -> 'b) -> 'a option -> 'b option`
- name: <$>
- type: function
- signature: `val (<$>) : ('a -> 'b) -> 'a option -> 'b option`
- doc: An infix operator alias for [Option.map f x]. Provides applicative functor syntax for mapping over options.
- pattern: Applying functions to optional values in a functional style


## `val monoid_product : 'a option -> 'b option -> ('a * 'b) option`
- name: monoid_product
- type: function
- signature: `val monoid_product : 'a option -> 'b option -> ('a * 'b) option`
- doc: Combines two options into a tuple option. Returns [Some (x,y)] if both inputs contain values, [None] if either is [None]. Used for combining independent optional computations.
- pattern: Combining multiple optional values that all must be present


## `val let+ : 'a option -> ('a -> 'b) -> 'b option`
- name: let+
- type: function
- signature: `val let+ : 'a option -> ('a -> 'b) -> 'b option`
- doc: A binding operator alias for [Option.>|=]. Provides syntactic sugar for mapping over options in let-binding syntax.
- pattern: Transforming optional values in a let-binding style


## `val and+ : 'a option -> 'b option -> ('a * 'b) option`
- name: and+
- type: function
- signature: `val and+ : 'a option -> 'b option -> ('a * 'b) option`
- doc: A binding operator alias for [Option.monoid_product]. Provides syntactic sugar for combining options in let-binding syntax.
- pattern: Combining multiple optional values in a let-binding style


## `val let* : 'a option -> ('a -> 'b option) -> 'b option`
- name: let*
- type: function
- signature: `val let* : 'a option -> ('a -> 'b option) -> 'b option`
- doc: A binding operator alias for [Option.>>=]. Provides monadic let-binding syntax for sequencing optional computations.
- pattern: Chaining optional computations in a let-binding style


## `val and* : 'a option -> 'b option -> ('a * 'b) option`
- name: and*
- type: function
- signature: `val and* : 'a option -> 'b option -> ('a * 'b) option`
- doc: A binding operator alias for [Option.monoid_product]. Alternative syntax for combining options in monadic let-binding style.
- pattern: Combining multiple optional values in a monadic let-binding style


