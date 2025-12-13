#!/usr/bin/env python
# File:                Ampel-ZTF/ampel/ztf/t3/complement/ZTFCutoutImages.py
# Author:              Jakob van Santen <jakob.van.santen@desy.de>
# Date:                18.09.2020
# Last Modified Date:  18.09.2020
# Last Modified By:    Jakob van Santen <jakob.van.santen@desy.de>

from base64 import b64decode
from collections.abc import Iterable
from typing import Literal

import backoff
import requests
from requests_toolbelt.sessions import (  # type: ignore[import-untyped]
    BaseUrlSession,
)

from ampel.abstract.AbsBufferComplement import AbsBufferComplement
from ampel.struct.AmpelBuffer import AmpelBuffer
from ampel.struct.T3Store import T3Store


class LSSTCutoutImages(AbsBufferComplement):
    """
    Add cutout images from LSST archive database
    """

    #: Which detection to retrieve cutouts for
    eligible: Literal["first", "last", "brightest", "all"] = "last"

    archive_url: str = (
        "https://ampel-dev.ia.zeuthen.desy.de/api/lsst/archive/v1/"
    )
    insecure: bool = False

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.session = BaseUrlSession(base_url=self.archive_url)

    @backoff.on_exception(
        backoff.expo,
        requests.ConnectionError,
        max_tries=5,
        factor=10,
    )
    @backoff.on_exception(
        backoff.expo,
        requests.HTTPError,
        giveup=lambda e: not isinstance(e, requests.HTTPError)
        or e.response is None
        or e.response.status_code not in {502, 503, 504, 429, 408},
        max_time=60,
    )
    def get_cutout(self, diaSourceId: int) -> None | dict[str, bytes]:
        response = self.session.get(
            f"alert/{diaSourceId}/cutouts", verify=not self.insecure
        )
        if response.status_code == 404:
            return None

        response.raise_for_status()
        json = response.json()
        return {
            k: b64decode(json[k])
            for k in ["cutoutScience", "cutoutTemplate", "cutoutDifference"]
        }

    def complement(self, records: Iterable[AmpelBuffer], t3s: T3Store) -> None:  # noqa: ARG002
        for record in records:
            if (photopoints := record.get("t0")) is None:
                raise ValueError(f"{type(self).__name__} requires t0 records")
            pps = sorted(
                [pp for pp in photopoints if "LSST_DP" in pp.get("tag", [])],
                key=lambda pp: pp["body"]["midpointMjdTai"],
            )
            if not pps:
                return

            if self.eligible == "last":
                candids = [pps[-1]["id"]]
            elif self.eligible == "first":
                candids = [pps[0]["id"]]
            elif self.eligible == "brightest":
                candids = [
                    min(pps, key=lambda pp: pp["body"]["psfFlux"])["id"]
                ]
            else:  # all
                candids = [pp["id"] for pp in pps]
            cutouts = {candid: self.get_cutout(candid) for candid in candids}

            if "extra" not in record or record["extra"] is None:
                record["extra"] = {self.__class__.__name__: cutouts}
            else:
                record["extra"][self.__class__.__name__] = cutouts
