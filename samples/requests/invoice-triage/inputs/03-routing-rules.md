# AP routing rules (current, v2026-05)

| Queue | Rule |
|---|---|
| PO-matched | Valid PO number found in SAP, amount within 5% of open PO balance |
| Non-PO | No PO, amount <= $10,000, supplier on non-PO approved list |
| Utilities | Supplier category = UTIL in vendor master |
| Capital | PO account assignment category = A (asset) |
| Exceptions | Anything else: no PO and > $10K, unknown supplier, > 5% variance, bank details differ from vendor master, suspected duplicate |

Priority: Exceptions rules override all others. Utilities overrides Non-PO.
