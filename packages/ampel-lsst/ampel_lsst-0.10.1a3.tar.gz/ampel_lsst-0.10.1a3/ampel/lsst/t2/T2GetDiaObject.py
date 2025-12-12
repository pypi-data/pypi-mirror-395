#!/usr/bin/env python
# File:                Ampel-LSST/ampel/lsst/t2/T2GetDiaObject.py
# License:             BSD-3-Clause
# Author:              Marcus Fennner <mf@physik.hu-berlinn.de>
# Date:                22.03.2022
# Last Modified Date:  22.06.2022
# Last Modified By:    jno <jnordin@physik.hu-berlinn.de>

from typing import TYPE_CHECKING, ClassVar

from ampel.abstract.AbsPointT2Unit import AbsPointT2Unit
from ampel.content.DataPoint import DataPoint
from ampel.model.DPSelection import DPSelection
from ampel.protocol.LoggerProtocol import LoggerProtocol
from ampel.types import UBson


class T2GetDiaObject(AbsPointT2Unit):
    """
    Get information from a LSST transient's diaObject to use in other T2
    """

    eligible: ClassVar[DPSelection] = DPSelection(
        filter="LSSTObjFilter", sort="diaObjectId", select="last"
    )
    params: list[str]

    if TYPE_CHECKING:
        logger: LoggerProtocol

    def process(self, datapoint: DataPoint) -> UBson:
        return {param: datapoint["body"].get(param) for param in self.params}
