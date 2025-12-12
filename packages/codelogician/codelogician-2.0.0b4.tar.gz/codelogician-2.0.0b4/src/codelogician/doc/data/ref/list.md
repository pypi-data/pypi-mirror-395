----
title: List Module
description: List Module types and functions
order: 3
----


## `val append_to_nil : 'a list -> bool`
- name: append_to_nil
- type: theorem
- signature: `val append_to_nil : 'a list -> bool`
- doc: Theorem: (List.append x []) = x
- pattern: N\A


## `val append_single : 'a -> 'a list -> 'a list -> bool`
- name: append_single
- type: theorem
- signature: `val append_single : 'a -> 'a list -> 'a list -> bool`
- doc: Theorem: (List.append (List.append y ([x])) z) = (List.append y ((x :: z)))
- pattern: N\A


## `val len_nonnegative : 'a list -> bool`
- name: len_nonnegative
- type: theorem
- signature: `val len_nonnegative : 'a list -> bool`
- doc: Length of a list is non-negative. This useful theorem is installed as a forward-chaining rule.
- pattern: N\A


## `val len_zero_is_empty : 'a list -> bool`
- name: len_zero_is_empty
- type: theorem
- signature: `val len_zero_is_empty : 'a list -> bool`
- doc: A list has length zero iff it is empty. This is a useful rewrite rule for obtaining empty lists.
- pattern: N\A


## `val len_append : 'a list -> 'a list -> bool`
- name: len_append
- type: theorem
- signature: `val len_append : 'a list -> 'a list -> bool`
- doc: The length of (x @ y) is the sum of the lengths of x and y
- pattern: N\A


## `type 'a t = 'a list`
- name: t
- type: type
- signature: `type 'a t = 'a list`
- doc: list
- pattern: N\A


## `val empty : 'a list`
- name: empty
- type: function
- signature: `val empty : 'a list`
- doc: Returns an empty list
- pattern: Creating an empty list, initializing a new list with no elements


## `val is_empty : 'a list -> bool`
- name: is_empty
- type: function
- signature: `val is_empty : 'a list -> bool`
- doc: Tests whether list [l] is empty
- pattern: Checking if a list has no elements


## `val cons : 'a -> 'a list -> 'a list`
- name: cons
- type: function
- signature: `val cons : 'a -> 'a list -> 'a list`
- doc: Prepends [x] to the beginning of [l], returning a new list
- pattern: Adding an element to the front of a list


## `val return : 'a -> 'a list`
- name: return
- type: function
- signature: `val return : 'a -> 'a list`
- doc: Creates a singleton list containing only [x]
- pattern: Creating a single-element list


## `val hd : 'a list -> 'a`
- name: hd
- type: function
- signature: `val hd : 'a list -> 'a`
- doc: Returns the first element of list [l]. Partial function that fails on empty lists. But it is recommended to rely on pattern matching instead
- pattern: Getting first element of list, with no safety check


## `val tl : 'a list -> 'a list`
- name: tl
- type: function
- signature: `val tl : 'a list -> 'a list`
- doc: Returns the list [l] without its first element. Partial function that fails on empty lists. But it is recommended to rely on pattern matching instead
- pattern: Getting all elements except first, with no safety check


## `val head_opt : 'a list -> 'a option`
- name: head_opt
- type: function
- signature: `val head_opt : 'a list -> 'a option`
- doc: Returns [Some x] where [x] is the first element of [l], or [None] if [l] is empty
- pattern: Safely getting first element of list with null check


## `val append : 'a list -> 'a list -> 'a list`
- name: append
- type: function
- signature: `val append : 'a list -> 'a list -> 'a list`
- doc: Returns a list composed of all elements of [l1], followed by all elements of [l2]
- pattern: Concatenating two lists together


## `val rev : 'a list -> 'a list`
- name: rev
- type: function
- signature: `val rev : 'a list -> 'a list`
- doc: Returns a new list with all elements of [l] in reverse order
- pattern: Reversing order of elements in list


## `val length : 'a list -> int`
- name: length
- type: function
- signature: `val length : 'a list -> int`
- doc: Returns the number of elements in list [l]. Linear time
- pattern: Getting number of elements in list


## `val split : ('a * 'b) list -> 'a list * 'b list`
- name: split
- type: function
- signature: `val split : ('a * 'b) list -> 'a list * 'b list`
- doc: Takes a list of pairs and returns a pair of lists
- pattern: Converting list of tuples into tuple of lists


## `val map : ('a -> 'b) -> 'a list -> 'b list`
- name: map
- type: function
- signature: `val map : ('a -> 'b) -> 'a list -> 'b list`
- doc: Applies function [f] to each element of [l] and returns the resulting list.
- pattern: Transforming each element of list using a function


## `val map2 : ('c -> 'a -> 'b) -> 'c list -> 'a list -> ('b list, string) result`
- name: map2
- type: function
- signature: `val map2 : ('c -> 'a -> 'b) -> 'c list -> 'a list -> ('b list, string) result`
- doc: Maps function [f] over pairs of elements from [l1] and [l2]. Returns [Error] if lists have different lengths
- pattern: Combining elements from two lists using a function


## `val for_all : ('a -> bool) -> 'a list -> bool`
- name: for_all
- type: function
- signature: `val for_all : ('a -> bool) -> 'a list -> bool`
- doc: Tests whether all elements of [l] satisfy predicate [f]
- pattern: Testing if condition holds for all elements


## `val exists : ('a -> bool) -> 'a list -> bool`
- name: exists
- type: function
- signature: `val exists : ('a -> bool) -> 'a list -> bool`
- doc: Tests whether there exists an element in [l] that satisfies predicate [f]
- pattern: Testing if condition holds for at least one element


## `val fold_left : ('b -> 'a -> 'b) -> 'b -> 'a list -> 'b`
- name: fold_left
- type: function
- signature: `val fold_left : ('b -> 'a -> 'b) -> 'b -> 'a list -> 'b`
- doc: Folds list [l] from left to right using function [f] and initial accumulator [acc]
- pattern: Reducing list to single value by processing elements left-to-right


## `val fold_right : ('b -> 'a -> 'a) -> 'b list -> 'a -> 'a`
- name: fold_right
- type: function
- signature: `val fold_right : ('b -> 'a -> 'a) -> 'b list -> 'a -> 'a`
- doc: Folds list [l] from right to left using function [f] and initial accumulator [acc]
- pattern: Reducing list to single value by processing elements right-to-left


## `val mapi : (int -> 'b -> 'a) -> 'b list -> 'a list`
- name: mapi
- type: function
- signature: `val mapi : (int -> 'b -> 'a) -> 'b list -> 'a list`
- doc: Maps function [f] over list [l], passing both the element and its index to [f]
- pattern: Transforming elements with access to their position/index


## `val filter : ('a -> bool) -> 'a list -> 'a list`
- name: filter
- type: function
- signature: `val filter : ('a -> bool) -> 'a list -> 'a list`
- doc: Keeps only the elements of [l] that satisfy [f]
- pattern: Filtering elements from a collection based on a condition


## `val filter_map : ('a -> 'b option) -> 'a list -> 'b list`
- name: filter_map
- type: function
- signature: `val filter_map : ('a -> 'b option) -> 'a list -> 'b list`
- doc: Applies [f] to each element of [l]. If [f] returns [Some y], keeps [y] in result list. If [f] returns [None], that element is dropped
- pattern: Combined filtering and transformation of elements, like filter().map() or comprehensions


## `val flat_map : ('b -> 'a list) -> 'b list -> 'a list`
- name: flat_map
- type: function
- signature: `val flat_map : ('b -> 'a list) -> 'b list -> 'a list`
- doc: Applies [f] to each element of [l] and concatenates all resulting lists
- pattern: Mapping elements to lists and flattening results, like flatMap() or SelectMany()


## `val find : ('a -> bool) -> 'a list -> 'a option`
- name: find
- type: function
- signature: `val find : ('a -> bool) -> 'a list -> 'a option`
- doc: Returns [Some x] if [x] is the first element of [l] such that [f x] is true. Otherwise it returns [None]
- pattern: Finding first element matching condition, like find() or First()


## `val mem : 'a -> 'a list -> bool`
- name: mem
- type: function
- signature: `val mem : 'a -> 'a list -> bool`
- doc: Returns [true] iff [x] is an element of [l]
- pattern: Testing if value exists in collection, like includes() or contains()


## `val mem_assoc : 'a -> ('a * 'b) list -> bool`
- name: mem_assoc
- type: function
- signature: `val mem_assoc : 'a -> ('a * 'b) list -> bool`
- doc: Returns [true] if [x] appears as a key in association list [l]
- pattern: Testing if key exists in key-value pairs, like hasKey() or containsKey()


## `val nth : int -> 'a list -> 'a option`
- name: nth
- type: function
- signature: `val nth : int -> 'a list -> 'a option`
- doc: Returns [Some x] where [x] is the nth element of [l], or [None] if list is too short
- pattern: Safe indexed access to collection elements, like get() or ElementAt()


## `val assoc : 'a -> ('a * 'b) list -> 'b option`
- name: assoc
- type: function
- signature: `val assoc : 'a -> ('a * 'b) list -> 'b option`
- doc: Returns [Some v] if [(x,v)] appears in association list [l], [None] otherwise
- pattern: Looking up values by key in key-value pairs, like get() or TryGetValue()


## `val bounded_recons : int -> 'a list -> 'a list`
- name: bounded_recons
- type: function
- signature: `val bounded_recons : int -> 'a list -> 'a list`
- doc: Like [List.take n l], but measured subset is [n] instead of [l]
- pattern: Taking first N elements with focus on count rather than input


## `val take : int -> 'a list -> 'a list`
- name: take
- type: function
- signature: `val take : int -> 'a list -> 'a list`
- doc: Returns a list composed of the first (at most) [n] elements of [l]. If [length l <= n] then it returns [l]
- pattern: Taking first N elements from collection, like take() or slice(0,n)


## `val drop : int -> 'a list -> 'a list`
- name: drop
- type: function
- signature: `val drop : int -> 'a list -> 'a list`
- doc: Returns [l] where the first (at most) [n] elements have been removed. If [length l <= n] then it returns [[]]
- pattern: Skipping first N elements from collection, like skip() or slice(n)


## `val range : int -> int -> int list`
- name: range
- type: function
- signature: `val range : int -> int -> int list`
- doc: Integer range. [List.range i j] is the list [[i; i+1; i+2; …; j-1]]. Returns the empty list if [i >= j]
- pattern: Generating sequence of integers, like range() or Enumerable.Range()


## `val insert_sorted : leq:('a -> 'a -> bool) -> 'a -> 'a list -> 'a list`
- name: insert_sorted
- type: function
- signature: `val insert_sorted : leq:('a -> 'a -> bool) -> 'a -> 'a list -> 'a list`
- doc: Inserts [x] in [l], keeping [l] sorted according to [leq]
- pattern: Inserting element while maintaining sort order


## `val sort : leq:('a -> 'a -> bool) -> 'a list -> 'a list`
- name: sort
- type: function
- signature: `val sort : leq:('a -> 'a -> bool) -> 'a list -> 'a list`
- doc: Sorts list [l] according to [leq] ordering
- pattern: Sorting collection with custom comparison


## `val is_sorted : leq:('a -> 'a -> bool) -> 'a list -> bool`
- name: is_sorted
- type: function
- signature: `val is_sorted : leq:('a -> 'a -> bool) -> 'a list -> bool`
- doc: Checks whether list [l] is sorted according to [leq] ordering
- pattern: Testing if collection is in sorted order


## `val monoid_product : 'a list -> 'b list -> ('a * 'b) list`
- name: monoid_product
- type: function
- signature: `val monoid_product : 'a list -> 'b list -> ('a * 'b) list`
- doc: Returns list of all pairs [(x,y)] where [x] comes from [l1] and [y] from [l2]
- pattern: Cartesian product of two collections


## `val (>|=) : 'a list -> ('a -> 'b) -> 'b list`
- name: >|=
- type: function
- signature: `val (>|=) : 'a list -> ('a -> 'b) -> 'b list`
- doc: Infix operator alias for [List.map]
- pattern: Infix syntax for mapping/transforming elements


## `val (>>=) : 'b list -> ('b -> 'a list) -> 'a list`
- name: >>=
- type: function
- signature: `val (>>=) : 'b list -> ('b -> 'a list) -> 'a list`
- doc: Infix operator alias for [List.flat_map]
- pattern: Infix syntax for flat mapping elements


## `val let+ : 'b list -> ('b -> 'a) -> 'a list`
- name: let+
- type: function
- signature: `val let+ : 'b list -> ('b -> 'a) -> 'a list`
- doc: Alias for [List.>|=]
- pattern: Alternative syntax for mapping in monadic contexts


## `val and+ : 'a list -> 'b list -> ('a * 'b) list`
- name: and+
- type: function
- signature: `val and+ : 'a list -> 'b list -> ('a * 'b) list`
- doc: Alias for [List.monoid_product]
- pattern: Alternative syntax for cartesian product in applicative contexts


## `val let* : 'b list -> ('b -> 'a list) -> 'a list`
- name: let*
- type: function
- signature: `val let* : 'b list -> ('b -> 'a list) -> 'a list`
- doc: Alias for [List.>>=]
- pattern: Alternative syntax for flat mapping in monadic contexts


## `val and* : 'a list -> 'b list -> ('a * 'b) list`
- name: and*
- type: function
- signature: `val and* : 'a list -> 'b list -> ('a * 'b) list`
- doc: Alias for [List.monoid_product]
- pattern: Alternative syntax for cartesian product in applicative contexts


## `val (--) : int -> int -> int list`
- name: --
- type: function
- signature: `val (--) : int -> int -> int list`
- doc: Infix operator alias for [List.range]
- Note: `end` is not included in the generated list of `(start -- end)`.
- Example: `List.(--) 1 3 (* gives [1;2] *)`
- pattern: Infix syntax for integer ranges


