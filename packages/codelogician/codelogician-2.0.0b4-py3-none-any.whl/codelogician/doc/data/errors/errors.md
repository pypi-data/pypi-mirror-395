----
title: Common errors when evaluating IML code in ImandraX 
description: A set of common errors and recommended solutions
order: 1
----

- explanation: |
    The `let*` binding operator is not available globally in IML. It must be brought into
    scope by opening the appropriate module (Option, Result, etc.).
  kind: TypeErr
  msg_str: Unknown identifier "let*".
  name: monadic_binding_pattern_match
  repro_iml: |
    type order_type = Market | Limit
    type order = {
      order_type : order_type;
      order_price : real;
    }
    type order_book = {
      buy_orders : order list;
    }
    let next_buy (ob : order_book) : order option =
      List.nth 0 ob.buy_orders
    let ob : order_book = {
      buy_orders = [{order_type = Market; order_price = 100.0}];
    }
    let b_bid =
      let* next = next_buy ob in
      if next.order_type <> Market then
        Some next.order_price
      else
        None
  solution: |
    type order_type = Market | Limit
    type order = {
      order_type : order_type;
      order_price : real;
    }
    type order_book = {
      buy_orders : order list;
    }
    let next_buy (ob : order_book) : order option =
      List.nth 0 ob.buy_orders
    let ob : order_book = {
      buy_orders = [{order_type = Market; order_price = 100.0}];
    }
    let b_bid =
      match next_buy ob with
      | Some next ->
        if next.order_type <> Market then
          Some next.order_price
        else
          None
      | None -> None
  solution_description: |
    Replace monadic binding with explicit pattern matching.
  tags: []
- explanation: |
    IML's standard comparison operators (<, >, <=, >=) are typed for integers by default.
    Using them on real numbers causes a type error. The Real module provides separate
    comparison operators for real numbers.
  kind: TypeErr
  msg_str: |-
    Application failed: expected argument of type `int`
    but got (price : real)
  name: real_comparison_operators
  repro_iml: |
    let price : real = 10.5
    let threshold : real = 5.0
    let max_price : real = 100.0
    let result =
      if price < threshold then
        Some price
      else if price > max_price then
        Some max_price
      else
        None
  solution: |
    let price : real = 10.5
    let threshold : real = 5.0
    let max_price : real = 100.0
    let result =
      if Real.(<) price threshold then
        Some price
      else if Real.(>) price max_price then
        Some max_price
      else
        None
  solution_description: |
    Use Real module comparison operators: Real.(<), Real.(>), Real.(<=), Real.(>=).
  tags: []
- explanation: |
    IML cannot automatically prove termination when the recursion pattern is non-standard
    (e.g., recursion on list length rather than list structure). An explicit measure
    annotation is required to show what decreases with each recursive call.
  kind: TacticEvalErr
  msg_str: 'Tactic failed: Goal is counter-satisfiable.'
  name: termination_measure_annotation
  repro_iml: |
    let rec left_pad c n xs =
      if List.length xs >= n then
        xs
      else
        left_pad c n (c :: xs)
  solution: |
    let left_pad_measure n xs =
      Ordinal.of_int (n - List.length xs)
    let rec left_pad c n xs =
      if List.length xs >= n then
        xs
      else
        left_pad c n (c :: xs)
    [@@measure left_pad_measure n xs]
  solution_description: |
    Add [@@measure ...] annotation with a function returning Ordinal.t that provably
    decreases on each recursive call.
  tags: []
- explanation: |
    Termination measures in IML must return `Ordinal.t`, not `int`. The `[@@measure ...]`
    attribute expects a function that returns an ordinal value to prove well-founded recursion.
  kind: TypeErr
  msg_str: |-
    Expression is expected to have type `Ordinal.t`,
    but its inferred type is `int`.
  name: measure_ordinal_type_mismatch
  repro_iml: |
    type action = Identity | Increment | Decrement
    let apply_action (act : action) (x : int) : int =
      match act with
      | Identity -> x
      | Increment -> x + 1
      | Decrement -> x - 1
    let process_actions_measure (actions : action list) (state : int) : int =
      List.length actions
    let rec process_actions (actions : action list) (state : int) : int =
      match actions with
      | [] -> state
      | act :: rest ->
          let new_state = apply_action act state in
          process_actions rest new_state
    [@@measure process_actions_measure actions state]
  solution: |
    type action = Identity | Increment | Decrement
    let apply_action (act : action) (x : int) : int =
      match act with
      | Identity -> x
      | Increment -> x + 1
      | Decrement -> x - 1
    let process_actions_measure (actions : action list) (state : int) : Ordinal.t =
      Ordinal.of_int (List.length actions)
    let rec process_actions (actions : action list) (state : int) : int =
      match actions with
      | [] -> state
      | act :: rest ->
          let new_state = apply_action act state in
          process_actions rest new_state
    [@@measure process_actions_measure actions state]
  solution_description: |
    Wrap the measure function's return value with `Ordinal.of_int` to convert int to Ordinal.t.
  tags: []
- explanation: |
    IML enforces a first-order type restriction: functions cannot be elements of composite types
    (lists, tuples, records, or algebraic data types). This is required for the formal semantics
    and automated reasoning capabilities.
  kind: ValidationError
  msg_str: |-
    Function definition is not valid:
    Functions must return a first-order type,
    but `ls_f` returns `(int -> int) list`
  name: function_list_first_order_violation
  repro_iml: |
    let f (x : int) : int = x + 1
    let ls_f = [f; f; f]
  solution: |
    let f (x : int) : int = x + 1
    type action =
      | AddOne
      | AddTwo
      | AddThree
    let apply_action (act : action) (x : int) : int =
      match act with
      | AddOne -> x + 1
      | AddTwo -> x + 2
      | AddThree -> x + 3
    let ls_actions = [AddOne; AddOne; AddOne]
  solution_description: |
    Use an algebraic data type to represent different actions instead of storing functions.
  tags: []
- explanation: |
    IML integers have arbitrary precision, so there is no built-in `max_int` constant.
    Unlike OCaml which has bounded integers, IML can represent arbitrarily large integers.
  kind: TypeErr
  msg_str: Unknown identifier "max_int".
  name: max_int_not_available
  repro_iml: |
    let clamp (x : int) : int =
      if x > max_int then
        max_int
      else
        x
  solution: |
    let max_allowed = 1000000
    let clamp (x : int) : int =
      if x > max_allowed then
        max_allowed
      else
        x
  solution_description: |
    Use a specific constant for your use case.
  tags: []
- explanation: |
    The `let*` binding operator is part of the Option module but not available globally.
    It needs to be brought into scope by opening the Option module or using qualified syntax.
  kind: TypeErr
  msg_str: Unknown identifier "let*".
  name: let_star_binding_not_in_scope
  repro_iml: |
    let process_options (x : int option) (y : int option) : int option =
      let* x_val = x in
      let* y_val = y in
      Some (x_val + y_val)
  solution: |
    let process_options (x : int option) (y : int option) : int option =
      let open Option in
      let* x_val = x in
      let* y_val = y in
      Some (x_val + y_val)
  solution_description: |
    Open the Option module to use let* binding operator.
  tags: []
- explanation: |
    `Real.pow` has signature `real -> int -> real`. The exponent must be an integer, not a real.
    This is because IML only supports integer exponentiation for exact arithmetic.
  kind: TypeErr
  msg_str: |-
    Application failed: expected argument of type `Int.t`
    but got (exponent : real)
  name: real_pow_exponent_must_be_int
  repro_iml: |
    let calculate (n : int) : real =
      let base = 2.5 in
      let exponent = Real.of_int (n / 41670) in
      Real.pow base exponent
  solution: |
    let calculate (n : int) : real =
      let base = 2.5 in
      let exponent = Real.of_int (n / 41670) in
      Real.pow base (Real.to_int exponent)
  solution_description: |
    Convert the exponent back to int using Real.to_int.
  tags: []
- explanation: |
    `List.fold_left2` does not exist in IML's List module. IML has `List.map2` but not fold_left2.
  kind: TypeErr
  msg_str: Unknown function `List.fold_left2`.
  name: list_fold_left2_not_available
  repro_iml: |
    let sum_pairs (l1 : int list) (l2 : int list) : int =
      List.fold_left2 (fun acc x y -> acc + x + y) 0 l1 l2
  solution: |
    let sum_pairs (l1 : int list) (l2 : int list) : int =
      match List.map2 (fun x y -> (x, y)) l1 l2 with
      | Error _ -> 0
      | Ok pairs -> List.fold_left (fun acc (x, y) -> acc + x + y) 0 pairs
  solution_description: |
    Use List.map2 to create pairs first, then fold.
  tags: []
- explanation: |
    Two issues: (1) `max_real` is not a built-in constant in IML, and (2) the comparison
    operator `>` is for integers. Real comparison requires different operators like `>.`,
    `<.`, `>=.`, `<=.` (though the standard operators now work for reals too).
  kind: TypeErr
  msg_str: |-
    Application failed: expected argument of type `int`
    but got (x : real)
  name: real_comparison_type_mismatch
  repro_iml: |
    let some_function (x : real) : real =
      if x > max_real then
        max_real
      else
        x
  solution: |
    let max_real_bound = 1000000.0
    let some_function (x : real) : real =
      if x >. max_real_bound then
        max_real_bound
      else
        x
  solution_description: |
    Define a specific bound and use real comparison operator.
  tags: []
- explanation: |
    Arrays are mutable data structures and not available in IML, which is a pure functional
    language without mutable state. All operations must be immutable.
  kind: TypeErr
  msg_str: Unknown identifier `Array.make`.
  name: array_not_available
  repro_iml: |
    let example () =
      let arr = Array.make 5 0 in
      arr
  solution: |-
    (* Use list instead of Array *)
    let example () =
      let arr = List.mapi (fun _ _ -> 0) (0 -- 5) in
      arr
  solution_description: |
    Use immutable lists with functional updates instead of arrays.
  tags: []
- explanation: |
    `Option.map2` does not exist in IML's Option module. Use `Option.monoid_product`
    or monadic composition instead.
  kind: TypeErr
  msg_str: Unknown function `Option.map2`.
  name: option_map2_not_available
  repro_iml: |
    let add_options (x : int option) (y : int option) : int option =
      Option.map2 (fun a b -> a + b) x y
  solution: |
    let add_options (x : int option) (y : int option) : int option =
      Option.monoid_product x y |> Option.map (fun (a, b) -> a + b)
  solution_description: |
    Use Option.monoid_product with map.
  tags: []
- explanation: |
    Similar to `max_int`, IML does not have a built-in `min_int` constant because integers
    have arbitrary precision and can be arbitrarily small (negative).
  kind: TypeErr
  msg_str: Unknown identifier "min_int".
  name: min_int_not_available
  repro_iml: |
    let clamp (x : int) : int =
      if x < min_int then
        min_int
      else
        x
  solution: |
    let min_allowed = -1000000
    let clamp (x : int) : int =
      if x < min_allowed then
        min_allowed
      else
        x
  solution_description: |
    Use a specific constant.
  tags: []
- explanation: |
    In IML, the function is called `Option.flat_map` instead of `Option.bind`. The monadic
    bind operator is available as `>>=` within the Option module.
  kind: TypeErr
  msg_str: Unknown function `Option.bind`.
  name: option_bind_not_available
  repro_iml: |
    let process (x : int option) : int option =
      Option.bind x (fun v -> Some (v + 1))
  solution: |
    let process (x : int option) : int option =
      Option.flat_map (fun v -> Some (v + 1)) x
  solution_description: |
    Use Option.flat_map.
  tags: []
- explanation: |
    IML is a pure language without exceptions. The `failwith` function from OCaml is not
    available. Error handling must use `Option` or `Result` types instead.
  kind: TypeErr
  msg_str: Unknown identifier "failwith".
  name: failwith_not_available
  repro_iml: |
    let divide (x : int) (y : int) : int =
      if y = 0 then
        failwith "Division by zero"
      else
        x / y
  solution: |
    let divide (x : int) (y : int) : int option =
      if y = 0 then
        None
      else
        Some (x / y)
  solution_description: |
    Return an option type with None for error cases.
  tags: []
- explanation: |
    References (`ref`) are mutable state and not available in IML, which is purely functional.
    All state changes must be explicit through function parameters and return values.
  kind: TypeErr
  msg_str: Unknown identifier "ref".
  name: ref_not_available
  repro_iml: |
    let counter () =
      let count = ref 0 in
      count := !count + 1;
      !count
  solution: |
    let counter (count : int) : int =
      count + 1
  solution_description: |
    Use a parameter to track state.
  tags: []
