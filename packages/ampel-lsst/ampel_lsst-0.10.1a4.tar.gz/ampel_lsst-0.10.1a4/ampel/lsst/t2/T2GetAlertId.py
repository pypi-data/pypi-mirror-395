#!/usr/bin/env python
# File:                Ampel-LSST/ampel/lsst/t2/T2GetAlertId.py
# License:             BSD-3-Clause
# Author:              Marcus Fennner <mf@physik.hu-berlinn.de>
# Date:                31.03.2022
# Last Modified Date:  31.03.2022
# Last Modified By:    Marcus Fennner <mf@physik.hu-berlinn.de>

from collections.abc import Sequence
from typing import ClassVar, Literal

from ampel.abstract.AbsTiedPointT2Unit import AbsTiedPointT2Unit
from ampel.content.DataPoint import DataPoint
from ampel.model.DPSelection import DPSelection
from ampel.model.UnitModel import UnitModel
from ampel.types import UBson
from ampel.view.T2DocView import T2DocView


class T2GetAlertId(AbsTiedPointT2Unit):
    """
    Get first alertId associated with the latest datapoint in a T1
    """

    eligible: ClassVar[DPSelection] = DPSelection(
        filter="LSSTDPFilter", sort="diaSourceId", select="last"
    )
    t2_dependency: Sequence[UnitModel[Literal["T2GetAlertJournal"]]]

    def process(
        self, datapoint: DataPoint, t2_views: Sequence[T2DocView]
    ) -> UBson:
        sourceid = datapoint["body"]["diaSourceId"]
        t0journals: list[dict] = []
        for t2_view in t2_views:
            if t2_view.unit != "T2GetAlertJournal":
                continue
            payload = t2_view.get_payload()
            assert isinstance(payload, list)
            for journal in payload:
                if "upsert" in journal and sourceid in journal["upsert"]:
                    t0journals += [journal]
        if not t0journals:
            return {}
        t0journals.sort(key=lambda x: x["ts"])
        runids = set([t0journal["run"] for t0journal in t0journals])
        if len(runids) > 1:
            self.logger.warn(
                f"Multiple runids found {runids}, assuming latest"
            )
            t0journals = [
                journal
                for journal in t0journals
                if journal["run"] == sorted(runids)[-1]
            ]
        first = t0journals[0]
        return {"ts": first["ts"], "alertId": first["alert"]}
