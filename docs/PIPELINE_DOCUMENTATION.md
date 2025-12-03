# Pipeline Documentation

## Overview

The pipeline orchestrates the complete workflow from downloading NSE files to generating final Excel output with calculated formulas.

## Pipeline Flow

```
1. Download Input Files
   ↓
2. Verify Downloads (with user prompt)
   ↓
3. User Confirmation
   ↓
4. Copy Data to Excel Template
   ↓
5. Run Formulas
   ↓
6. Copy to Output File
```

## API Endpoints

### 1. Run Pipeline (Download + Verify)

**Endpoint**: `POST /pipeline/run`

**Request Body**:
```json
{
  "start_date": "2023-12-01",
  "end_date": "2023-12-05",
  "urls": {},
  "raw_path": "/path/to/raw",
  "template_path": "/path/to/template.xlsx",  // Optional
  "intermediate_path": "/path/to/intermediate",  // Optional
  "output_path": "/path/to/output",  // Optional
  "worksheet_mapping": {  // Optional
    "cm_bhavcopy": "Eq Bhav",
    "fo_bhavcopy": "FU Data final"
  },
  "worksheets_to_output": ["Sheet1", "Results"]  // Optional
}
```

**Response**:
```json
{
  "success": true,
  "phases": [
    {
      "phase": "download",
      "success": true,
      "downloaded": ["file1.zip", "file2.zip"],
      "missing": []
    },
    {
      "phase": "verification",
      "success": true,
      "verified_count": 10,
      "invalid_count": 0,
      "verified_files": [...],
      "invalid_files": []
    }
  ],
  "current_phase": "verification",
  "requires_user_confirmation": true,
  "message": "Download and verification completed. Ready for user confirmation."
}
```

### 2. Confirm and Continue (Excel Processing)

**Endpoint**: `POST /pipeline/confirm`

**Request Body**:
```json
{
  "start_date": "2023-12-01",
  "end_date": "2023-12-05",
  "raw_path": "/path/to/raw",
  "template_path": "/path/to/template.xlsx",
  "intermediate_path": "/path/to/intermediate",
  "output_path": "/path/to/output",
  "confirmed": true,
  "worksheet_mapping": {},
  "worksheets_to_output": []
}
```

**Response**:
```json
{
  "success": true,
  "phases": [
    {
      "phase": "excel_processing",
      "success": true,
      "intermediate_path": "/path/to/intermediate/processed.xlsx",
      "output_path": "/path/to/output/final.xlsx",
      "worksheets": ["Sheet1", "Results"],
      "message": "Successfully created output file: final.xlsx"
    }
  ],
  "current_phase": "excel_processing",
  "output_path": "/path/to/output/final.xlsx"
}
```

### 3. Verify Only

**Endpoint**: `POST /pipeline/verify-only`

**Query Parameters**:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `raw_path`: Path to raw files directory

**Response**:
```json
{
  "success": true,
  "phase": "verification",
  "verified_count": 10,
  "invalid_count": 0,
  "verified_files": [...],
  "invalid_files": [],
  "all_valid": true
}
```

## Services

### VerificationService

Verifies downloaded files:
- **ZIP files**: Checks validity, extracts and lists contents
- **CSV files**: Validates format and counts rows
- **DAT files**: Checks readability and counts lines

**Methods**:
- `verify_file(file_path)` - Verify any file type
- `verify_zip_file(file_path)` - Verify ZIP file
- `verify_csv_file(file_path)` - Verify CSV file
- `verify_dat_file(file_path)` - Verify DAT file
- `verify_downloads(start_date, end_date, raw_path)` - Verify all downloads

### ExcelService

Processes Excel files:
- **Copy Data**: Copies CSV/DAT data to Excel worksheets
- **Run Formulas**: Executes Excel formulas
- **Copy to Output**: Creates final output file

**Methods**:
- `copy_data_to_excel(source_files, template_path, output_path)` - Copy data to Excel
- `run_formulas(excel_path)` - Run formulas in Excel file
- `copy_to_output(source_excel_path, output_path)` - Copy to final output
- `process_full_pipeline(...)` - Run all steps

### PipelineService

Orchestrates the full workflow:
- **Phase 1**: Download files
- **Phase 2**: Verify downloads
- **Phase 3**: Excel processing (after confirmation)

**Methods**:
- `run_download_phase(...)` - Download files
- `run_verification_phase(...)` - Verify downloads
- `run_excel_processing_phase(...)` - Process Excel files
- `run_full_pipeline(...)` - Run complete pipeline
- `continue_pipeline_after_confirmation(...)` - Continue after user confirms

## Worksheet Mapping

Default mapping of file types to worksheet names:

```python
{
    'cm_bhavcopy': 'Eq Bhav',
    'fo_bhavcopy': 'FU Data final',
    'cm_delivery': 'Eq Del',
    'fo_udiff': 'Daily OP Data',
    'fo_participant_oi': 'Daily OP Data'
}
```

Custom mapping can be provided in the request.

## Usage Example

### Step 1: Run Pipeline (Download + Verify)

```python
import requests

response = requests.post('http://localhost:5001/pipeline/run', json={
    "start_date": "2023-12-01",
    "end_date": "2023-12-01",
    "urls": {},
    "raw_path": "/path/to/raw"
})

data = response.json()
if data['requires_user_confirmation']:
    # Show verification results to user
    print(f"Verified: {data['phases'][1]['verified_count']}")
    print(f"Invalid: {data['phases'][1]['invalid_count']}")
    
    # If user confirms, proceed to step 2
```

### Step 2: User Confirms and Continue

```python
if user_confirmed:
    response = requests.post('http://localhost:5001/pipeline/confirm', json={
        "start_date": "2023-12-01",
        "end_date": "2023-12-01",
        "raw_path": "/path/to/raw",
        "template_path": "/path/to/template.xlsx",
        "intermediate_path": "/path/to/intermediate",
        "output_path": "/path/to/output",
        "confirmed": True
    })
    
    data = response.json()
    if data['success']:
        print(f"Output file: {data['output_path']}")
```

## Error Handling

The pipeline handles errors at each phase:

- **Download errors**: Reported in `missing` list
- **Verification errors**: Listed in `invalid_files` with error messages
- **Excel processing errors**: Returned in response `error` field

## File Structure

```
raw_path/
  ├── cm_bhavcopy_2023-12-01.zip
  ├── fo_bhavcopy_2023-12-01.zip
  └── ...

intermediate_path/
  └── processed_2023-12-01.xlsx  (with formulas)

output_path/
  └── final_2023-12-01.xlsx  (final output)
```

## Testing

Run pipeline tests:

```bash
cd backend
pytest tests/test_pipeline.py -v
pytest tests/test_verification.py -v
```

## Notes

- Template Excel file is optional - new workbook will be created if not provided
- Formulas are executed using openpyxl's calculation engine
- Output file contains only calculated values (no formulas)
- All file paths should be absolute or relative to backend directory

