#
#   Imandra Inc.
#
#   client.py
#
import os
from pathlib import Path
from typing import Any, Literal

import imandrax_api
import structlog
from imandrax_api.twirp.exceptions import TwirpServerException

from .proto_models import (
    DecomposeRes,
    Error,
    ErrorMessage,
    EvalRes,
    InstanceRes,
    TypecheckRes,
    VerifyRes,
)
from .proto_to_dict import proto_to_dict

logger = structlog.get_logger(__name__)


def get_imandrax_client(
    imandra_api_key: str | None = None,
    env: Literal["dev", "prod"] | None = None,
) -> imandrax_api.Client:
    imandrax_env = env or os.getenv("IMANDRA_UNI_KEY", "prod")
    if imandrax_env == "dev":
        url = imandrax_api.url_dev
    elif imandrax_env == "prod":
        url = imandrax_api.url_prod
    else:
        url = os.getenv("IMANDRAX_URL")
        if not url:
            raise ValueError("IMANDRAX_URL is not set")

    imandrax_api_key = imandra_api_key or os.getenv("IMANDRA_UNI_KEY")
    if not imandrax_api_key:
        # try to read from default config location
        config_path = Path.home() / ".config" / "imandrax" / "api_key"
        if config_path.exists():
            imandrax_api_key = config_path.read_text().strip()

    if not imandrax_api_key:
        logger.error("IMANDRA_UNI_KEY is None")
        raise ValueError("IMANDRA_UNI_KEY is None")
    client = imandrax_api.Client(url=url, auth_token=imandrax_api_key, timeout=300)
    logger.info("imandrax_client_initialized", env=imandrax_env)
    return client


def eval_src(
    imx_client: imandrax_api.Client,
    src: str,
    timeout: float | None = None,
) -> EvalRes:
    res = imx_client.eval_src(src=src, timeout=timeout)
    return EvalRes.model_validate(proto_to_dict(res))


def typecheck(
    imx_client: imandrax_api.Client, src: str, timeout: float | None = None
) -> TypecheckRes:
    """Typecheck IML code.

    No eval_src is needed before typecheck.

    Example:
        >>> iml_code = '''\
        ... let f x = x + 1
        ...
        ... let g x = f x + 1
        ... '''
        >>> typecheck(imx_client, iml_code)
        TypecheckRes(success=True, types=[InferredType(name='g', ty='int -> int', line=3, column=1), InferredType(name='f', ty='int -> int', line=1, column=1)], errors=None)
    """  # noqa: E501
    res = imx_client.typecheck(src=src, timeout=timeout)
    typecheck_res = TypecheckRes.model_validate(proto_to_dict(res))
    return typecheck_res


def decompose(
    imx_client: imandrax_api.Client,
    name: str,
    assuming: str | None = None,
    basis: list[str] | None = None,
    rule_specs: list[str] | None = None,
    prune: bool | None = True,
    ctx_simp: bool | None = None,
    lift_bool: Any | None = None,
    timeout: float | None = None,
    str: bool | None = True,
) -> DecomposeRes:
    if basis is None:
        basis = []
    if rule_specs is None:
        rule_specs = []

    res = imx_client.decompose(
        name=name,
        basis=basis,
        rule_specs=rule_specs,
        prune=prune,
        ctx_simp=ctx_simp,
        lift_bool=lift_bool,
        timeout=timeout,
        str=str,
    )
    return DecomposeRes.model_validate(proto_to_dict(res))


def verify_src(
    imx_client: imandrax_api.Client,
    src: str,
    hints: str | None = None,
    timeout: float | None = None,
) -> VerifyRes:
    res = imx_client.verify_src(src=src, hints=hints, timeout=timeout)
    return VerifyRes.model_validate(proto_to_dict(res))


def verify_src_catching_internal_error(
    imx_client: imandrax_api.Client,
    src: str,
    hints: str | None = None,
    timeout: float | None = None,
) -> VerifyRes:
    try:
        return verify_src(imx_client, src, hints, timeout)
    except TwirpServerException as e:
        if e.message == "Internal Server Error":
            return VerifyRes(
                errors=[
                    Error(
                        msg=ErrorMessage(msg=e.to_dict()["meta"]["body"]),
                        kind="verify_internal",
                    )
                ]
            )
        raise e


def instance_src(
    imx_client: imandrax_api.Client,
    src: str,
    hints: str | None = None,
    timeout: float | None = None,
) -> InstanceRes:
    res = imx_client.instance_src(src=src, hints=hints, timeout=timeout)
    return InstanceRes.model_validate(proto_to_dict(res))
