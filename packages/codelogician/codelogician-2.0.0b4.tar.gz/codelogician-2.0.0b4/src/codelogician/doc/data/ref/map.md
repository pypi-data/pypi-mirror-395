----
title: Map Module
description: Map Module types and functions
order: 11
----


## `type Map.t = {| l : ('a * 'b) list; | default : 'b}`
- name: t
- type: type
- signature: `type Map.t = {| l : ('a * 'b) list; | default : 'b}`
- doc: The map type representing a key-value mapping where each key is associated with exactly one value
- pattern: N\A


## `val const : 'b -> ('a, 'b) Map.t`
- name: const
- type: function
- signature: `val const : 'b -> ('a, 'b) Map.t`
- doc: Creates a constant map that maps every key to the same value [v]
- pattern: Initializing maps with a default value for all possible keys, useful for creating maps with a uniform base value


## `val add' : ('a, 'b) Map.t -> 'a -> 'b -> ('a, 'b) Map.t`
- name: add'
- type: function
- signature: `val add' : ('a, 'b) Map.t -> 'a -> 'b -> ('a, 'b) Map.t`
- doc: Adds or updates the binding from key [k] to value [v] in map [m]
- pattern: Adding or updating key-value pairs in a map with map-first argument order


## `val add : 'a -> 'b -> ('a, 'b) Map.t -> ('a, 'b) Map.t`
- name: add
- type: function
- signature: `val add : 'a -> 'b -> ('a, 'b) Map.t -> ('a, 'b) Map.t`
- doc: Adds or updates the binding from key [k] to value [v] in map [m]
- pattern: Adding or updating key-value pairs in a map with key-first argument order, similar to dictionary updates in other languages


## `val get_default : ('a, 'b) Map.t -> 'b`
- name: get_default
- type: function
- signature: `val get_default : ('a, 'b) Map.t -> 'b`
- doc: Returns the default value associated with map [m]
- pattern: Retrieving the default value used for keys not explicitly set in the map


## `val get' : ('a, 'b) Map.t -> 'a -> 'b`
- name: get'
- type: function
- signature: `val get' : ('a, 'b) Map.t -> 'a -> 'b`
- doc: Retrieves the value associated with key [k] in map [m]
- pattern: Looking up values by key in a map with map-first argument order


## `val get : 'a -> ('a, 'b) Map.t -> 'b`
- name: get
- type: function
- signature: `val get : 'a -> ('a, 'b) Map.t -> 'b`
- doc: Retrieves the value associated with key [k] in map [m]
- pattern: Looking up values by key in a map with key-first argument order, similar to dictionary lookups in other languages


## `val of_list : 'b -> ('a * 'b) list -> ('a, 'b) Map.t`
- name: of_list
- type: function
- signature: `val of_list : 'b -> ('a * 'b) list -> ('a, 'b) Map.t`
- doc: Creates a map from a list [l] of key-value pairs, using [default] as the value for keys not in the list
- pattern: Converting a list of key-value pairs into a map, commonly used when initializing a map from existing data


