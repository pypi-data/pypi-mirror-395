----
title: Numeric Approximations
description: A number of useful approximations of numeric constants and functions
order: 1
----

### Pi

```
let pi = 3.14159265358979323846
```

### Pi/2

```
let pi_over_2 = 1.57079632679489661923
```

### Exp
```
let exp (x : real) =
    (* Truncated Taylor series approximation of `e^x` for n=5 *)
    1.0 +.
    x +.
    (x *. x) /. 2.0 +.
    (x *. x *. x) /. 6.0 +.
    (x *. x *. x *. x) /. 24.0 +.
    (x *. x *. x *. x *. x) /. 120.0
```

### Sin
```
let sin (x : real) = 
    (* Truncated Taylor series approximation of `sin` for n=5 *)
    x -. 
    (x *. x *. x) /. 6.0 +.
    (x *. x *. x *. x *. x) /. 120.0 -.
    (x *. x *. x *. x *. x *. x *. x) /. 5040.0 +.
    (x *. x *. x *. x *. x *. x *. x *. x *. x) /. 362880.0 -.
    (x *. x *. x *. x *. x *. x *. x *. x *. x *. x *. x) /. 39916800.0
```

### Cos
```
let cos (x : real) = 
    (* Truncated Taylor series approximation of `cos` for n=5 *)
    1.0 -.
    (x *. x) /. 2.0 +.
    (x *. x *. x *. x) /. 24.0 -.
    (x *. x *. x *. x *. x *. x) /. 720.0 +.
    (x *. x *. x *. x *. x *. x *. x *. x) /. 40320.0 -.
    (x *. x *. x *. x *. x *. x *. x *. x *. x *. x) /. 3628800.0
```

### Tan
```
let tan (x : real) = 
    (* Truncated Taylor series approximation of `tan` for n=5 *)
    if x <. -.pi_over_2 || x >. pi_over_2 then None
    else Some (
        x +.
        (x *. x *. x) /. 3.0 +.
        (2.0 *. x *. x *. x *. x *. x) /. 15.0 +.
        (17.0 *. x *. x *. x *. x *. x *. x *. x) /. 315.0 +.
        (62.0 *. x *. x *. x *. x *. x *. x *. x *. x) /. 2835.0)
```

### Sec
```
let sec (x : real) = 
    (* Truncated Taylor series approximation of `sec` for n=5 *)
    if x <. -.pi_over_2 || x >. pi_over_2 then None
    else Some (
        1.0 /. cos x)
```

### Arcsin
```
let arcsin ( x : real ) =
    (* Truncated Taylor series approximation for `arcsin` for n=5 *)
    if x <. -.1.0 || x >. 1.0 then None
    else Some (
        x +.
        (x *. x *. x) /. 6.0 +.
        (3.0 *. x *. x *. x *. x *. x) /. 40.0 +.
        (5.0 *. x *. x *. x *. x *. x *. x *. x) /. 112.0 +.
        (35.0 *. x *. x *. x *. x *. x *. x *. x *. x) /. 1152.0)
```

### Arccos
```
let arccos ( x : real ) =
    (* Truncated Taylor series approximation for `arccos` for n=5 *)
    if x <. -.1.0 || x >. 1.0 then None
    else Some (
        pi_over_2 -. 
        (x +.
        (x *. x *. x) /. 6.0 +.
        (3.0 *. x *. x *. x *. x *. x) /. 40.0 +.
        (5.0 *. x *. x *. x *. x *. x *. x *. x) /. 112.0 +.
        (35.0 *. x *. x *. x *. x *. x *. x *. x *. x) /. 1152.0))
```

### Arctan
```
let arctan (x : real) =
    (* Truncated Taylor series expansion *)
    if x <. -1.0 || x >. 1.0 then None
    else Some (
        x -. 
        (x *. x *. x) /. 3.0 +.
        (x *. x *. x *. x *. x) /. 5.0 -.
        (x *. x *. x *. x *. x *. x *. x) /. 7.0 +.
        (x *. x *. x *. x *. x *. x *. x *. x *. x) /. 9.0)
```

### Sinh
```
(* Hyperbolic functions *)
let sinh (x : real) =
    (* Truncated Taylor series approximation for `sinh` for n=5 *)
    x +.
    (x *. x *. x) /. 6.0 +.
    (x *. x *. x *. x *. x) /. 120.0 +.
    (x *. x *. x *. x *. x *. x *. x) /. 5040.0 +.
    (x *. x *. x *. x *. x *. x *. x *. x *. x) /. 362880.0
```

### Cosh
```
let cosh (x : real) = 
    (* Truncated Taylor series approximation for 'cosh' for n=5 *)
    1.0 +.
    (x *. x) /. 2.0 +.
    (x *. x *. x *. x) /. 24.0 +.
    (x *. x *. x *. x *. x *. x) /. 720.0 +.
    (x *. x *. x *. x *. x *. x *. x *. x) /. 40320.0 +.
    (x *. x *. x *. x *. x *. x *. x *. x *. x) /. 3628800.0
```

### Tanh
```
let tanh (x : real) = 
    (* Truncated Taylor series approximation for `tanh` for n = 5 *)
    if x <. -.pi_over_2 || x >. pi_over_2 then None
    else Some (
        x -.
        (x *. x *. x) /. 3.0 +.
        (2.0 *. x *. x *. x *. x *. x) /. 15.0 +.
        (17.0 *. x *. x *. x *. x *. x *. x *. x) /. 315.0 +.
        (62.0 *. x *. x *. x *. x *. x *. x *. x *. x) /. 2835.0 +.
        (x *. x *. x *. x *. x *. x *. x *. x *. x) /. 15552.0 )
```

### Arcsinh
```
let arcsinh (x : real) = 
    (* Truncated Taylor series approximation for `arcsinh` for n=5 *)
    if x <. -.1.0 || x >. 1.0 then None
    else Some (
        x -. 
        (x *. x *. x) /. 6.0 +.
        (3.0 *. x *. x *. x *. x *. x) /. 40.0 +.
        (5.0 *. x *. x *. x *. x *. x *. x *. x) /. 112.0 +.
        (35.0 *. x *. x *. x *. x *. x *. x *. x *. x) /. 1152.0)
```

