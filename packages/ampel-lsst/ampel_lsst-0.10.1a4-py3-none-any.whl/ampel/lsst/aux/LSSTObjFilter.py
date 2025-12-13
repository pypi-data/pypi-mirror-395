#!/usr/bin/env python
# File              : Ampel-LSST/ampel/lsst/aux/LSSTobjFilter.py
# License           : BSD-3-Clause
# Author            : Marcus Fenner <mf@physik.hu-berlin.de>
# Date              : 22.03.2022
# Last Modified Date: 22.03.2022
# Last Modified By  : Marcus Fenner <mf@physik.hu-berlin.de>


from ampel.abstract.AbsApplicable import AbsApplicable
from ampel.content.DataPoint import DataPoint


class LSSTObjFilter(AbsApplicable):
    """
    Get diaObject for metadata
    """

    def apply(self, arg: list[DataPoint]) -> list[DataPoint]:
        return [el for el in arg if "LSST_OBJ" in el["tag"]]
