# pyright: strict
# Dev-doc
# Most commands have a `--json` option that outputs the results in JSON format.
# The implmentation is done by making `typer.echo` a injected dependency.
import asyncio
import json as jsonlib
import os
import sys
from pathlib import Path
from typing import Annotated, Any, Literal, TypedDict, assert_never, cast

import typer
from imandrax_api_models import DecomposeRes, InstanceRes, VerifyRes
from imandrax_api_models.client import (
    ImandraXAsyncClient,
    get_imandrax_async_client,
    get_imandrax_client,
)
from imandrax_api_models.context_utils import (
    format_decomp_res,
    format_eval_res,
    format_vg_res,
    remove_art_and_task_fields,
)
from imandrax_api_models.logging_utils import configure_logging
from iml_query.processing import (
    extract_decomp_reqs,
    extract_instance_reqs,
    extract_verify_reqs,
)
from iml_query.processing.decomp import DecompReqArgs
from iml_query.tree_sitter_utils import get_parser

app = typer.Typer(name='ImandraX')


DEBUG = os.environ.get('DEBUG', '0') == '1'
"""Env var to enable debug logging."""

if DEBUG:
    configure_logging('debug')
else:
    configure_logging('warning')


def _remove_fields(data: dict[str, Any]) -> dict[str, Any]:
    """Resursively look inside a dict for certain keys and remove it."""
    data = data.copy()
    remove_fields = ['artifact', 'task', 'model']
    for k in list(data.keys()):
        v = data[k]
        if k in remove_fields:
            data.pop(k)
        elif isinstance(v, dict):
            v = cast(dict[str, Any], v)
            data[k] = _remove_fields(v)
    return data


def _load_iml(path: str | None) -> str:
    """Read IML code from a file or stdin."""
    if (path is None) or (path == '-'):
        # Read from stdin if no path is provided
        iml = sys.stdin.read()
    else:
        if not Path(path).exists():
            raise typer.BadParameter(f'IML file {path} does not exist')
        iml = Path(path).read_text()
    return iml


def ifprintf(message: Any | None) -> None:
    """Similar to OCmal's `ifprintf` function.

    Used to intercept stdout printing when "--json" is set.
    """
    pass


@app.command(
    name='check',
    help='Evaluate an IML file without VG and decomp.',
)
def check(
    file: Annotated[
        str | None,
        typer.Argument(
            help='Path of the IML file to evaluate. Set to "-" to read from stdin.',
        ),
    ] = None,
    with_vgs: Annotated[
        bool,
        typer.Option(
            help='Whether to strip verify and instance requests before evaluating.',
        ),
    ] = False,
    with_decomps: Annotated[
        bool,
        typer.Option(
            help='Whether to decomp requests before evaluating.',
        ),
    ] = False,
    json: Annotated[
        bool,
        typer.Option(
            help='Whether to output the results in JSON format.',
        ),
    ] = False,
):
    iml = _load_iml(file)

    c = get_imandrax_client()
    eval_res = c.eval_model(src=iml, with_vgs=with_vgs, with_decomps=with_decomps)
    if not json:
        typer.echo(format_eval_res(eval_res, iml))
    else:
        typer.echo(jsonlib.dumps(eval_res.model_dump(), indent=2))


# VG
# ====================


class VGItem(TypedDict):
    kind: Literal['verify', 'instance']
    src: str
    start_point: tuple[int, int]
    end_point: tuple[int, int]


def _collect_vgs(iml: str) -> list[VGItem]:
    tree = get_parser().parse(iml.encode('utf-8'))
    iml, tree, verify_reqs, verify_req_ranges = extract_verify_reqs(iml, tree)
    iml, tree, instance_reqs, instance_req_ranges = extract_instance_reqs(iml, tree)

    # Collect
    vg_items: list[VGItem] = []
    for req, req_range in zip(verify_reqs, verify_req_ranges, strict=True):
        vg_items.append(
            {
                'kind': 'verify',
                'src': req['src'],
                'start_point': (req_range.start_point[0], req_range.start_point[1]),
                'end_point': (req_range.end_point[0], req_range.end_point[1]),
            }
        )
    for req, req_range in zip(instance_reqs, instance_req_ranges, strict=False):
        vg_items.append(
            {
                'kind': 'instance',
                'src': req['src'],
                'start_point': (req_range.start_point[0], req_range.start_point[1]),
                'end_point': (req_range.end_point[0], req_range.end_point[1]),
            }
        )
    vg_items.sort(key=lambda x: x['start_point'])
    return vg_items


@app.command(
    name='list-vg',
    help='List verification goals in an IML file.',
)
def list_vg(
    file: Annotated[
        str | None,
        typer.Argument(
            help='Path of the IML file to check. Set to "-" to read from stdin.',
        ),
    ] = None,
    json: Annotated[
        bool,
        typer.Option(
            help='Whether to output the results in JSON format.',
        ),
    ] = False,
):
    iml = _load_iml(file)

    vgs: list[VGItem] = _collect_vgs(iml)

    if not json:
        for i, item in enumerate(vgs, 1):
            loc_str = (
                f'{item["start_point"][0]}:{item["start_point"][1]}'
                f'-{item["end_point"][0]}:{item["end_point"][1]}'
            )
            typer.echo(f'{i}: {item["kind"]} ({loc_str}): {item["src"]}')
    else:
        json_s = jsonlib.dumps(vgs, indent=2)
        typer.echo(json_s)


@app.command(
    name='check-vg',
    help='Check verification goals in an IML file.',
)
def check_vg(
    file: Annotated[
        str | None,
        typer.Argument(
            help='Path of the IML file to check. Set to "-" to read from stdin.',
        ),
    ] = None,
    index: Annotated[
        list[int] | None,
        typer.Option(
            help='Name of the verification goal to check.',
        ),
    ] = None,
    check_all: Annotated[
        bool,
        typer.Option(
            help='Whether to check all verify requests in the IML file.',
        ),
    ] = False,
    json: Annotated[
        bool,
        typer.Option(
            help='Whether to output the results in JSON format.',
        ),
    ] = False,
):
    index = index or []

    if not json:
        echo = typer.echo
    else:
        echo = ifprintf

    async def _async_check_vg() -> list[VerifyRes | InstanceRes]:
        iml = _load_iml(file)
        vgs = _collect_vgs(iml)

        index_: list[int] = (
            list(range(1, len(vgs) + 1)) if check_all or (len(index) == 0) else index
        )

        vg_with_idx: list[tuple[int, VGItem]] = [
            (i, vg) for (i, vg) in enumerate(vgs, 1) if i in index_
        ]

        async def _check_vg(
            vg: VGItem,
            i: int,
            c: ImandraXAsyncClient,
        ) -> VerifyRes | InstanceRes:
            match vg['kind']:
                case 'verify':
                    res = await c.verify_src(src=vg['src'])
                case 'instance':
                    res = await c.instance_src(src=vg['src'])
                case _:
                    assert_never(vg['kind'])
            echo(f'{i}: {vg["kind"]} ({vg["src"]})')
            echo(format_vg_res(res))
            return res

        async with get_imandrax_async_client() as c:
            eval_res = await c.eval_model(src=iml)
            echo(format_eval_res(eval_res, iml))
            if eval_res.has_errors:
                echo('Error(s) found in IML file. Exiting.')
                sys.exit(1)
                return
            echo('\n' + '=' * 5 + 'VG' + '=' * 5 + '\n')
            tasks = [_check_vg(vg, i, c) for (i, vg) in vg_with_idx]
            return await asyncio.gather(*tasks)

    vg_res_list: list[VerifyRes | InstanceRes] = asyncio.run(_async_check_vg())
    if json:
        out = [_remove_fields(vg_res.model_dump()) for vg_res in vg_res_list]
        typer.echo(jsonlib.dumps(out, indent=2, skipkeys=True))


# decomp
# ====================


class DecompItem(TypedDict):
    req_args: DecompReqArgs
    start_point: tuple[int, int]
    end_point: tuple[int, int]


def _collect_decomps(iml: str) -> list[DecompItem]:
    tree = get_parser().parse(iml.encode('utf-8'))
    iml, tree, decomp_reqs, ranges = extract_decomp_reqs(iml, tree)

    decomp_items: list[DecompItem] = [
        DecompItem(
            req_args=req,
            start_point=range_.start_point,
            end_point=range_.end_point,
        )
        for req, range_ in zip(decomp_reqs, ranges, strict=True)
    ]

    decomp_items.sort(key=lambda x: x['start_point'])
    return decomp_items


@app.command(
    name='list-decomp',
    help='List decomp requests in an IML file.',
)
def list_decomp(
    file: Annotated[
        str | None,
        typer.Argument(
            help='Path of the IML file to check. Set to "-" to read from stdin.',
        ),
    ] = None,
    json: Annotated[
        bool,
        typer.Option(
            help='Whether to output the results in JSON format.',
        ),
    ] = False,
):
    iml = _load_iml(file)
    decomps = _collect_decomps(iml)

    if not json:
        for i, item in enumerate(decomps, 1):
            typer.echo(f'{i}: {item["req_args"]["name"]}')
    else:
        json_s = jsonlib.dumps(decomps, indent=2)
        typer.echo(json_s)


@app.command(
    name='check-decomp',
    help='Check decomp requests in an IML file.',
)
def check_decomp(
    file: Annotated[
        str | None,
        typer.Argument(
            help='Path of the IML file to check. Set to "-" to read from stdin.',
        ),
    ] = None,
    index: Annotated[
        list[int] | None,
        typer.Option(
            help='Index of the decomposition request to check.',
        ),
    ] = None,
    check_all: Annotated[
        bool,
        typer.Option(
            help='Whether to check all decomp requests in the IML file.',
        ),
    ] = False,
    json: Annotated[
        bool,
        typer.Option(
            help='Whether to output the results in JSON format.',
        ),
    ] = False,
):
    index = index or []

    if not json:
        echo = typer.echo
    else:
        echo = ifprintf

    async def _async_check_decomp() -> list[DecomposeRes]:
        iml = _load_iml(file)
        decomps = _collect_decomps(iml)

        index_: list[int] = (
            list(range(1, len(decomps) + 1))
            if check_all or (len(index) == 0)
            else index
        )

        decomp_with_idx: list[tuple[int, DecompItem]] = [
            (i, decomp) for (i, decomp) in enumerate(decomps, 1) if i in index_
        ]

        async def _check_decomp(
            decomp: DecompItem, i: int, c: ImandraXAsyncClient
        ) -> DecomposeRes:
            echo(f'{i}: decompose {decomp["req_args"]["name"]}')
            res = await c.decompose(**decomp['req_args'])
            echo(format_decomp_res(res))
            return res

        async with get_imandrax_async_client() as c:
            eval_res = await c.eval_model(src=iml)
            echo(format_eval_res(eval_res, iml))
            if eval_res.has_errors:
                typer.echo('Error(s) found in IML file. Exiting.')
                sys.exit(1)
                return

            echo('\n' + '=' * 5 + 'Decomp' + '=' * 5 + '\n')
            tasks = [_check_decomp(decomp, i, c) for (i, decomp) in decomp_with_idx]
            return await asyncio.gather(*tasks)

    decomp_res_list: list[DecomposeRes] = asyncio.run(_async_check_decomp())

    if json:
        out = [
            remove_art_and_task_fields(decomp_res.model_dump())
            for decomp_res in decomp_res_list
        ]
        typer.echo(jsonlib.dumps(out, indent=2))


if __name__ == '__main__':
    app()
