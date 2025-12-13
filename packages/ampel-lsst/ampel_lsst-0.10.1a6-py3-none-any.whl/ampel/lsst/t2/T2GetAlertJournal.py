#!/usr/bin/env python
# File:                Ampel-LSST/ampel/lsst/t2/T2GetAlertJournal.py
# License:             BSD-3-Clause
# Author:              Marcus Fennner <mf@physik.hu-berlinn.de>
# Date:                31.03.2022
# Last Modified Date:  31.03.2022
# Last Modified By:    Marcus Fennner <mf@physik.hu-berlinn.de>


from ampel.abstract.AbsStockT2Unit import AbsStockT2Unit
from ampel.content.StockDocument import StockDocument
from ampel.types import UBson


class T2GetAlertJournal(AbsStockT2Unit):
    """
    Get the alert journal of an LSST stock
    """

    def process(self, stock_doc: StockDocument) -> UBson:
        return [
            journal for journal in stock_doc["journal"] if journal["tier"] == 0
        ]
