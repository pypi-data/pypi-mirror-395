#!/usr/bin/env python
# File              : Ampel-LSST/ampel/lsst/ingest/LSSTMongoMuxer.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 18.03.2022
# Last Modified By  : Marcus Fenner <mf@physik.hu-berlin.de>

import datetime
from typing import Any

from ampel.abstract.AbsT0Muxer import AbsT0Muxer
from ampel.content.DataPoint import DataPoint
from ampel.types import StockId
from ampel.util.mappings import unflatten_dict


class LSSTMongoMuxer(AbsT0Muxer):
    """
    This class compares info between alert and DB so that only the needed info is ingested later.

    # Not used - removed
    :param alert_history_length: alerts must not contain all available info for a given transient.
    Alerts for LSST should provide a photometric history of 365 days.

    JN: For *elasticc* diffimage and forced photometry will have identical flux
    values. Since there is both a previous source phot and previous forced phot
    history, a single alert can contain multiple copes of the same measurement.
    Again, for *elasticc* it also seems like they keep the same id
    ForcedSourceID and SourceID
    for both kinds. As JN understand, this means that as new measurements come
    in, the typical SourceId flux values will be retained and forced phot
    "updates" not added to the DB. As the flux is the same this _should_ not
    matter.
    What we should do is probably:
    - Generate ID datapoints in LSSTDataPointShaper, prob of a hash from
    [time, flux, ccdVisitId(?)].
    - Make a proper superseeded search a la ZiMongoMuxer here where we would
    look for identical time (only?)
    But since this should not make a difference, provided we drop duplicates in
    the LSSTDataPointShaper it seems that this change is not strictly necessary
    now (assuming I got everything right.)


    """

    # Standard projection used when checking DB for existing PPS/ULS
    projection: dict[str, int] = {
        "_id": 0,
        "id": 1,
        "tag": 1,
        "channel": 1,
        "excl": 1,
        "stock": 1,
        "body.midpointMjdTai": 1,
        "body.band": 1,
        "body.psfFlux": 1,
        "body.diaObjectId": 1,
    }

    #: Require minimum time-to-live for datapoints
    min_ttl: None | float = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # used to check potentially already inserted pps
        self._photo_col = self.context.db.get_collection("t0")
        self._projection_spec = unflatten_dict(self.projection)

    def process(
        self, dps_al: list[DataPoint], stock_id: None | StockId = None
    ) -> tuple[None | list[DataPoint], None | list[DataPoint]]:
        """
        :param dps_al: datapoints from alert
        :param stock_id: stock id from alert
        Attempt to determine which pps/uls should be inserted into the t0 collection,
        and which one should be marked as superseded.
        """

        # Part 1: gather info from DB and alert
        #######################################

        # New pps/uls lists for db loaded datapoints
        filter: dict[str, Any] = {"stock": stock_id}
        if self.min_ttl is not None:
            filter["expiry"] = {
                "$not": {
                    "$lt": datetime.datetime.now(tz=datetime.timezone.utc)
                    + datetime.timedelta(seconds=self.min_ttl)
                }
            }
        dps_db: list[DataPoint] = list(
            self._photo_col.find(filter, self.projection)
        )

        # Create set with datapoint ids from alert
        ids_dps_alert = {el["id"]: el for el in dps_al}

        # python set of ids of datapoints from DB
        ids_dps_db = {el["id"]: el for el in dps_db}

        # Part 2: Insert new data points
        ################################

        # Difference between candids from the alert and candids present in DB
        ids_dps_to_insert = ids_dps_alert.keys() - ids_dps_db.keys()
        ids_dps_to_combine = ids_dps_alert.keys() | ids_dps_db.keys()

        # Emit union of datapoints from alert and database, prefering content
        # from the database. This allows the ingestion handler to detect when an
        # additional channel accepts a datapoint that was already in the
        # database.
        dps_combine = [
            ids_dps_db[dp_id] if dp_id in ids_dps_db else ids_dps_alert[dp_id]
            for dp_id in ids_dps_to_combine
        ]

        return [
            dp for dp in dps_al if dp["id"] in ids_dps_to_insert
        ], dps_combine

    def _project(self, doc, projection):
        out: dict[str, Any] = {}
        for key, spec in projection.items():
            if key not in doc:
                continue

            if isinstance(spec, dict):
                item = doc[key]
                if isinstance(item, list):
                    out[key] = [self._project(v, spec) for v in item]
                elif isinstance(item, dict):
                    out[key] = self._project(item, spec)
            else:
                out[key] = doc[key]

        return out
