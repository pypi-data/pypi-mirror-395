from collections.abc import Sequence

from ampel.t1.T1SimpleCombiner import T1SimpleCombiner


class LSSTT1Combiner(T1SimpleCombiner):
    """Dummy class that exists only to provide default values for access and policy"""

    access: Sequence[int | str] = []
    policy: Sequence[int | str] = []
