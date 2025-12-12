from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from ...classes.private_field import private_field

if TYPE_CHECKING:
    from attrs_circular_service import Service


@base_class
class BaseKernel(BaseClass):
    """Base kernel using attrs; creates its Service and initializes circular link."""

    debug: bool = public_field(
        default=False,
        description="Enable or disable debug mode for the kernel",
    )
    name: str = public_field(
        description="Name of the kernel instance",
    )
    _service: Service | None = private_field(
        default=None,
        description="Internal reference to the associated Service instance",
    )

    def __attrs_post_init__(self) -> None:
        service_cls = self.get_service_class()
        self._service = service_cls(name=f"{self.name}_service")
        self._service.initialize(self)

    @classmethod
    def get_service_class(cls) -> type[Service]:
        from attrs_circular_service import Service

        return Service

    @property
    def service(self) -> Service:
        assert self._service is not None
        return self._service
