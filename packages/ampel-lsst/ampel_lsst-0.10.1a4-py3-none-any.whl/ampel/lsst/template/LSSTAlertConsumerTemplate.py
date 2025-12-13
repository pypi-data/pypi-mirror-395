from ampel.lsst.ingest.LSSTCompilerOptions import (
    CompilerOptions,
    LSSTCompilerOptions,
)
from ampel.model.UnitModel import UnitModel
from ampel.template.EasyAlertConsumerTemplate import EasyAlertConsumerTemplate


class LSSTAlertConsumerTemplate(EasyAlertConsumerTemplate):
    supplier: str | UnitModel = UnitModel(
        unit="LSSTAlertSupplier", config={"deserialize": None}
    )
    shaper: str | UnitModel = "LSSTDataPointShaper"
    combiner: str | UnitModel = "LSSTT1Combiner"
    compiler_opts: CompilerOptions = LSSTCompilerOptions()
    muxer: None | str | UnitModel = "LSSTMongoMuxer"
