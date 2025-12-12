# ruff: noqa: E702
import json
import os
from collections.abc import Callable, Iterable
from itertools import groupby
from typing import TypeVar

T = TypeVar('T')
U = TypeVar('U')


# fmt: off
def member[T](xs: Iterable[T]) -> Callable[[T], bool]: return lambda x: x in xs
def fst[T, U](xy: tuple[T, U]) -> T: x, _ = xy; return x
def snd[T, U](xy: tuple[T, U]) -> U: _, y = xy; return y
def swap[T, U](xy: tuple[T, U]) -> tuple[U, T]: x, y = xy; return y, x
def dup[T](x: T) -> tuple[T, T]: return x, x
def distrib(xys): return [(x, y) for x, ys in xys for y in ys]
def not_none(x): return x is not None
def guard(f, x): return x if f(x) else None
def maybe[T, U](f: Callable[[T], U], x: T | None) -> U | None: return None if x is None else f(x)
def maybe_else[T, U](y: U, f: Callable[[T], U], x: T | None) -> U: return y if x is None else f(x)
def head(x): return next(iter(x), None)
def filter(p, xs): return [x for x in xs if p(x)]
def rev(items): return list(reversed(list(items)))
def flat_map(f, xs): return [y for x in xs for y in f(x)]
def unzip(pairs): return [x for x, _ in pairs], [y for _, y in pairs]
def map[T, U](f: Callable[[T], U], xs: Iterable[T]) -> list[U]: return [f(x) for x in xs]
def dict_keys(d): return list(d.keys())
def dict_values(d): return list(d.values())
def map_values(f, d): return {k: f(v) for k, v in d.items()}
def consult_or(z, d): return lambda x: d.get(x, z)
def splice[T](f: Callable[..., T]) -> Callable[[Iterable], T]: return lambda args: f(*args)
def json_read(f): return json.loads(text_read(f))
def text_read(f: str) -> str:
    with open(f) as s: return s.read()

def intersperse(sep, xs):
    yield next(xs)
    for x in xs:
        yield sep
        yield x

def group_snd_by_fst(pairs):
    return [(x, map(snd, y)) for x, y in groupby(sorted(pairs, key=fst), key=fst)]

def mdict(pairs): return dict(group_snd_by_fst(pairs))

def lazy(f):
    cell = [None]
    def g():
        if cell[0] is None:
            cell[0] = f()
        return cell[0]
    return g


def show(x):
    from rich.console import Console
    from rich.pretty import Pretty

    r = (x.__rich__() if hasattr(x, '__rich__') else
         x if hasattr(x, '__rich_console__') else
         Pretty(x))
    width = int(os.popen('stty size', 'r').read().split(' ')[1])
    with Console(width=width) as c:
        c.print(r)
# fmt: on


def get_imandra_uni_key() -> str:
    key = os.getenv('IMANDRA_UNI_KEY')
    if not key:
        raise ValueError("CodeLogician requires 'IMANDRA_UNI_KEY' to be set!")
    return key
