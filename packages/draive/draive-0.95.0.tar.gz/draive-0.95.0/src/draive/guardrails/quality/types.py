from typing import Any, Protocol, runtime_checkable

from haiway import Meta, MetaValues

from draive.guardrails.types import GuardrailsException
from draive.multimodal import MultimodalContent

__all__ = (
    "GuardrailsQualityException",
    "GuardrailsQualityVerifying",
)


class GuardrailsQualityException(GuardrailsException):
    __slots__ = (
        "content",
        "reason",
    )

    def __init__(
        self,
        *args: object,
        reason: str,
        content: MultimodalContent,
        meta: Meta | MetaValues | None = None,
    ) -> None:
        super().__init__(*args, meta=meta)
        self.reason: str = reason
        self.content: MultimodalContent = content


@runtime_checkable
class GuardrailsQualityVerifying(Protocol):
    async def __call__(
        self,
        content: MultimodalContent,
        /,
        **extra: Any,
    ) -> None: ...
