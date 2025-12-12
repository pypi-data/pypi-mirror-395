----
title: Set Module
description: Set Module types and functions
order: 4
----


## `type Set.t = ('a, bool) Map.t`
- name: t
- type: type
- signature: `type Set.t = ('a, bool) Map.t`
- doc: The set type, implemented as a map from elements to boolean values indicating membership
- pattern: N\A


## `val empty : ('a, bool) Map.t`
- name: empty
- type: function
- signature: `val empty : ('a, bool) Map.t`
- doc: Creates an empty set where all elements are mapped to false
- pattern: Initializing a new set before adding elements, similar to creating an empty HashSet or Set in other languages


## `val full : ('a, bool) Map.t`
- name: full
- type: function
- signature: `val full : ('a, bool) Map.t`
- doc: Creates a full set where all elements are mapped to true
- pattern: Creating a universal set containing all possible elements, often used as a starting point for set operations like complement


## `val is_empty : 'a Set.t -> bool`
- name: is_empty
- type: function
- signature: `val is_empty : 'a Set.t -> bool`
- doc: Tests if set [s] is empty by comparing it to the empty set
- pattern: Checking if a collection contains any elements before performing operations, like validating user input or checking search results


## `val is_valid : 'a Set.t -> bool`
- name: is_valid
- type: function
- signature: `val is_valid : 'a Set.t -> bool`
- doc: Checks if set [s] is valid. Always returns true since all sets are valid
- pattern: Validating set integrity, though in this implementation all sets are considered valid by design


## `val mem : 'a -> 'a Set.t -> bool`
- name: mem
- type: function
- signature: `val mem : 'a -> 'a Set.t -> bool`
- doc: Tests if element [x] is a member of set [s]
- pattern: Testing element existence in a collection, like checking if a user ID exists or if a value is allowed


## `val subset : 'a Set.t -> 'a Set.t -> bool`
- name: subset
- type: function
- signature: `val subset : 'a Set.t -> 'a Set.t -> bool`
- doc: Tests if set [s1] is a subset of set [s2]
- pattern: Checking if one collection's elements are fully contained within another, like validating permissions or category hierarchies


## `val add : 'a -> 'a Set.t -> 'a Set.t`
- name: add
- type: function
- signature: `val add : 'a -> 'a Set.t -> 'a Set.t`
- doc: Adds element [x] to set [s]
- pattern: Adding unique elements to a collection, ensuring no duplicates, like building a set of unique identifiers or tags


## `val remove : 'a -> 'a Set.t -> 'a Set.t`
- name: remove
- type: function
- signature: `val remove : 'a -> 'a Set.t -> 'a Set.t`
- doc: Removes element [x] from set [s]
- pattern: Removing elements from a collection while maintaining uniqueness, like removing revoked permissions or deleted items


## `val inter : 'a Set.t -> 'a Set.t -> 'a Set.t`
- name: inter
- type: function
- signature: `val inter : 'a Set.t -> 'a Set.t -> 'a Set.t`
- doc: Computes the intersection of sets [s1] and [s2]
- pattern: Finding common elements between two collections, like identifying shared permissions or matching criteria


## `val union : 'a Set.t -> 'a Set.t -> 'a Set.t`
- name: union
- type: function
- signature: `val union : 'a Set.t -> 'a Set.t -> 'a Set.t`
- doc: Computes the union of sets [s1] and [s2]
- pattern: Combining two collections while eliminating duplicates, like merging user groups or combining search results


## `val complement : 'a Set.t -> 'a Set.t`
- name: complement
- type: function
- signature: `val complement : 'a Set.t -> 'a Set.t`
- doc: Computes the complement of set [s]
- pattern: Finding all elements not in a set, useful for implementing negation or finding excluded items


## `val diff : 'a Set.t -> 'a Set.t -> 'a Set.t`
- name: diff
- type: function
- signature: `val diff : 'a Set.t -> 'a Set.t -> 'a Set.t`
- doc: Computes the difference of sets [s1] and [s2]
- pattern: Finding elements in one collection but not another, like identifying unique permissions or filtering exclusions


## `val of_list : 'a list -> ('a, bool) Map.t`
- name: of_list
- type: function
- signature: `val of_list : 'a list -> ('a, bool) Map.t`
- doc: Creates a set from list [l] by recursively adding each element
- pattern: Converting sequences or arrays to sets while eliminating duplicates, like creating a set of unique values from user input or data import


## `val (++) : 'a Set.t -> 'a Set.t -> 'a Set.t`
- name: ++
- type: function
- signature: `val (++) : 'a Set.t -> 'a Set.t -> 'a Set.t`
- doc: An infix operator alias for [Set.union]
- pattern: Providing a more concise syntax for combining sets, similar to overloaded operators in other languages


## `val (--) : 'a Set.t -> 'a Set.t -> 'a Set.t`
- name: --
- type: function
- signature: `val (--) : 'a Set.t -> 'a Set.t -> 'a Set.t`
- doc: An infix operator alias for [Set.diff]
- pattern: Providing a more concise syntax for set difference, similar to overloaded operators in other languages


