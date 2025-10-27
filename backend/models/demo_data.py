import random
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models.database import get_db_connection, init_database
except ImportError:
    from database import get_db_connection, init_database

# Sample data pools
FIRST_NAMES = ['John', 'Mary', 'James', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 
               'William', 'Barbara', 'David', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Jessica']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
              'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson']

DIAGNOSES = [
    'Type 2 Diabetes Mellitus',
    'Congestive Heart Failure',
    'Chronic Obstructive Pulmonary Disease',
    'Pneumonia',
    'Acute Myocardial Infarction',
    'Sepsis',
    'Chronic Kidney Disease',
    'Stroke',
    'Hip Fracture',
    'Urinary Tract Infection'
]

SAMPLE_NOTES = [
    "Patient presents with shortness of breath and chest pain. Diagnosed with acute myocardial infarction. Started on aspirin 325mg and atorvastatin 80mg. Scheduled for cardiac catheterization.",
    "Admitted with fever, cough, and difficulty breathing. Chest X-ray shows bilateral infiltrates consistent with pneumonia. Started on ceftriaxone 1g IV and azithromycin 500mg PO.",
    "Patient with history of diabetes presents with hyperglycemia and ketoacidosis. Blood glucose 450 mg/dL. Started on insulin drip. Monitoring electrolytes closely.",
    "Elderly patient admitted after fall at home. X-ray confirms hip fracture. Scheduled for surgical repair. Pain managed with morphine 2mg IV PRN.",
    "Patient with CHF exacerbation. Bilateral lower extremity edema noted. Started on furosemide 40mg IV. Strict I&O monitoring."
]

def generate_demo_data(num_patients=50):
    """Generate realistic demo patient data"""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    init_database()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM notes')
    cursor.execute('DELETE FROM vitals')
    cursor.execute('DELETE FROM patients')
    
    print(f"Generating {num_patients} demo patients...")
    
    for i in range(num_patients):
        # Generate patient data
        patient_id = f"P{str(i+1).zfill(5)}"
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        age = random.randint(25, 90)
        gender = random.choice(['M', 'F'])
        
        # Admission date in last 30 days
        days_ago = random.randint(1, 30)
        admission_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Some patients discharged, some still admitted
        discharge_date = None
        if random.random() > 0.3:  # 70% discharged
            los = random.randint(2, 14)  # length of stay
            discharge_date = (datetime.strptime(admission_date, '%Y-%m-%d') + timedelta(days=los)).strftime('%Y-%m-%d')
        
        diagnosis = random.choice(DIAGNOSES)
        previous_admissions = random.randint(0, 5)
        comorbidities = random.randint(0, 4)
        
        # Insert patient
        cursor.execute('''
            INSERT INTO patients (patient_id, name, age, gender, admission_date, discharge_date, 
                                diagnosis, previous_admissions, comorbidities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (patient_id, name, age, gender, admission_date, discharge_date, 
              diagnosis, previous_admissions, comorbidities))
        
        # Generate vitals
        heart_rate = random.randint(60, 120)
        bp_systolic = random.randint(100, 180)
        bp_diastolic = random.randint(60, 100)
        temperature = round(random.uniform(36.5, 39.5), 1)
        oxygen_saturation = random.randint(88, 100)
        
        cursor.execute('''
            INSERT INTO vitals (patient_id, heart_rate, blood_pressure_systolic, 
                              blood_pressure_diastolic, temperature, oxygen_saturation)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (patient_id, heart_rate, bp_systolic, bp_diastolic, temperature, oxygen_saturation))
        
        # Add clinical note for some patients
        if random.random() > 0.5:
            note_text = random.choice(SAMPLE_NOTES)
            cursor.execute('''
                INSERT INTO notes (patient_id, note_text)
                VALUES (?, ?)
            ''', (patient_id, note_text))
    
    conn.commit()
    
    # Calculate risk scores for all patients
    print("Calculating risk scores...")
    try:
        from ml.risk_predictor import predictor
        
        cursor.execute('''
            SELECT p.*, v.heart_rate, v.blood_pressure_systolic, v.blood_pressure_diastolic,
                   v.temperature, v.oxygen_saturation
            FROM patients p
            LEFT JOIN vitals v ON p.patient_id = v.patient_id
        ''')
        
        patients = cursor.fetchall()
        for patient in patients:
            patient_dict = dict(patient)
            prediction = predictor.predict(patient_dict)
            
            cursor.execute('''
                UPDATE patients 
                SET risk_score = ?, risk_level = ?
                WHERE patient_id = ?
            ''', (prediction['riskScore'], prediction['riskLevel'], patient_dict['patient_id']))
        
        conn.commit()
        print(f"✅ Calculated risk scores for {len(patients)} patients")
    except Exception as e:
        print(f"⚠️  Could not calculate risk scores: {e}")
    
    conn.close()
    print(f"✅ Generated {num_patients} patients with vitals and notes")

if __name__ == '__main__':
    generate_demo_data(50)
