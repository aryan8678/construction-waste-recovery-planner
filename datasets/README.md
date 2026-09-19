# Construction Waste / Waste Management Dataset Package — V1

## Included
For each of the three selected CSV files supplied in `F2-datasets.zip`:
- Original CSV: preserved unchanged under `original/`
- Cleaned CSV: under `cleaned/`
- Source linkage: `source_inventory.csv`
- Transformation audit: `logs/data_change_log.csv`
- Quality summary: `logs/data_quality_report.csv`
- Requested-feature coverage: `logs/requested_feature_audit.csv`

## Traceability
Each cleaned file contains:
- `source_id`
- `source_row_id`

Use these fields to connect a cleaned row to:
1. `source_inventory.csv`
2. The original CSV under `original/`
3. The relevant change-log entries in `logs/data_change_log.csv`

## Cleaning performed
- Standardized column names to lowercase snake_case
- Trimmed whitespace in text fields
- Added traceability metadata
- Removed exact duplicate rows
- Converted clearly numeric fields where safe
- Did not invent or impute missing values

## Critical research limitation
The supplied files are general waste-management datasets. They do not reliably contain all requested construction-waste ML features:
- material type specifically for construction materials
- condition
- contamination level
- reusability
- validated recommended recovery pathway target

Do not present missing or derived fields as original observations. If your teammate later creates labels with expert rules, store a separate labelled/derived dataset and document the label-generation method.
