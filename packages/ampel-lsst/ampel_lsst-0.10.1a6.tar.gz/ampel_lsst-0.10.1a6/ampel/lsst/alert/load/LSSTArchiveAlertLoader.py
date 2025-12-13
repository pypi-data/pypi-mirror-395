from collections.abc import Iterator
from functools import cached_property
from typing import Annotated, Any

from pydantic import Field
from requests_toolbelt.sessions import (  # type: ignore[import-untyped]
    BaseUrlSession,
)

from ampel.abstract.AbsAlertLoader import AbsAlertLoader
from ampel.log.AmpelLogger import AmpelLogger


class LSSTArchiveAlertLoader(AbsAlertLoader[dict]):
    """
    Load alerts from LSST alert archive
    """

    archive_url: str = (
        "https://ampel-dev.ia.zeuthen.desy.de/api/lsst/archive/v1/"
    )
    insecure: Annotated[
        bool, Field(description="Do not verify HTTPS certificates")
    ] = False

    condition: Annotated[
        str, Field(description="SQL condition for alert query")
    ]
    order_by: Annotated[
        None | str, Field(description="Order by clause for alert query")
    ] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._it: None | Iterator[dict] = None

    def set_logger(self, logger: AmpelLogger) -> None:
        super().set_logger(logger)

    @cached_property
    def session(self) -> BaseUrlSession:
        return BaseUrlSession(base_url=self.archive_url)

    def _build_query(
        self, condition: str, limit: None | int = None
    ) -> dict[str, Any]:
        exclude = [
            "cutoutTemplate",
            "cutoutScience",
            "cutoutDifference",
        ]
        return {
            "exclude": exclude,
            "condition": condition,
            "order": self.order_by,
            "limit": limit,
        }

    def alerts(self, limit: None | int = None) -> Iterator[dict]:
        """
        Generate alerts until timeout is reached
        :returns: dict instance of the alert content
        :raises StopIteration: when no alerts recieved within timeout
        """

        response = self.session.post(
            "display/alerts/query",
            json=self._build_query(self.condition, limit=limit),
            verify=not self.insecure,
        )
        try:
            response.raise_for_status()
        except Exception:
            self.logger.error(
                f"Error querying LSST alert archive: {response.json()}"
            )
            raise

        yield from response.json()

    def __next__(self) -> dict:
        if self._it is None:
            self._it = self.alerts()
        return next(self._it)
