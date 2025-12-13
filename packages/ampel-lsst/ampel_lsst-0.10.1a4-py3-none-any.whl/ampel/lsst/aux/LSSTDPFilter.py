#!/usr/bin/env python
# File              : Ampel-LSST/ampel/lsst/aux/LSSTDPFilter.py
# License           : BSD-3-Clause
# Author            : Marcus Fenner <mf@physik.hu-berlin.de>
# Date              : 15.09.2021
# Last Modified Date: 28.02.2022
# Last Modified By  : Marcus Fenner <mf@physik.hu-berlin.de>


from ampel.abstract.AbsApplicable import AbsApplicable
from ampel.content.DataPoint import DataPoint


class LSSTDPFilter(AbsApplicable):
    """
    Only get LSST (not forced photometry) datapoints
    """

    def apply(self, arg: list[DataPoint]) -> list[DataPoint]:
        return [el for el in arg if "LSST_DP" in el["tag"]]
