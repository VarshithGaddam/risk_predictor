# CSV Upload Format Guide

## Required Columns

Your CSV file **must** include these columns:

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| `patient_id` | Text | Unique patient identifier | P00001 |
| `name` | Text | Patient full name | John Doe |
| `age` | Number | Patient age in years | 65 |
| `gender` | Text | M or F | M |
| `admission_date` | Date | Format: YYYY-MM-DD | 2024-10-15 |
| `diagnosis` | Text | Primary diagnosis | Type 2 Diabetes Mellitus |

## Optional Columns

These columns are optional but recommended for better risk prediction:

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| `discharge_date` | Date | Format: YYYY-MM-DD (leave empty if still admitted) | 2024-10-20 |
| `previous_admissions` | Number | Number of previous hospital admissions | 2 |
| `comorbidities` | Number | Number of comorbid conditions | 3 |
| `heart_rate` | Number | Heart rate in bpm | 85 |
| `blood_pressure_systolic` | Number | Systolic BP in mmHg | 145 |
| `blood_pressure_diastolic` | Number | Diastolic BP in mmHg | 90 |
| `temperature` | Number | Body temperature in Celsius | 37.2 |
| `oxygen_saturation` | Number | O2 saturation percentage | 96 |

## Sample CSV Format

### Minimal Format (Required Fields Only)
```csv
patient_id,name,age,gender,admission_date,diagnosis
P00001,John Doe,65,M,2024-10-15,Type 2 Diabetes Mellitus
P00002,Jane Smith,72,F,2024-10-16,Congestive Heart Failure
P00003,Bob Johnson,58,M,2024-10-17,Pneumonia
```

### Complete Format (All Fields)
```csv
patient_id,name,age,gender,admission_date,diagnosis,previous_admissions,comorbidities,heart_rate,blood_pressure_systolic,blood_pressure_diastolic,temperature,oxygen_saturation
P00001,John Doe,65,M,2024-10-15,Type 2 Diabetes Mellitus,2,3,85,145,90,37.2,96
P00002,Jane Smith,72,F,2024-10-16,Congestive Heart Failure,3,4,95,160,95,37.5,92
P00003,Bob Johnson,58,M,2024-10-17,Pneumonia,0,1,105,140,88,38.5,89
```

## Common Diagnoses

Use these standard diagnosis names for better risk prediction:

- Type 2 Diabetes Mellitus
- Congestive Heart Failure
- Chronic Obstructive Pulmonary Disease
- Pneumonia
- Acute Myocardial Infarction
- Sepsis
- Chronic Kidney Disease
- Stroke
- Hip Fracture
- Urinary Tract Infection

## Data Validation Rules

1. **patient_id**: Must be unique across all patients
2. **age**: Must be between 0 and 120
3. **gender**: Must be 'M' or 'F'
4. **admission_date**: Must be in YYYY-MM-DD format
5. **heart_rate**: Typical range 40-200 bpm
6. **blood_pressure_systolic**: Typical range 80-200 mmHg
7. **blood_pressure_diastolic**: Typical range 40-120 mmHg
8. **temperature**: Typical range 35.0-42.0°C
9. **oxygen_saturation**: Must be 0-100%

## Tips for Creating Your CSV

1. **Use Excel or Google Sheets**
   - Create your data in a spreadsheet
   - Save/Export as CSV format

2. **Avoid Special Characters**
   - Don't use commas in text fields
   - Use simple text for names and diagnoses

3. **Date Format**
   - Always use YYYY-MM-DD format
   - Example: 2024-10-15 (not 10/15/2024)

4. **Missing Data**
   - Leave optional fields empty if data not available
   - Don't use "N/A" or "null" - just leave blank

5. **File Encoding**
   - Save as UTF-8 encoding
   - This ensures special characters work correctly

## Example Files Included

- `sample_patients.csv` - 15 sample patients with all fields
- Use this as a template for your own data

## After Upload

Once uploaded, the system will:
1. ✅ Validate all required fields
2. ✅ Calculate risk scores automatically
3. ✅ Display patients in the Patient List
4. ✅ Update dashboard metrics

## Troubleshooting

**Error: "No file provided"**
- Make sure you selected a file before clicking Upload

**Error: "File must be CSV format"**
- Ensure file extension is .csv
- Re-save from Excel as CSV format

**Error: Missing required fields**
- Check that all required columns are present
- Column names must match exactly (case-sensitive)

**Patients show N/A for risk scores**
- Risk scores calculate automatically after upload
- Refresh the page if they don't appear immediately
- Make sure vital signs data is included for better predictions

## Need Help?

Check the sample file `sample_patients.csv` for a working example!
