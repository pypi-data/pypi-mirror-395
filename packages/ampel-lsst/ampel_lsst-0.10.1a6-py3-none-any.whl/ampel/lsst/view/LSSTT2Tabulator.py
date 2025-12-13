#!/usr/bin/env python
# File              : Ampel-LSST/ampel/lsst/view/LSSTT2Tabulator.py
# License           : BSD-3-Clause
# Author            : Marcus Fenner <mf@physik.hu-berlin.de>
# Date              : 25.05.2021
# Last Modified Date: 05.05.2022
# Last Modified By  : Marcus Fenner <mf@physik.hu-berlin.de>

import sys
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

import numpy as np
from astropy.table import Table

from ampel.abstract.AbsT2Tabulator import AbsT2Tabulator
from ampel.content.DataPoint import DataPoint
from ampel.types import StockId
from ampel.util.collections import ampel_iter

LSST_BANDPASSES = {
    "u": "lsstu",
    "g": "lsstg",
    "r": "lsstr",
    "i": "lssti",
    "z": "lsstz",
    "y": "lssty",
}


class LSSTT2Tabulator(AbsT2Tabulator):
    convert2jd: bool = True
    zp: float
    allow_nan_flux: bool = False
    # tag priority: lower index -> higher priority
    tags: Sequence[str | int] = ["LSST_FP", "LSST_DP"]
    """ """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tag_priority = {
            tag: index for index, tag in enumerate(self.tags)
        }

    def get_flux_table(
        self,
        dps: Iterable[DataPoint],
    ) -> Table:
        flux, fluxerr, filtername, tai = self.get_values(
            dps,
            ["psfFlux", "psfFluxErr", "band", "midpointMjdTai"],
            self._tag_priority,
        )
        if self.convert2jd:
            tai = self._to_jd(tai)
        filters = list(map(LSST_BANDPASSES.get, filtername))

        table = Table(
            {
                "time": tai,
                "flux": flux,
                "fluxerr": fluxerr,
                "band": filters,
                # ZP for ELAsTiCC, might need to be corrected for LSST!
                "zp": [self.zp] * len(filters),
                "zpsys": ["ab"] * len(filters),
            },
            dtype=("float64", "float64", "float64", "str", "float64", "str"),
        )

        if self.allow_nan_flux:
            return table
        return table[np.isfinite(table["flux"])]

    def get_positions(
        self, dps: Iterable[DataPoint]
    ) -> Sequence[tuple[float, float, float]]:
        return tuple(
            zip(
                self.get_jd(dps),
                *self.get_values(dps, ["ra", "dec"], self._tag_priority),
                strict=False,
            )
        )

    def get_jd(self, dps: Iterable[DataPoint]) -> Sequence[float]:
        return self._to_jd(
            self.get_values(dps, ["midpointMjdTai"], self._tag_priority)[0]
        )

    @staticmethod
    def _to_jd(dates: Sequence[Any]) -> Sequence[Any]:
        return [date + 2400000.5 for date in dates]

    def get_stock_id(self, dps: Iterable[DataPoint]) -> set[StockId]:
        return set(
            stockid
            for el in dps
            if "LSST" in el["tag"]
            for stockid in ampel_iter(el["stock"])
        )

    def get_stock_name(self, dps: Iterable[DataPoint]) -> list[str]:
        return [str(stock) for stock in self.get_stock_id(dps)]

    @staticmethod
    def _select_dps(
        dps: Iterable[DataPoint], tag_priority: Mapping[str | int, int]
    ) -> Iterable[DataPoint]:
        # select one datapoint per visit with highest tag priority
        selected_dps: dict[int, DataPoint] = {}
        for el in dps:
            if (tag_priority.keys() & el["tag"]) and (
                (key := el["body"]["midpointMjdTai"]) not in selected_dps
                or min(tag_priority.get(t, sys.maxsize) for t in el["tag"])
                < min(
                    tag_priority.get(t, sys.maxsize)
                    for t in selected_dps[key]["tag"]
                )
            ):
                selected_dps[key] = el
        return selected_dps.values()

    @staticmethod
    def get_values(
        dps: Iterable[DataPoint],
        params: Sequence[str],
        tag_priority: Mapping[str | int, int],
    ) -> tuple[Sequence[Any], ...]:
        if tup := tuple(
            map(
                list,
                zip(
                    *(
                        [el["body"][param] for param in params]
                        for el in LSSTT2Tabulator._select_dps(
                            dps, tag_priority
                        )
                    ),
                    strict=False,
                ),
            )
        ):
            return tup
        return tuple([[]] * len(params))
