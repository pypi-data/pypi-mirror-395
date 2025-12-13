from collections.abc import Generator, Iterable

from ampel.base.AmpelBaseModel import AmpelBaseModel


class StringFilter(AmpelBaseModel):
    include: None | set[str] = None
    exclude: None | set[str] = None

    def filter(self, fields: Iterable[str]) -> Generator[str, None, None]:
        for field in fields:
            if self.include is not None and field not in self.include:
                continue
            if self.exclude is not None and field in self.exclude:
                continue
            yield field


class FieldSelection(AmpelBaseModel):
    """
    Field selection for LSST data points
    """

    diaSource: None | StringFilter = None
    diaForcedSource: None | StringFilter = None
    diaObject: None | StringFilter = None
    diaNondetectionLimit: None | StringFilter = None

    @classmethod
    def default(cls) -> "FieldSelection":
        return FieldSelection(
            diaSource=StringFilter(
                include={
                    "band",
                    "dec",
                    "isNegative",
                    "midpointMjdTai",
                    "psfFlux",
                    "psfFluxErr",
                    "ra",
                    "snr",
                    "visit",
                    "diaSourceId",
                },
                exclude=None,
            ),
            diaForcedSource=StringFilter(
                include={
                    "band",
                    "dec",
                    "midpointMjdTai",
                    "psfFlux",
                    "psfFluxErr",
                    "ra",
                    "visit",
                    "diaForcedSourceId",
                },
                exclude=None,
            ),
            diaObject=StringFilter(
                include={
                    "dec",
                    "decErr",
                    "ra_dec_Cov",
                    "ra",
                    "radecMjdTai",
                    "raErr",
                    "diaObjectId",
                },
                exclude=None,
            ),
            diaNondetectionLimit=None,
        )
