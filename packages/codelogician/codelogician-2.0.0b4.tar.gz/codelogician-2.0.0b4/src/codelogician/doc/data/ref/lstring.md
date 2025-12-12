----
title: Lstring Module
description: Lstring Module types and functions
order: 12
----


## `type t = LChar.t list`
- name: t
- type: type
- signature: `type t = LChar.t list`
- doc: A list of logic-mode characters
- pattern: N\A


## `val empty : LChar.t list`
- name: empty
- type: function
- signature: `val empty : LChar.t list`
- doc: Returns an empty string (empty list of characters)
- pattern: Creating an empty string, like "" or empty string literal in other languages


## `val of_list : 'a -> 'a`
- name: of_list
- type: function
- signature: `val of_list : 'a -> 'a`
- doc: Converts a list directly to an LString.t
- pattern: Converting array/list of characters to string, like String.fromCharArray() or similar


## `val length : LChar.t list -> int`
- name: length
- type: function
- signature: `val length : LChar.t list -> int`
- doc: Returns the number of characters in string [s]
- pattern: Getting string length, like .length or len() in other languages


## `val append : LChar.t list -> LChar.t list -> LChar.t list`
- name: append
- type: function
- signature: `val append : LChar.t list -> LChar.t list -> LChar.t list`
- doc: Concatenates strings [s1] and [s2]
- pattern: Joining two strings together, like + operator or concat() in other languages


## `val (^^) : LChar.t list -> LChar.t list -> LChar.t list`
- name: ^^
- type: function
- signature: `val (^^) : LChar.t list -> LChar.t list -> LChar.t list`
- doc: An infix operator alias for LString.append
- pattern: Infix string concatenation, like + or .. operators in other languages


## `val for_all : (LChar.t -> bool) -> LChar.t list -> bool`
- name: for_all
- type: function
- signature: `val for_all : (LChar.t -> bool) -> LChar.t list -> bool`
- doc: Tests if all characters in [s] satisfy predicate [f]
- pattern: Checking if all characters match a condition, like every() or all() in other languages


## `val exists : (LChar.t -> bool) -> LChar.t list -> bool`
- name: exists
- type: function
- signature: `val exists : (LChar.t -> bool) -> LChar.t list -> bool`
- doc: Tests if any character in [s] satisfies predicate [f]
- pattern: Checking if any character matches a condition, like some() or any() in other languages


## `val concat : LChar.t list -> LChar.t list list -> LChar.t list`
- name: concat
- type: function
- signature: `val concat : LChar.t list -> LChar.t list list -> LChar.t list`
- doc: Concatenates all strings in list [l], placing [sep] between each
- pattern: Joining array of strings with separator, like join() or String.join() in other languages


## `val is_printable : LChar.t list -> bool`
- name: is_printable
- type: function
- signature: `val is_printable : LChar.t list -> bool`
- doc: Tests if all characters in [s] are printable
- pattern: Checking if string contains only printable characters, like string validation


## `val sub : LChar.t list -> int -> int -> LChar.t list`
- name: sub
- type: function
- signature: `val sub : LChar.t list -> int -> int -> LChar.t list`
- doc: Extracts substring of [s] starting at position [i] of length [len]
- pattern: Extracting substring, like substring() or slice() in other languages


## `val prefix : LChar.t list -> LChar.t list -> bool`
- name: prefix
- type: function
- signature: `val prefix : LChar.t list -> LChar.t list -> bool`
- doc: Tests if [s1] is a prefix of [s2]
- pattern: Checking if string starts with another string, like startsWith() in other languages


## `val suffix : LChar.t list -> LChar.t list -> bool`
- name: suffix
- type: function
- signature: `val suffix : LChar.t list -> LChar.t list -> bool`
- doc: Tests if [s1] is a suffix of [s2]
- pattern: Checking if string ends with another string, like endsWith() in other languages


## `val contains : LChar.t list -> LChar.t list -> bool`
- name: contains
- type: function
- signature: `val contains : LChar.t list -> LChar.t list -> bool`
- doc: Tests if [s2] appears as a substring within [s1]
- pattern: Checking if string contains substring, like includes() or contains() in other languages


## `val take : int -> LString.t -> LString.t`
- name: take
- type: function
- signature: `val take : int -> LString.t -> LString.t`
- doc: Returns first [n] characters of string [s]. The [LString.t] version of [List.take]
- pattern: Taking first N characters from string, like slice(0,n) or substring(0,n) in other languages


## `val drop : int -> LString.t -> LString.t`
- name: drop
- type: function
- signature: `val drop : int -> LString.t -> LString.t`
- doc: Removes first [n] characters from string [s]. The [LString.t] version of [List.drop]
- pattern: Removing first N characters from string, like slice(n) or substring(n) in other languages


## `val len_pos : LChar.t list -> bool`
- name: len_pos
- type: theorem
- signature: `val len_pos : LChar.t list -> bool`
- doc: The length of a string is always non-negative
- pattern: N\A


## `val len_zero_inversion : LChar.t list -> bool`
- name: len_zero_inversion
- type: theorem
- signature: `val len_zero_inversion : LChar.t list -> bool`
- doc: If the length of a string is zero, then the string is empty
- pattern: N\A


