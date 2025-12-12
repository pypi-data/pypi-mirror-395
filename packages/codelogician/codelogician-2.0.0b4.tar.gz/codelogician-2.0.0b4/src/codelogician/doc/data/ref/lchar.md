----
title: Lchar Module
description: Lchar Module types and functions
order: 9
----


## `type LChar.t =  LChar.Char of bool * bool * bool * bool * bool * bool * bool * bool`
- name: t
- type: type
- signature: `type LChar.t =
 LChar.Char of bool * bool * bool * bool * bool * bool * bool * bool`
- doc: An 8-bit character
- pattern: N\A


## `val zero : LChar.t`
- name: zero
- type: function
- signature: `val zero : LChar.t`
- doc: Returns a character with all bits set to false (null character)
- pattern: Creating a null/zero character, like '\0' or character code 0 in other languages


## `val is_printable : LChar.t -> bool`
- name: is_printable
- type: function
- signature: `val is_printable : LChar.t -> bool`
- doc: Tests if character [c] is printable based on its bit pattern
- pattern: Checking if a character is displayable/printable, like isprint() or similar character classification functions


