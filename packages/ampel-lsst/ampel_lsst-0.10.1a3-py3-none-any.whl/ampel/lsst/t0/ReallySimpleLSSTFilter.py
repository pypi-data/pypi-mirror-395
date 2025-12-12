#!/usr/bin/env python
# File:                Ampel-ZTF/ampel/lsst/t0/ReallySimpleLSSTFilter.py
# License:             BSD-3-Clause
# Author:              Marcus Fenner <mf@physik.hu-berlin.de>
# Date:                24.03.2022
# Last Modified Date:  24.03.2022
# Last Modified By:    Marcus Fenner <mf@physik.hu-berlin.de>


from ampel.abstract.AbsAlertFilter import AbsAlertFilter
from ampel.protocol.AmpelAlertProtocol import AmpelAlertProtocol


class ReallySimpleLSSTFilter(AbsAlertFilter):
    """
    ELASTICC specific filter. It selects alerts based on:
    * numper of previous detections
    """

    # History
    min_ndet: int  # number of previous detections
    max_ndet: None | int  # number of previous detections
    min_tspan: float  # minimum duration of alert detection history [days]
    max_tspan: float  # maximum duration of alert detection history [days]

    def post_init(self):
        # feedback
        for k in self.__annotations__:
            self.logger.info(f"Using {k}={getattr(self, k)}")

        # To make this tenable we should create this list dynamically depending on what entries are required
        # by the filter. Now deciding not to include drb in this list, eg.
        self.keys_to_check = ("midpointMjdTai",)

    def _alert_has_keys(self, photop) -> bool:
        """
        check that given photopoint contains all the keys needed to filter
        """
        for el in self.keys_to_check:
            if el not in photop:
                self.logger.info(None, extra={"missing": el})
                return False
            if photop[el] is None:
                self.logger.info(None, extra={"isNone": el})
                return False
        return True

    # Override
    def process(self, alert: AmpelAlertProtocol) -> None | bool:
        """
        Mandatory implementation.
        To exclude the alert, return *None*
        To accept it, either return
        * self.on_match_t2_units
        * or a custom combination of T2 unit names
        """

        pps = [
            el for el in alert.datapoints if el.get("diaSourceId") is not None
        ]
        if len(pps) < self.min_ndet:
            self.logger.info(None, extra={"nDet": len(pps)})
            return None
        if self.max_ndet and len(pps) > self.max_ndet:
            self.logger.info(None, extra={"nDet": len(pps)})
            return None

        # cut on length of detection history
        detections_jds = [el["midpointMjdTai"] for el in pps]
        last_det = max(detections_jds)
        det_tspan = last_det - min(detections_jds)
        if not (self.min_tspan <= det_tspan <= self.max_tspan):
            self.logger.info(None, extra={"tSpan": det_tspan})
            return None

        self.logger.debug("Alert accepted", extra={"midpointMjdTai": last_det})
        return True
