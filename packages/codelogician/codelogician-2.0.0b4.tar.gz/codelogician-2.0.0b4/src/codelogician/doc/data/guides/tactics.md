----
title: Module `Tactic`
description: Description of tactics and other
order: 5
----

The following entries are qualified by the module `Tactic`.

`tac_loc`
- Signature: `type tac_loc`
- Doc: Position in the tactic tree

`goal`
- Signature: `type goal`
- Doc:

`proof`
- Signature: `type proof`
- Doc:

`model`
- Signature: `type model`
- Doc:

`'a term`
- Signature: `type 'a term`
- Doc:

`quote_term`
- Signature: `val quote_term : 'a -> 'a term`
- Doc: [quote_term (1 + 2)] is a quotation that will not evaluate to anything but the term "1 + 2". It can then be provided as-is to a tactic.

`'a res`
- Signature: `type 'a res = ('a, string * model option * goal list * tac_loc option) result`
- Doc:

`'a m`
- Signature: `type 'a m = goal -> 'a res`
- Doc: The main tactic monad.

`t`
- Signature: `type t = (goal list * proof) option m`
- Doc: The type of tactics. A tactic takes a goal and either:
      - returns [Error _] to signal failure
      - returns [Ok None] to signal that it did nothing (goal stays the same)
      - returns [Ok (Some (subgoals, proof))] with new subgoals and the proof
        that these (boxed) imply the input goal (boxed).

`return`
- Signature: `val return : 'a -> 'a m`
- Doc: Succeed with a value.

`fail_res`
- Signature: `val fail_res : ?subgoals:goal list -> string -> 'a res`
- Doc: Return a failure result. Useful in custom tactics.

`fail`
- Signature: `val fail : string -> 'a m`
- Doc: Tactic that always just fails.

`goal`
- Signature: `val goal : goal m`
- Doc: Access the current goal.

`combine_proofs`
- Signature: `val combine_proofs : proof list -> proof -> proof`
- Doc: Given a proof [p] of [box A1, ..., box An |- box B] and [hyps], proofs of [|- box A_i] respectively, return a proof of [|- box B]

`( let+ )`
- Signature: `val ( let+ ) : 'a m -> ('a -> 'b) -> 'b m`
- Doc: Monadic map.

`( let* )`
- Signature: `val ( let* ) : 'a m -> ('a -> 'b m) -> 'b m`
- Doc: Monadic bind.

`@>`
- Signature: `val ( @> ) : t -> t -> t`
- Doc: [t @> t'] expects [t] to produce exactly one sub-goal, and uses [t'] to prove this subgoal.

`@>|`
- Signature: `val ( @>| ) : t -> t list -> t`
- Doc: [t @>| [t1; t2; ...; tn]] expects [t] to return exactly [n] sub-goals, and uses [t_i] to solve the [i]-th goal.

`@>>|`
- Signature: `val ( @>>| ) : t -> t -> t`
- Doc: [t1 @>>| t2] applies t1 and then applies t2 to all t1-generated subgoals.

`<|>`
- Signature: `val ( <|> ) : t -> t -> t`
- Doc: [t1 <|> t2] is the `or tactical` which applies t1 and uses its result if it succeeds, and otherwise applies t2 if t1 had failed.

`skip`
- Signature: `val skip : t`
- Doc: [skip] is a no-op from a reasoning perspective (goal will be unchanged). This can be useful when needing to put a place-holder tactic in, e.g., a list of tactics for subgoals when using [@>|], e.g., [... @|> [...; skip; ...]]. See the variant [skip_msg] which is like [skip] but also prints a message. Note the notation [[%skip "skip message"]] can be used, with [[%skip]] emitting no message.

`skip_msg`
- Signature: `val skip_msg : string -> t`
- Doc: [skip_msg "msg"] is like [skip] (a reasoning no-op) but also prints the string "msg". This can be useful for tactic debugging. Note the notation [[%skip "skip message"]] can be used, with [[%skip]] emitting no message.

`try_`
- Signature: `val try_ : t -> t`
- Doc: [try_ t] is the `try tactical` which returns the result of applying t if t succeeds, and otherwise does nothing (using [skip])

`ground_eval`
- Signature: `val ground_eval : ?max_cache:int -> unit -> t`
- Doc:

`qs`
- Signature: `val qs : t`
- Doc: A very fast, incomplete SMT solver for simple QF_UFDT/LIA/LRA goals.

`cc`
- Signature: `val cc : t`
- Doc:

`simp`
- Signature: `val simp : t`
- Doc: Quick and simple simplifier. This always returns 1 goal.
- Detail: Used for simplifying goals. `[%simp rule1, rule2]` is a shorthand for `simplify ~rules:[...]`.

`simp_all`
- Signature: `val simp_all : t`
- Doc: Quick and simple simplifier on hypotheses and conclusion. This always returns 1 goal.

`ctx_simplify`
- Signature: `val ctx_simplify : t`
- Doc: Contextual simplifcation

`expr_simplify`
- Signature: `val expr_simplify : t`
- Doc: Moral equivalent of Z3's Expr.simplify applied to each hypothesis and conclusion in the goal.
- Detail: Used for expression simplification. `esimp` is a convenient alias.

`esimp`
- Signature: `val esimp : t`
- Doc: Alias for expr_simplify.
- Detail: Used for expression simplification.

`or_left`
- Signature: `val or_left : t`
- Doc: Takes [G ?- a || b], returns [G ?- a]

`or_right`
- Signature: `val or_right : t`
- Doc: Takes [G ?- a || b], returns [G ?- b]

`split_and`
- Signature: `val split_and : t`
- Doc: Takes [G ?- a && b], returns [G ?- a] and [G ?- b]

`exact`
- Signature: `val exact : t`
- Doc: Takes [G, t ?- t, ...], succeeds with no further goal. Otherwise fails.

`trivial`
- Signature: `val trivial : t`
- Doc: Succeeds if a goal is trivially true due to having [false] in the hypotheses, [true] in the conclusion, or the exact same term in the hypotheses and conclusion (subsuming the [exact] tactic).
- Detail: Used to solve goals that are simple tautologies or can be solved by simple inspection of the context.

`intros`
- Signature: `val intros : t`
- Doc: [intros] takes a goal [H |- (A && B) ==> C] and returns the new goal [H, A, B |- C].

`unintros`
- Signature: `val unintros : int list -> t`
- Doc: [unintros [1;3;4]] takes a goal [H0; H1; ...; H7 |- C] and turns it into [H0; H2; H5; H6; H7 |- (H1 && H3 && H4) ==> C]. In that sense it's the inverse of [intros].

`swap`
- Signature: `val swap : int -> t`
- Doc: [swap i] takes a goal [H0; ...; Hk |- C0; ...; Ck] and `swaps` a literal (either a hypothesis or a conclusion term) over the sequent line (|-), negating it in the process. If [i>=0], then hypothesis [i] ([Hi]) is negated and made a conclusion. If [i<0], then conclusion [abs(i+1)] (C(abs(i+1))) is negated and made a hypothesis.
- Detail: Used to move a hypothesis to the conclusion (or vice-versa) by negating it. Example: `swap (-1)` moves the first conclusion to the hypotheses.

`drop`
- Signature: `val drop : int -> t`
- Doc: [drop i] drops a hypothesis or conclusion, using the same literal addressing scheme as `swap`.

`expand`
- Signature: `val expand : ?index:int -> ?all:bool -> string -> t`
- Doc: [expand "foo"] expands the first occurrence of `foo`. [expand ~index:3 "foo"] expands the index 3 (i.e., fourth) occurrence of `foo`. [expand ~all:true "foo"] expands all current instances of `foo`. Instances introduced through this expansion process will not be recursively expanded. Note the notation [[%expand "foo"]] can also be used, with either function names or terms which will be automatically quoted (see `expand_term`).

`expand_term`
- Signature: `val expand_term : ?index:int -> ?all:bool -> 'a term -> t`
- Doc: [expand_term (quote_term (foo x))] expands the first occurrence of `foo x`. [expand_term ~index:3 (quote_term (foo x))] expands the index 3 (i.e., fourth) occurrence of `foo x`. [expand_term ~all:true (quote_term (foo x))] expands all current instances of `foo`. Instances introduced through this expansion process will not be recursively expanded. Note the notation [[%expand (foo x)]] handles term quoting automatically.

`replace`
- Signature: `val replace : 'a term -> t`
- Doc: [replace (quote_term x)] uses an equality hypothesis `x=t` to replace `x` by `t`.
- Detail: Used to perform a substitution based on an equality in the goal. The syntax is `[%replace my_var]`.

`normalize`
- Signature: `val normalize : ?rules:identifier list -> ?strict:bool -> ?basis:identifier list -> ?inline:bool -> 'a term -> t`
- Doc: [normalize (quote_term t)] normalizes a given term under hypotheses of the current goal, replacing the term with its normalized version if it appears in the goal, and adding the hypotheses `t = normalized_t` if the target term does not appear already in the goal. Normalization applies all active rewrite rules, forward chaining rules, expands all enabled non-recursive function definitions and includes the speculative expansion and simplification of recursive functions in order to take advantage of inductive hypotheses, in the same manner as the waterfall simplifier. The `rules` and `strict` parameters behave the same as with the `simplify` tactic, restricting which rewrite rules and function definitions may be applied and/or expanded. The `basis` parameter acts as a restriction on which function definitions can be expanded (basis members are not expanded, unless they are explicitly given via `rules` with `strict:true`. Note the notation [[%normalize t]] which normalizes term `t` with default arguments given to [normalize].
- Detail: Used to normalize a specific term in the goal. The syntax is `[%normalize my_term]`. It can be restricted to a set of rules, e.g., `normalize ~rules:[[%id my_rule]] [%t my_term]`.

`cases`
- Signature: `val cases : bool term list -> t`
- Doc: [cases [(quote_term t1);...;(quote_term tk)]] case-splits on the given cases, returning k+1 subgoals consisting of one for each case (with the case added as a hypothesis), and one additional subgoal for the 'negative' case in which all t1,...,tk are false. The terms must be boolean-valued. Note the notation [[%cases t1, t2, ..., tk]] will handle term quoting automatically.

`subgoal`
- Signature: `val subgoal : bool term -> t`
- Doc: [subgoal (quote_term t)] assumes a term and adds the correctness of this assumption as a subgoal. This effectively applies the `cut` rule of sequent calculus to produce two subgoals: one in which the term has been assumed, and another in which the term must be proved under the current goal context. The term must be boolean-valued. Note the notation [[%subgoal t]] will handle term quoting automatically.
- Detail: Used to introduce a new subgoal. This is useful for breaking down a complex proof. Syntax: `[%subgoal my_subgoal]`.

`lift_ifs`
- Signature: `val lift_ifs : t`
- Doc: Lift if-then-else expressions to the top-level and split accordingly into subgoals. This does a limited amount of feasibility checking to eliminate obviously true subgoals (infeasible `if` branches under the current context) while lifting.
- Detail: A common tactic used to handle conditional expressions in the goal by splitting the proof into cases. It is often followed by `@>|` to handle the generated subgoals.

`tauto`
- Signature: `val tauto : t`
- Doc: Tauto is a propositional tautology checker. Tauto fails if the goal is not proved. Tauto is actually a fail-if-not-proved version of [lift_ifs @>>| exact], as [lift_ifs] followed by [exact] is a complete tautology checker using if-normalization.

`flatten`
- Signature: `val flatten : t`
- Doc: Disjunctive flattening.

`smolsmt`
- Signature: `val smolsmt : t`
- Doc: A small and simple SMT solver for QF_UF goals.

`unroll`
- Signature: `val unroll : ?smt:string -> ?query_timeout:int -> ?no_asm_query_timeout:int -> int -> t`
- Doc: [unroll ~smt:"z3" 42] does 42 rounds of unrolling with SMT solver named "z3". Pass [?smt:None] to use the best available SMT solver.
- Detail: Used to prove properties of recursive functions by unrolling their definitions a fixed number of times. Example: `[@@by unroll 20]`.

`arith`
- Signature: `val arith : t`
- Doc: A decision procedure for linear (real and integer) arithmetic.
- Detail: Used to solve goals that are propositions in linear arithmetic.

`nonlin`
- Signature: `val nonlin : ?smt:string -> unit -> t`
- Doc: An SMT solver with non-linear arithmetic enabled. Pass [None] to use the best available SMT solver.
- Detail: Used to solve goals involving non-linear arithmetic. Example: `[@@by nonlin ()]`.

`auto`
- Signature: `val auto : t`
- Doc: Auto tactic, Imandra's flagship automated inductive waterfall proof procedure, taking into account all known active (rw,fc,elim,gen) rules, incorporating conditional rewriting with back-chaining, speculative expansion of recursive functions and symbolic execution, forward-chaining for simplification contexts, subgoaling, congruence closure, tautology detection, destructor elimination, generalization and automated induction.
- Detail: Used extensively in the examples to automatically prove theorems and lemmas. It is often used as the only tactic in a `[@@by ...]` block, like `[@@by auto]`. It can also be used at the end of a tactic chain to finish off goals, like `... @> auto]`.

`induction`
- Signature: `val induction : ?id:identifier -> ?vars:string list -> unit -> t`
- Doc: Induction tactic: Synthesize an induction scheme for the goal and apply it. This does not invoke the induction waterfall (as in `auto`).
- Detail: These tactics are used to initiate proofs by induction. They can be used to induct on the structure of a term (`[@@by induction ()]`), on a function (`[@@by induct ~on_fun:[%id f] ()]`), or using a custom induction scheme (`[@@by induction ~id:[%id my_induct] ()]`). They are typically the first tactic in a proof and are often combined with other tactics using `@>|` or `@>>|` to handle the different induction cases.

`simplify`
- Signature: `val simplify : ?smt:string -> ?backchain_limit:int -> ?rules:identifier list -> ?strict:bool -> ?basis:identifier list -> unit -> t`
- Doc: Full simplifier (the waterfall simplifier). Pass [?smt:None] to use the best available SMT solver. The parameter `rules` is an optional list of IDs of rewrite rules. If given, only these rewrite rules will be used during simplification. The parameter `~strict` when `true` and given in conjunction with `rules` further restricts the simplifier to only use definitional rules (function definitions, both recursive and non-recursive) and rewrite rules which are explicitly present in the `rules` list. The parameter `~backchain_limit` controls the recursive depth of back-chaining on hypotheses that is allowed during the relieving of rewrite rule guards (hypotheses). Note the syntax `[%simplify foo, bar, baz]` which expands to `simplify ~rules:[[%id foo]; [%id bar]; [%id baz]] ()`. Note that `[%simp ...]` is an alias for `[%simplify ...]`. Note the syntax `[%simplify_only ...]` and its alias `[%simp_only ...]` which are like `[%simp ...]` with `~strict:true`.
- Detail: Used for simplifying goals. `[%simp rule1, rule2]` is a shorthand for `simplify ~rules:[...]`. `[%simp_only ...]` is used when you want to control exactly which rewrite rules are applied. Example: `[@@by [%simp_only rev_len] @> [%simp_only len_append, k]]`.

`induct`
- Signature: `val induct : ?smt:string -> ?on_fun:identifier -> ?on_vars:string list -> ?otf:bool -> ?max_induct:int -> ?do_not:string list -> unit -> t`
- Doc: Induction using the waterfall. Use like this: [induct ~smt:"z3" ~on_vars:["x"; "y"] ()] for structural induction, or [induct ~on_fun:[%id f] ()] for function induction with function [f]
- Detail: These tactics are used to initiate proofs by induction. They can be used to induct on the structure of a term (`[@@by induction ()]`), on a function (`[@@by induct ~on_fun:[%id f] ()]`), or using a custom induction scheme (`[@@by induction ~id:[%id my_induct] ()]`). They are typically the first tactic in a proof and are often combined with other tactics using `@>|` or `@>>|` to handle the different induction cases.

`use`
- Signature: `val use : bool term -> t`
- Doc: Use an existing theorem to add an additional hypothesis to the current goal. For example [use (quote_term (add_is_commutative x y))] takes a goal [A ?- B] and returns a goal [(x+y)=(y+x), A ?- B]. Note the notation [[%use foo x y z]] handles term quoting automatically.
- Detail: Used to bring a previously proven lemma or theorem into the current proof context. The syntax is `[%use my_lemma x y]`. It is often chained with `auto` to use the new hypothesis to solve the goal: `[@@by [%use my_lemma] @> auto]`.

`enumerate`
- Signature: `val enumerate : string list -> t`
- Doc: A tactic that enumerates all values of finite-type variables.

`repeat`
- Signature: `val repeat : ?depth:int -> t -> t`
- Doc: [repeat tac] applies [tac] to a goal, to obtain new subgoals. It then recurse on each of these subgoals, until it reaches subgoals where [tac] return [None] (does nothing). The [depth] parameter is used to prevent infinite recursions. If it is non-positive then this just applies [tac]. The default value is [20].

`par_solve`
- Signature: `val par_solve : (t term * goal) list -> proof list res`
- Doc: Primitive to solve subgoals in parallel

`par`
- Signature: `val par : t -> t term -> t`
- Doc: [par split tac] uses [split] to split the current goal into a list of subgoals; then it applies [tac] to each subgoal in parallel.