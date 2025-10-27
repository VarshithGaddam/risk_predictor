# Demo Clinical Notes

Use these sample clinical notes to test the NLP analyzer:

## Sample 1: Cardiac Event
```
Patient presents with severe chest pain radiating to left arm and shortness of breath. ECG shows ST elevation consistent with acute myocardial infarction. Troponin levels elevated at 2.5 ng/mL. Patient has history of hypertension and diabetes. Started on aspirin 325mg, clopidogrel 300mg loading dose, and atorvastatin 80mg. Heparin drip initiated. Patient scheduled for emergency cardiac catheterization.
```

## Sample 2: Respiratory Infection
```
65-year-old male admitted with fever (39.2°C), productive cough, and difficulty breathing. Chest X-ray reveals bilateral infiltrates consistent with pneumonia. Oxygen saturation 88% on room air, improved to 94% on 2L nasal cannula. Started on ceftriaxone 1g IV q24h and azithromycin 500mg PO daily. Blood cultures pending. Patient has COPD and is on home oxygen.
```

## Sample 3: Diabetic Emergency
```
Patient with type 2 diabetes presents with nausea, vomiting, and altered mental status. Blood glucose 485 mg/dL, pH 7.25, positive ketones indicating diabetic ketoacidosis. Started on insulin drip at 0.1 units/kg/hr. IV fluids initiated with normal saline. Electrolytes being monitored closely. Patient reports non-compliance with metformin and insulin regimen.
```

## Sample 4: Trauma
```
72-year-old female brought in after fall at home. Patient complains of severe right hip pain and inability to bear weight. X-ray confirms right femoral neck fracture. Vital signs stable. Pain managed with morphine 4mg IV. Patient has osteoporosis and takes alendronate. Orthopedic surgery consulted for surgical repair. Pre-op labs ordered.
```

## Sample 5: Heart Failure Exacerbation
```
Patient with known congestive heart failure presents with worsening dyspnea and bilateral lower extremity edema. Weight increased 5kg over past week. Chest X-ray shows pulmonary congestion. BNP elevated at 1200 pg/mL. Started on furosemide 40mg IV, increased home dose of lisinopril. Strict intake and output monitoring. Low sodium diet ordered.
```

## Sample 6: Sepsis
```
Patient admitted from nursing home with altered mental status, fever (38.8°C), and hypotension (BP 85/50). Suspected urinary tract infection based on cloudy, foul-smelling urine. Lactate 4.2 mmol/L concerning for sepsis. Blood and urine cultures obtained. Started on broad-spectrum antibiotics: vancomycin 1g IV and piperacillin-tazobactam 4.5g IV. Aggressive fluid resuscitation initiated. ICU transfer arranged.
```

## Expected Entities

The NLP analyzer should extract:

**Symptoms**: chest pain, shortness of breath, fever, cough, nausea, vomiting, pain, dyspnea, edema

**Diagnoses**: myocardial infarction, hypertension, diabetes, pneumonia, COPD, ketoacidosis, fracture, heart failure, sepsis, infection

**Medications**: aspirin, clopidogrel, atorvastatin, heparin, ceftriaxone, azithromycin, insulin, metformin, morphine, alendronate, furosemide, lisinopril, vancomycin

**Procedures**: catheterization, surgery, resuscitation, repair

## Testing Tips

1. Try copying different samples to see how the analyzer handles various medical scenarios
2. Mix and match sentences from different samples
3. Add your own medical terms to test pattern matching
4. Check confidence scores - lower scores indicate uncertain extractions
5. Verify that the summary accurately captures the key information
