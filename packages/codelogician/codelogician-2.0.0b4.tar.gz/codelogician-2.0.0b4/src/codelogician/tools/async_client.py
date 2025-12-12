import os
from pathlib import Path
from typing import Any, Literal

import imandrax_api
import structlog
from imandrax_api import AsyncClient  # type: ignore[attr-defined]
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
) -> AsyncClient:
    imandrax_env = env or os.getenv("IMANDRAX_ENV", "prod")
    if imandrax_env == "dev":
        url = imandrax_api.url_dev
    else:
        url = imandrax_api.url_prod

    imandrax_api_key = imandra_api_key or os.getenv("IMANDRAX_API_KEY")

    if not imandrax_api_key:
        # try to read from default config location
        config_path = Path.home() / ".config" / "imandrax" / "api_key"
        if config_path.exists():
            imandrax_api_key = config_path.read_text().strip()

    if not imandrax_api_key:
        logger.error("IMANDRAX_API_KEY is None")
        raise ValueError("IMANDRAX_API_KEY is None")
    client = AsyncClient(url=url, auth_token=imandrax_api_key, timeout=300)
    logger.info("imandrax_client_initialized", env=imandrax_env)
    return client


async def eval_src(
    imx_client: AsyncClient,
    src: str,
    timeout: float | None = None,
) -> EvalRes:
    res = await imx_client.eval_src(src=src, timeout=timeout)
    return EvalRes.model_validate(proto_to_dict(res))


async def typecheck(
    imx_client: AsyncClient, src: str, timeout: float | None = None
) -> TypecheckRes:
    res = await imx_client.typecheck(src=src, timeout=timeout)
    return TypecheckRes.model_validate(proto_to_dict(res))


async def decompose(
    imx_client: AsyncClient,
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

    res = await imx_client.decompose(
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


async def verify_src(
    imx_client: AsyncClient,
    src: str,
    hints: str | None = None,
    timeout: float | None = None,
) -> VerifyRes:
    res = await imx_client.verify_src(src=src, hints=hints, timeout=timeout)
    return VerifyRes.model_validate(proto_to_dict(res))


async def verify_src_catching_internal_error (
    imx_client: AsyncClient,
    src: str,
    hints: str | None = None,
    timeout: float | None = None,
) -> VerifyRes:
    try:
        return await verify_src(imx_client, src, hints, timeout)
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


async def instance_src (
    imx_client: AsyncClient,
    src: str,
    hints: str | None = None,
    timeout: float | None = None,
) -> InstanceRes:
    res = await imx_client.instance_src(src=src, hints=hints, timeout=timeout)
    return InstanceRes.model_validate(proto_to_dict(res))
