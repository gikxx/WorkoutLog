from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi.responses import JSONResponse


def problem(
    status: int,
    title: str,
    detail: str,
    type_: str = "about:blank",
    instance: Optional[str] = None,
    extras: Optional[Dict[str, Any]] = None,
) -> JSONResponse:
    """
    RFC 7807 compliant error response
    """
    correlation_id = str(uuid4())
    payload = {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail,
        "correlation_id": correlation_id,
        "instance": instance or f"/errors/{correlation_id}",
    }
    if extras:
        payload.update(extras)

    return JSONResponse(
        status_code=status,
        content=payload,
        headers={
            "X-Correlation-ID": correlation_id,
            "Content-Type": "application/problem+json",
        },
    )
