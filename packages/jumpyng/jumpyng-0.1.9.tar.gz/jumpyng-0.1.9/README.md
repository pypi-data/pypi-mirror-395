# jumpyng

Helper utilities for processing DeepLabCut jumping experiments, generating QC reports, and computing jump metrics.

## Installation
```bash
pip install jumpyng
```

## Usage
- `jumpyng.algorithm`: bulk data loading, jump detection, and metric calculation helpers.
- `jumpyng.visualization`: PDF report generation for quick visual checks.
- `jumpyng.utils`: Helper functions used to speed up analysis and contains common functions.
- `jumpyng.validation`: Validation tools used for Data Quality QA/QC checks.
- `jumpyng.dlchelper`: wrappers for running DeepLabCut and pre-processing data (install with `pip install jumpyng[dlc]` to use these helpers).

The package is still evolving; APIs may change between minor versions.
