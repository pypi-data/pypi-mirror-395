#
#   Imandra Inc.
#
#   utils.py
#

from typing import cast

from .proto_models import Error, ErrorMessage, EvalRes


def _error_msg_to_llm_context(
    error_msg: ErrorMessage,
    max_backtrace_len: int = 0,
) -> str:
    locs = error_msg.locs if error_msg.locs else []
    loc_strs: list[str] = [
        (f"({loc.start.line}, {loc.start.col}) - ({loc.stop.line}, {loc.stop.col})")
        for loc in locs
        if (loc.start is not None and loc.stop is not None)
    ]
    loc_str = "; ".join(loc_strs) if loc_strs else ""

    res = f"{error_msg.msg}"
    if loc_str:
        res += f"\nlocs: {loc_str}"
    if error_msg.backtrace and max_backtrace_len > 0:
        res += f"\nbacktrace: {error_msg.backtrace[:max_backtrace_len]}"
    return res


def error_to_llm_context(error: Error, max_stack_depth: int = 3) -> str:
    err_kind = error.kind
    top_msg: str | None = None
    if error.msg is not None:
        top_msg = _error_msg_to_llm_context(error.msg)
    stack_strs = (
        [_error_msg_to_llm_context(msg) for msg in error.stack[:max_stack_depth]]
        if error.stack
        else []
    )
    stack_str = "\n".join(stack_strs)

    s = ""
    s += f"{top_msg}" if top_msg else ""
    s += f"\n<kind>{err_kind}</kind>" if err_kind else ""
    s += f"\n<stack>\n{stack_str}\n</stack>" if stack_str else ""

    return s


def eval_res_errors_to_llm_context(
    eval_res: EvalRes, max_errors: int = 3
) -> str | None:
    po_errors = eval_res.po_errors
    if not eval_res.errors and not po_errors:
        return None

    errs: list[str] = [error_to_llm_context(err) for err in eval_res.errors]
    po_errs = [error_to_llm_context(err) for err in po_errors]

    res = ""
    for i, err in enumerate(errs[:max_errors], 1):
        res += f"<error_{i}>\n{err}\n</error_{i}>\n\n"
    if po_errors:
        res += "Proof obligation errors (including termination proving errors):\n\n"
    for i, err in enumerate(po_errs[:max_errors], 1):
        res += f"<po_error_{i}>\n{err}\n</po_error_{i}>\n\n"
    return res


def eval_res_to_llm_context(eval_res: EvalRes) -> str:
    if not eval_res.has_errors:
        s = "Success!"
        if eval_res.eval_results:
            s += "\n"
        for i, eval_result in enumerate(eval_res.eval_results, 1):
            s += f"\nEval result #{i}:\n"
            s += f"- success: {eval_result.success}\n"
            s += f"- value as ocaml: {eval_result.value_as_ocaml}\n"
            if eval_result.errors:
                s += "errors:\n"
                for err in eval_result.errors:
                    s += f"- {error_to_llm_context(err)}\n"
        return s

    else:
        s = ""
        s += "Evaluation errors:\n\n"
        s += cast(str, eval_res_errors_to_llm_context(eval_res))
        return s