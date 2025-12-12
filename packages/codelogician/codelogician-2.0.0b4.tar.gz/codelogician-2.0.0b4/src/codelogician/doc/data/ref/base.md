----
title: Base Module
description: Base Module types and functions
order: 1
----


## `val +. : real -> real -> real`
- name: +.
- type: function
- signature: `val +. : real -> real -> real`
- doc: [+.] is addition for reals
- pattern: Real number arithmetic addition


## `type int = <logic_core_builtin>`
- name: int
- type: type
- signature: `type int = <logic_core_builtin>`
- doc: Builtin integer type, using arbitrary precision integers. This type is an alias to {!Z.t} (using Zarith). NOTE: here Imandra diverges from normal OCaml, where integers width is bounded by native machine integers. "Normal" OCaml integers have type {!Caml.Int.t} and can be entered using the 'i' suffix: [0i]
- pattern: Arbitrary precision integers for unbounded calculations


## `type nonrec bool = <logic_core_builtin>`
- name: bool
- type: type
- signature: `type nonrec bool = <logic_core_builtin>`
- doc: Builtin boolean type.
- pattern: Boolean true/false values for logical operations


## `val || : bool -> bool -> bool`
- name: ||
- type: function
- signature: `val || : bool -> bool -> bool`
- doc: [||] is the boolean OR operator
- pattern: Logical OR operation between two boolean values


## `val && : bool -> bool -> bool`
- name: &&
- type: function
- signature: `val && : bool -> bool -> bool`
- doc: [&&] is the boolean AND operator
- pattern: Logical AND operation between two boolean values


## `type nonrec unit = | ()`
- name: unit
- type: type
- signature: `type nonrec unit = | ()`
- doc: Unit type with single constructor [()]
- pattern: Represents absence of a meaningful value


## `val = : 'a -> 'a -> bool`
- name: =
- type: function
- signature: `val = : 'a -> 'a -> bool`
- doc: Equality. Must be applied to non-function types.
- pattern: Value equality comparison


## `val <> : 'a -> 'a -> bool`
- name: <>
- type: function
- signature: `val <> : 'a -> 'a -> bool`
- doc: [<>] is the inequality operator
- pattern: Value inequality comparison


## `val not : bool -> bool`
- name: not
- type: function
- signature: `val not : bool -> bool`
- doc: [not] is the boolean NOT operator
- pattern: Logical negation of boolean values


## `val ==> : bool -> bool -> bool`
- name: ==>
- type: function
- signature: `val ==> : bool -> bool -> bool`
- doc: [==>] is logical implication
- pattern: Logical implication in mathematical reasoning


## `val <== : bool -> bool -> bool`
- name: <==
- type: function
- signature: `val <== : bool -> bool -> bool`
- doc: [<==] is reverse logical implication
- pattern: Reverse logical implication in mathematical reasoning


## `val <==> : bool -> bool -> bool`
- name: <==>
- type: function
- signature: `val <==> : bool -> bool -> bool`
- doc: [<==>] is logical equivalence
- pattern: Logical equivalence/biconditional in mathematical reasoning


## `val + : int -> int -> int`
- name: +
- type: function
- signature: `val + : int -> int -> int`
- doc: [+] is integer addition
- pattern: Basic arithmetic addition of integers


## `val const : 'a -> 'b -> 'a`
- name: const
- type: function
- signature: `val const : 'a -> 'b -> 'a`
- doc: [const x y] returns [x]. In other words, [const x] is the constant function that always returns [x].
- pattern: Creating constant functions in functional programming


## `val >= : int -> int -> bool`
- name: >=
- type: function
- signature: `val >= : int -> int -> bool`
- doc: [>=] is greater than or equal comparison for integers
- pattern: Numeric comparison for ordering


## `val mk_nat : int -> int`
- name: mk_nat
- type: function
- signature: `val mk_nat : int -> int`
- doc: [mk_nat x] converts integer [x] to natural number by returning [x] if non-negative, 0 otherwise
- pattern: Converting integers to non-negative numbers


## `type nonrec option = | None | Some of 'a`
- name: option
- type: type
- signature: `type nonrec option = | None | Some of 'a`
- doc: Option type representing optional values
- pattern: Representing values that may or may not exist


## `type list = | [] | :: of 'a * 'a list`
- name: list
- type: type
- signature: `type list = | [] | :: of 'a * 'a list`
- doc: List type with empty list [] and cons :: constructors
- pattern: Sequential data structure with variable length


## `type nonrec float = <logic_core_builtin>`
- name: float
- type: type
- signature: `type nonrec float = <logic_core_builtin>`
- doc: Floating point number type
- pattern: IEEE 754 floating point arithmetic


## `type nonrec real = <logic_core_builtin>`
- name: real
- type: type
- signature: `type nonrec real = <logic_core_builtin>`
- doc: Real number type
- pattern: Mathematical real number calculations


## `type nonrec string = <logic_core_builtin>`
- name: string
- type: type
- signature: `type nonrec string = <logic_core_builtin>`
- doc: String type
- pattern: Text manipulation and processing


## `val < : int -> int -> bool`
- name: <
- type: function
- signature: `val < : int -> int -> bool`
- doc: [<] is less than comparison for integers
- pattern: Numeric comparison for strict ordering


## `val <= : int -> int -> bool`
- name: <=
- type: function
- signature: `val <= : int -> int -> bool`
- doc: [<=] is less than or equal comparison for integers
- pattern: Numeric comparison for non-strict ordering


## `val > : int -> int -> bool`
- name: >
- type: function
- signature: `val > : int -> int -> bool`
- doc: [>] is greater than comparison for integers
- pattern: Numeric comparison for strict ordering


## `val min : int -> int -> int`
- name: min
- type: function
- signature: `val min : int -> int -> int`
- doc: [min x y] returns the minimum of integers [x] and [y]
- pattern: Finding smaller of two numbers


## `val max : int -> int -> int`
- name: max
- type: function
- signature: `val max : int -> int -> int`
- doc: [max x y] returns the maximum of integers [x] and [y]
- pattern: Finding larger of two numbers


## `val <. : real -> real -> bool`
- name: <.
- type: function
- signature: `val <. : real -> real -> bool`
- doc: [<.] is less than comparison for reals
- pattern: Real number comparison for strict ordering


## `val <=. : real -> real -> bool`
- name: <=.
- type: function
- signature: `val <=. : real -> real -> bool`
- doc: [<=.] is less than or equal comparison for reals
- pattern: Real number comparison for non-strict ordering


## `val >. : real -> real -> bool`
- name: >.
- type: function
- signature: `val >. : real -> real -> bool`
- doc: [>.] is greater than comparison for reals
- pattern: Real number comparison for strict ordering


## `val >=. : real -> real -> bool`
- name: >=.
- type: function
- signature: `val >=. : real -> real -> bool`
- doc: [>=.] is greater than or equal comparison for reals
- pattern: Real number comparison for non-strict ordering


## `val min_r : real -> real -> real`
- name: min_r
- type: function
- signature: `val min_r : real -> real -> real`
- doc: [min_r x y] returns the minimum of reals [x] and [y]
- pattern: Finding smaller of two real numbers


## `val max_r : real -> real -> real`
- name: max_r
- type: function
- signature: `val max_r : real -> real -> real`
- doc: [max_r x y] returns the maximum of reals [x] and [y]
- pattern: Finding larger of two real numbers


## `val ~- : int -> int`
- name: ~-
- type: function
- signature: `val ~- : int -> int`
- doc: [~- x] returns the negation of integer [x]
- pattern: Arithmetic negation of integers


## `val abs : int -> int`
- name: abs
- type: function
- signature: `val abs : int -> int`
- doc: [abs x] returns the absolute value of integer [x]
- pattern: Computing magnitude of numbers


## `val - : int -> int -> int`
- name: -
- type: function
- signature: `val - : int -> int -> int`
- doc: [-] is integer subtraction
- pattern: Basic arithmetic subtraction


## `val ~+ : int -> int`
- name: ~+
- type: function
- signature: `val ~+ : int -> int`
- doc: [~+ x] returns [x] unchanged (unary plus)
- pattern: Identity operation on numbers


## `val * : int -> int -> int`
- name: *
- type: function
- signature: `val * : int -> int -> int`
- doc: [*] is integer multiplication
- pattern: Basic arithmetic multiplication


## `val / : int -> int -> int`
- name: /
- type: function
- signature: `val / : int -> int -> int`
- doc: Euclidian division on integers, see http://smtlib.cs.uiowa.edu/theories-Ints.shtml
- pattern: Integer division with rounding towards zero


## `val mod : int -> int -> int`
- name: mod
- type: function
- signature: `val mod : int -> int -> int`
- doc: Euclidian remainder on integers
- pattern: Computing remainders in modular arithmetic


## `val compare : int -> int -> int`
- name: compare
- type: function
- signature: `val compare : int -> int -> int`
- doc: Total order, if x = y then 0 else if x < y then -1 else 1
- pattern: Three-way comparison for sorting and ordering


## `type result = | Ok of 'a | Error of 'b`
- name: result
- type: type
- signature: `type result = | Ok of 'a | Error of 'b`
- doc: Result type, representing either a successful result [Ok x] or an error [Error x].
- pattern: Error handling and computation results


## `type either = | Left of 'a | Right of 'b`
- name: either
- type: type
- signature: `type either = | Left of 'a | Right of 'b`
- doc: A familiar type for Haskellers
- pattern: Representing values of two different types


## `val |> : 'a -> ('a -> 'b) -> 'b`
- name: |>
- type: function
- signature: `val |> : 'a -> ('a -> 'b) -> 'b`
- doc: Pipeline operator. [x |> f] is the same as [f x], but it composes nicely: [ x |> f |> g |> h] can be more readable than [h(g(f x))].
- pattern: Function composition in data processing pipelines


## `val @@ : ('a -> 'b) -> 'a -> 'b`
- name: @@
- type: function
- signature: `val @@ : ('a -> 'b) -> 'a -> 'b`
- doc: Right-associative application operator. [f @@ x] is the same as [f x], but it binds to the right: [f @@ g @@ h @@ x] is the same as [f (g (h x))] but with fewer parentheses.
- pattern: Nested function application without parentheses


## `val id : 'a -> 'a`
- name: id
- type: function
- signature: `val id : 'a -> 'a`
- doc: Identity function. [id x = x] always holds.
- pattern: Function that returns its input unchanged


## `val %> : ('a -> 'b) -> ('b -> 'c) -> 'a -> 'c`
- name: %>
- type: function
- signature: `val %> : ('a -> 'b) -> ('b -> 'c) -> 'a -> 'c`
- doc: Mathematical composition operator. [f %> g] is [fun x -> g (f x)]
- pattern: Composing functions in mathematical style


## `val -. : real -> real -> real`
- name: -.
- type: function
- signature: `val -. : real -> real -> real`
- doc: [-.] is subtraction for reals
- pattern: Real number arithmetic subtraction


## `val ~-. : real -> real`
- name: ~-.
- type: function
- signature: `val ~-. : real -> real`
- doc: [~-.] is negation for reals
- pattern: Real number arithmetic negation


## `val *. : real -> real -> real`
- name: *.
- type: function
- signature: `val *. : real -> real -> real`
- doc: [*.] is multiplication for reals
- pattern: Real number arithmetic multiplication


## `val /. : real -> real -> real`
- name: /.
- type: function
- signature: `val /. : real -> real -> real`
- doc: [/.] is division for reals
- pattern: Real number arithmetic division


## `val @ : 'a list -> 'a list -> 'a list`
- name: @
- type: function
- signature: `val @ : 'a list -> 'a list -> 'a list`
- doc: Infix alias to {!List.append}
- pattern: List concatenation


## `val ^ : String.t -> String.t -> String.t`
- name: ^
- type: function
- signature: `val ^ : String.t -> String.t -> String.t`
- doc: Alias to {!String.append}
- pattern: String concatenation


## `val succ : int -> int`
- name: succ
- type: function
- signature: `val succ : int -> int`
- doc: [succ x] returns the successor of integer [x]
- pattern: Incrementing integers by one


## `val pred : int -> int`
- name: pred
- type: function
- signature: `val pred : int -> int`
- doc: [pred x] returns the predecessor of integer [x]
- pattern: Decrementing integers by one


## `val fst : ('a * 'b) -> 'a`
- name: fst
- type: function
- signature: `val fst : ('a * 'b) -> 'a`
- doc: [fst (x,y)] returns the first component [x] of pair [(x,y)]
- pattern: Accessing first element of a pair


## `val snd : ('a * 'b) -> 'b`
- name: snd
- type: function
- signature: `val snd : ('a * 'b) -> 'b`
- doc: [snd (x,y)] returns the second component [y] of pair [(x,y)]
- pattern: Accessing second element of a pair


## `val -- : int list -> int list -> int list`
- name: --
- type: function
- signature: `val -- : int list -> int list -> int list`
- doc: Alias to {!List.(--)}
- Note: `end` is not included in the generated list of `(start -- end)`.
- Example: `(1--3) (* gives [1;2] *)`
- pattern: Integer range generation


