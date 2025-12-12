from __future__ import annotations

from typing import TYPE_CHECKING

from ...decorator.base_class import base_class

if TYPE_CHECKING:
    from .attrs_circular_base_kernel import AdvancedKernel, BaseKernel


@base_class
class Service:
    kernel: BaseKernel | None = None
    name: str

    @property
    def advanced_kernel(self) -> AdvancedKernel | None:
        # Only available when attached to an AdvancedKernel
        k = self.kernel
        if k is not None and k.__class__.__name__ == "AdvancedKernel":
            # Avoid direct import to keep circular hints safe at runtime
            return k  # type: ignore[return-value]
        return None

    @property
    def base_kernel(self) -> BaseKernel | None:
        return self.kernel

    @property
    def mode(self) -> str:
        return "basic"

    def initialize(self, kernel: BaseKernel) -> None:
        self.kernel = kernel


@base_class
class AdvancedService(Service):
    @property
    def mode(self) -> str:
        return "advanced"
