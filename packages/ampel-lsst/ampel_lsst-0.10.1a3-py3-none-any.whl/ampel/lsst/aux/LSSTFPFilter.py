#!/usr/bin/env python
# File              : Ampel-LSST/ampel/lsst/aux/LSSTFPFilter.py
# License           : BSD-3-Clause
# Author            : Marcus Fenner <mf@physik.hu-berlin.de>
# Date              : 15.09.2021
# Last Modified Date: 15.09.2021
# Last Modified By  : Marcus Fenner <mf@physik.hu-berlin.de>


from ampel.abstract.AbsApplicable import AbsApplicable
from ampel.content.DataPoint import DataPoint


class LSSTFPFilter(AbsApplicable):
    """
    Only get LSST's forced photometry datapoints
    """

    def apply(self, arg: list[DataPoint]) -> list[DataPoint]:
        return [el for el in arg if "LSST_FP" in el["tag"]]
