#!/usr/bin/env python


import gzip
import logging
import os
from io import BytesIO, StringIO

import fastavro

from ampel.alert.load.DirAlertLoader import DirAlertLoader
from ampel.lsst.kafka.HttpSchemaRepository import (
    DEFAULT_SCHEMA,
    Schema,
    parse_schema,
)

log = logging.getLogger(__name__)


class ElasticcDirAlertLoader(DirAlertLoader):
    """
    Load alerts from a Dir, but with a schemaless format. Using schema as in
    KafkaAlertLoader.

    """

    #: Message schema
    avro_schema: dict | str = DEFAULT_SCHEMA

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._alert_schema: Schema = parse_schema(self.avro_schema)

    def __next__(self) -> StringIO | BytesIO:
        if not self._files:
            self.build_file_list()
            self._iter_files = iter(self._files)

        if (fpath := next(self._iter_files, None)) is None:
            raise StopIteration

        if self.logger.verbose > 1:
            self.logger.debug("Loading " + fpath)

        # Assuming one alert per file and either compressed (gz) or binary uncompressed
        if os.path.splitext(fpath)[1] == ".gz":
            alertopener = gzip.open
        else:
            alertopener = open  # type: ignore[assignment]

        with alertopener(fpath, self._open_mode) as alert_file:
            return fastavro.schemaless_reader(  # type: ignore[return-value]
                alert_file,  # type: ignore[arg-type]
                self._alert_schema,
                reader_schema=None,
            )
