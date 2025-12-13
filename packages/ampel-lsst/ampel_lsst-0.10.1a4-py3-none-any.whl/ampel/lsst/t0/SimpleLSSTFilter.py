#!/usr/bin/env python
# File:                Ampel-LSST/ampel/lsst/t0/SimpleLSSTFilter.py
# License:             BSD-3-Clause
# Author:              m. giomi <matteo.giomi@desy.de>
# Date:                06.06.2018
# Last Modified Date:  24.03.2022
# Last Modified By:    Marcus Fenner <mf@physik.hu-berlin.de>

from typing import Any

import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Table

from ampel.abstract.AbsAlertFilter import AbsAlertFilter
from ampel.protocol.AmpelAlertProtocol import AmpelAlertProtocol
from ampel.ztf.base.CatalogMatchUnit import CatalogMatchUnit


class SimpleLSSTFilter(CatalogMatchUnit, AbsAlertFilter):
    """
    General-purpose filter. It selects alerts based on:
    * numper of previous detections
    * distance to known SS objects
    * detection of proper-motion and paralax for coincidence sources in GAIA DR2

    """

    # History
    min_ndet: int  # number of previous detections
    min_tspan: float  # minimum duration of alert detection history [days]
    max_tspan: float  # maximum duration of alert detection history [days]
    min_archive_tspan: float = (
        0.0  # minimum duration of alert detection history [days]
    )
    max_archive_tspan: float = (
        10**5.0
    )  # maximum duration of alert detection history [days]

    # Astro
    #    min_sso_dist: float  # distance to nearest solar system object [arcsec]
    min_gal_lat: float  # minium distance from galactic plane. Set to negative to disable cut.

    # Gaia
    gaia_rs: float  # search radius for GAIA DR2 matching [arcsec]
    gaia_pm_signif: float  # significance of proper motion detection of GAIA counterpart [sigma]
    gaia_plx_signif: (
        float  # significance of parallax detection of GAIA counterpart [sigma]
    )
    gaia_veto_gmag_min: float  # min gmag for normalized distance cut of GAIA counterparts [mag]
    gaia_veto_gmag_max: float  # max gmag for normalized distance cut of GAIA counterparts [mag]
    gaia_excessnoise_sig_max: float  # maximum allowed noise (expressed as significance) for Gaia match to be trusted.

    def post_init(self):
        # feedback
        for k in self.__annotations__:
            self.logger.info(f"Using {k}={getattr(self, k)}")

        # To make this tenable we should create this list dynamically depending on what entries are required
        # by the filter. Now deciding not to include drb in this list, eg.
        self.keys_to_check = (
            "midpointMjdTai",
            "ra",
            "decl",
        )

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

    def get_galactic_latitude(self, transient):
        """
        compute galactic latitude of the transient
        """
        coordinates = SkyCoord(transient["ra"], transient["decl"], unit="deg")
        return coordinates.galactic.b.deg

    def is_star_in_gaia(self, transient: dict[str, Any]) -> bool:
        """
        match tranient position with GAIA DR2 and uses parallax
        and proper motion to evaluate star-likeliness
        returns: True (is a star) or False otehrwise.
        """

        srcs = self.cone_search_all(
            transient["ra"],
            transient["decl"],
            [
                {
                    "name": "GAIADR2",
                    "use": "catsHTM",
                    "rs_arcsec": self.gaia_rs,
                    "keys_to_append": [
                        "Mag_G",
                        "PMRA",
                        "ErrPMRA",
                        "PMDec",
                        "ErrPMDec",
                        "Plx",
                        "ErrPlx",
                        "ExcessNoiseSig",
                    ],
                }
            ],
        )[0]

        if srcs:
            gaia_tab = Table(
                [
                    {
                        k: np.nan if v is None else v
                        for k, v in src["body"].items()
                    }
                    for src in srcs
                ]
            )

            # compute distance
            gaia_tab["DISTANCE"] = [src["dist_arcsec"] for src in srcs]
            gaia_tab["DISTANCE_NORM"] = (
                1.8 + 0.6 * np.exp((20 - gaia_tab["Mag_G"]) / 2.05)
                > gaia_tab["DISTANCE"]
            )
            gaia_tab["FLAG_PROX"] = [
                x["DISTANCE_NORM"]
                and self.gaia_veto_gmag_min
                <= x["Mag_G"]
                <= self.gaia_veto_gmag_max
                for x in gaia_tab
            ]

            # check for proper motion and parallax conditioned to distance
            gaia_tab["FLAG_PMRA"] = (
                abs(gaia_tab["PMRA"] / gaia_tab["ErrPMRA"])
                > self.gaia_pm_signif
            )
            gaia_tab["FLAG_PMDec"] = (
                abs(gaia_tab["PMDec"] / gaia_tab["ErrPMDec"])
                > self.gaia_pm_signif
            )
            gaia_tab["FLAG_Plx"] = (
                abs(gaia_tab["Plx"] / gaia_tab["ErrPlx"])
                > self.gaia_plx_signif
            )

            # take into account precison of the astrometric solution via the ExcessNoise key
            gaia_tab["FLAG_Clean"] = (
                gaia_tab["ExcessNoiseSig"] < self.gaia_excessnoise_sig_max
            )

            # select just the sources that are close enough and that are not noisy
            gaia_tab = gaia_tab[gaia_tab["FLAG_PROX"]]
            gaia_tab = gaia_tab[gaia_tab["FLAG_Clean"]]

            # among the remaining sources there is anything with
            # significant proper motion or parallax measurement
            if (
                any(gaia_tab["FLAG_PMRA"] == True)  # noqa: E712
                or any(gaia_tab["FLAG_PMDec"] == True)  # noqa: E712
                or any(gaia_tab["FLAG_Plx"] == True)  # noqa: E712
            ):
                return True

        return False

    # Override
    def process(self, alert: AmpelAlertProtocol) -> None | bool:
        """
        Mandatory implementation.
        To exclude the alert, return *None*
        To accept it, either return
        * self.on_match_t2_units
        * or a custom combination of T2 unit names
        """

        # CUT ON THE HISTORY OF THE ALERT
        #################################

        pps = [
            el for el in alert.datapoints if el.get("diaSourceId") is not None
        ]
        if len(pps) < self.min_ndet:
            # self.logger.debug("rejected: %d photopoints in alert (minimum required %d)"% (npp, self.min_ndet))
            self.logger.info(None, extra={"nDet": len(pps)})
            return None

        # cut on length of detection history
        detections_jds = [el["midpointMjdTai"] for el in pps]
        det_tspan = max(detections_jds) - min(detections_jds)
        if not (self.min_tspan <= det_tspan <= self.max_tspan):
            # self.logger.debug("rejected: detection history is %.3f d long, \
            # requested between %.3f and %.3f d"% (det_tspan, self.min_tspan, self.max_tspan))
            self.logger.info(None, extra={"tSpan": det_tspan})
            return None

        # IMAGE QUALITY CUTS
        ####################

        latest = alert.datapoints[0]
        # latest = sorted(alert.datapoints, key=lambda x:x["jd"], reverse=True)[0]
        if not self._alert_has_keys(latest):
            return None

        # cut on galactic latitude
        b = self.get_galactic_latitude(latest)
        if abs(b) < self.min_gal_lat:
            # self.logger.debug("rejected: b=%.4f, too close to Galactic plane (max allowed: %f)."% (b, self.min_gal_lat))
            self.logger.info(None, extra={"galPlane": abs(b)})
            return None

        # check with gaia
        if self.gaia_rs > 0 and self.is_star_in_gaia(latest):
            self.logger.debug(
                f"rejected: within {self.gaia_rs:.2f} arcsec from a GAIA start (PM of PLX)"
            )
            self.logger.info(None, extra={"gaiaIsStar": True})
            return None

        # self.logger.debug("Alert %s accepted. Latest pp ID: %d"%(alert.tran_id, latest['candid']))
        self.logger.debug(
            "Alert accepted", extra={"latestPpId": latest["diaSourceId"]}
        )

        # for key in self.keys_to_check:
        # 	self.logger.debug("{}: {}".format(key, latest[key]))

        return True
