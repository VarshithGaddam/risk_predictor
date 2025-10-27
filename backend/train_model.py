"""
Train the Random Forest ML model on patient data
Run this script after loading demo data to train the model
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import get_db_connection
from ml.risk_predictor import predictor

def train_model():
    """Train ML model on existing patient data"""
    print("🤖 Training Random Forest ML Model...")
    print("=" * 50)
    
    # Get all patients from database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, v.heart_rate, v.blood_pressure_systolic, v.blood_pressure_diastolic,
               v.temperature, v.oxygen_saturation
        FROM patients p
        LEFT JOIN vitals v ON p.patient_id = v.patient_id
    ''')
    
    patients = cursor.fetchall()
    conn.close()
    
    if len(patients) == 0:
        print("❌ No patients found in database!")
        print("💡 Run 'python models/demo_data.py' first to generate demo data")
        return False
    
    print(f"📊 Found {len(patients)} patients in database")
    
    # Convert to list of dicts
    patient_data_list = [dict(patient) for patient in patients]
    
    # Train model
    success = predictor.train_model(patient_data_list)
    
    if success:
        print("\n" + "=" * 50)
        print("✅ Model training complete!")
        print(f"📈 Model Accuracy: {predictor.model_accuracy:.2%}")
        print("💾 Model saved to: risk_model.pkl")
        print("\n🎯 Your platform now uses REAL Machine Learning!")
        print("=" * 50)
    else:
        print("❌ Model training failed")
    
    return success

if __name__ == '__main__':
    train_model()
