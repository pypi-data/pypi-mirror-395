#!/usr/bin/env python
# File              : Ampel-LSST/ampel/lsst/alert/load/MultiAvroAlertLoader.py
# License           : BSD-3-Clause
# Author            : Marcus Fenner <mf@physik.hu-berlin.de>
# Date              : 07.05.2021
# Last Modified Date: 14.09.2021
# Last Modified By  : Marcus Fenner <mf@physik.hu-berlin.de>

from collections.abc import Iterable
from io import BytesIO, IOBase
from typing import no_type_check

from fastavro import reader

from ampel.abstract.AbsAlertLoader import AbsAlertLoader
from ampel.base.AuxUnitRegister import AuxUnitRegister
from ampel.model.UnitModel import UnitModel


class MultiAvroAlertLoader(AbsAlertLoader[BytesIO]):
    """
    Load avro alerts from another AlertLoader.
    This is needed if there are multiple Alerts in a single avro file.
    """

    loader: UnitModel

    def __init__(self, **kwargs) -> None:
        if "loader" in kwargs and isinstance(kwargs["loader"], str):
            kwargs["loader"] = {"unit": kwargs["loader"]}
        super().__init__(**kwargs)

        self.set_alert_source(self.loader)

    def set_alert_source(self, loader) -> None:
        self.alert_loader: AbsAlertLoader[Iterable[IOBase]] = (
            AuxUnitRegister.new_unit(  # type: ignore
                model=loader
            )
        )
        self.next_file()

    @no_type_check
    def next_file(self) -> None:
        self.reader = reader(next(self.alert_loader))

    def __iter__(self):
        return self

    @no_type_check
    def __next__(self) -> BytesIO:
        try:
            return next(self.reader)
        except StopIteration:
            self.next_file()
            return next(self.reader)
