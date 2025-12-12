----
title: Multiset Module
description: Multiset Module types and functions
order: 10
----


## `type Multiset.t = ('a, int) Map.t`
- name: t
- type: type
- signature: `type Multiset.t = ('a, int) Map.t`
- doc: The multiset type, implemented as a map from elements to their occurrence counts. Each element is associated with an integer representing how many times it appears in the multiset.
- pattern: N\A


## `val empty : ('a, int) Map.t`
- name: empty
- type: function
- signature: `val empty : ('a, int) Map.t`
- doc: Creates an empty multiset where all possible elements implicitly have a count of 0. This serves as the starting point for building multisets.
- pattern: Initializing a new multiset before adding elements, similar to creating an empty array or list in other languages


## `val add : 'a -> ('a, int) Map.t -> ('a, int) Map.t`
- name: add
- type: function
- signature: `val add : 'a -> ('a, int) Map.t -> ('a, int) Map.t`
- doc: Adds one occurrence of element [x] to multiset [m] by retrieving its current count, incrementing it by 1, and storing the new count. This maintains the multiset property of tracking multiple occurrences.
- pattern: Incrementing counters for elements, like counting word frequencies or adding items to a shopping cart


## `val find : 'a -> ('a, int) Map.t -> int`
- name: find
- type: function
- signature: `val find : 'a -> ('a, int) Map.t -> int`
- doc: Retrieves the number of occurrences of element [x] in multiset [m]. This is an alias for Map.get that returns the count directly.
- pattern: Querying how many times an element appears, such as checking inventory levels or word frequencies


## `val mem : 'a -> ('a, int) Map.t -> bool`
- name: mem
- type: function
- signature: `val mem : 'a -> ('a, int) Map.t -> bool`
- doc: Tests if element [x] exists in multiset [m] by checking if its occurrence count is greater than 0. This distinguishes between elements that are present (count > 0) and absent (count = 0).
- pattern: Testing if an element exists at least once in the collection, like checking if an item is in stock


## `val remove : 'a -> ('a, int) Map.t -> ('a, int) Map.t`
- name: remove
- type: function
- signature: `val remove : 'a -> ('a, int) Map.t -> ('a, int) Map.t`
- doc: Removes one occurrence of element [x] from multiset [m] by decreasing its count by 1, ensuring the count never goes below 0. This maintains the invariant that counts are always non-negative.
- pattern: Decreasing element counts one at a time, such as removing items from a shopping cart or consuming inventory


## `val of_list : 'a list -> ('a, int) Map.t`
- name: of_list
- type: function
- signature: `val of_list : 'a list -> ('a, int) Map.t`
- doc: Converts a list [l] into a multiset by recursively processing each element. It starts with an empty multiset and adds each element from the list in sequence, building up the occurrence counts.
- pattern: Converting sequences or collections from other data structures into counted form, like building a frequency table from a list of events


