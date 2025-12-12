---
title: Ordinal Module
description: Ordinal used in termination proofs
order: 9
---


# Module `Ordinal`

18 entries

The following entries are qualified by the module `Ordinal`.

`t`
- Signature: `type t = Int of int | Cons of t * int * t`
- Doc: Ordinals, up to ε₀, in Cantor Normal Form

`of_int`
- Signature: `val of_int : int -> t`
- Doc: Creates an ordinal from an integer.

`~$`
- Signature: `val (~$) : int -> t`
- Doc: Infix operator for `of_int`.

`<<`
- Signature: `val (<<) : t -> t -> bool`
- Doc: The well-founded relation on ordinals.

`plus`
- Signature: `val plus : t -> t -> t`
- Doc: Addition of ordinals. Not commutative.

`simple_plus`
- Signature: `val simple_plus : t -> t -> t`
- Doc: Adds two ordinals, but only if they are both integers, otherwise returns 0.

`+`
- Signature: `val (+) : t -> t -> t`
- Doc: Infix operator for `plus`.

`of_list`
- Signature: `val of_list : t list -> t`
- Doc: Creates an ordinal from a list of ordinals.

`pair`
- Signature: `val pair : t -> t -> t`
- Doc: Creates an ordinal pair.

`triple`
- Signature: `val triple : t -> t -> t -> t`
- Doc: Creates an ordinal triple.

`quad`
- Signature: `val quad : t -> t -> t -> t -> t`
- Doc: Creates an ordinal quad.

`shift`
- Signature: `val shift : t -> by:t -> t`
- Doc: Shifts an ordinal.

`is_valid`
- Signature: `val is_valid : t -> bool`
- Doc: Checks if an ordinal is valid.

`is_valid_rec`
- Signature: `val is_valid_rec : t -> bool`
- Doc: Recursive helper to check if an ordinal is valid.

`zero`
- Signature: `val zero : t`
- Doc: The ordinal for zero.

`one`
- Signature: `val one : t`
- Doc: The ordinal for one.

`omega`
- Signature: `val omega : t`
- Doc: The omega ordinal.

`omega_omega`
- Signature: `val omega_omega : t`
- Doc: The omega^omega ordinal.
