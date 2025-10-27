from flask import Blueprint, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_db_connection
from ml.risk_predictor import predictor

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/api/predict/risk', methods=['POST'])
def predict_risk():
    """Predict patient readmission risk"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # If patient_id provided, fetch from database
    if 'patientId' in data:
        patient_id = data['patientId']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, v.heart_rate, v.blood_pressure_systolic, v.blood_pressure_diastolic,
                   v.temperature, v.oxygen_saturation
            FROM patients p
            LEFT JOIN vitals v ON p.patient_id = v.patient_id
            WHERE p.patient_id = ?
        ''', (patient_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Patient not found'}), 404
        
        patient_data = dict(row)
    else:
        # Use provided patient data
        patient_data = data
    
    try:
        prediction = predictor.predict(patient_data)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@predict_bp.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """Calculate risk scores for all patients"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, v.heart_rate, v.blood_pressure_systolic, v.blood_pressure_diastolic,
                   v.temperature, v.oxygen_saturation
            FROM patients p
            LEFT JOIN vitals v ON p.patient_id = v.patient_id
        ''')
        
        patients = cursor.fetchall()
        updated_count = 0
        
        for patient in patients:
            patient_dict = dict(patient)
            prediction = predictor.predict(patient_dict)
            
            cursor.execute('''
                UPDATE patients 
                SET risk_score = ?, risk_level = ?
                WHERE patient_id = ?
            ''', (prediction['riskScore'], prediction['riskLevel'], patient_dict['patient_id']))
            
            updated_count += 1
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'patientsUpdated': updated_count
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
