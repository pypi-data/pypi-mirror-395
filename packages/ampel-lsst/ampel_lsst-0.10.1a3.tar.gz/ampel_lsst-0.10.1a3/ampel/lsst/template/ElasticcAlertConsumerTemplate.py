from ampel.model.UnitModel import UnitModel

from .LSSTAlertConsumerTemplate import LSSTAlertConsumerTemplate


class ElasticcAlertConsumerTemplate(LSSTAlertConsumerTemplate):
    loader: str | UnitModel = UnitModel(
        unit="KafkaAlertLoader",
        config={
            "bootstrap": "public.alerts.ztf.uw.edu:9092",
            "group_name": "ampel-test",
            "topics": ["elasticc-test-only-3"],
            "timeout": 30,
        },
    )
