from flask import Blueprint, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_db_connection
from models.demo_data import generate_demo_data
from ml.risk_predictor import predictor
import csv
import io

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients with optional filtering and sorting"""
    risk_filter = request.args.get('risk')
    sort_by = request.args.get('sort', 'risk')
    limit = request.args.get('limit', 100, type=int)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query
    query = '''
        SELECT p.*, v.heart_rate, v.blood_pressure_systolic, v.blood_pressure_diastolic,
               v.temperature, v.oxygen_saturation
        FROM patients p
        LEFT JOIN vitals v ON p.patient_id = v.patient_id
        WHERE 1=1
    '''
    params = []
    
    if risk_filter:
        query += ' AND p.risk_level = ?'
        params.append(risk_filter)
    
    # Add sorting
    if sort_by == 'risk':
        query += ' ORDER BY p.risk_score DESC'
    elif sort_by == 'date':
        query += ' ORDER BY p.admission_date DESC'
    elif sort_by == 'name':
        query += ' ORDER BY p.name ASC'
    
    query += f' LIMIT {limit}'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    patients = []
    for row in rows:
        patient = dict(row)
        patients.append(patient)
    
    conn.close()
    return jsonify(patients)

@patients_bp.route('/api/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get detailed patient information"""
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
    if not row:
        conn.close()
        return jsonify({'error': 'Patient not found'}), 404
    
    patient = dict(row)
    
    # Get notes
    cursor.execute('SELECT * FROM notes WHERE patient_id = ? ORDER BY created_at DESC', (patient_id,))
    notes = [dict(note) for note in cursor.fetchall()]
    patient['notes'] = notes
    
    conn.close()
    return jsonify(patient)

@patients_bp.route('/api/data/upload', methods=['POST', 'OPTIONS'])
def upload_data():
    """Upload CSV file with patient data"""
    # Handle preflight request
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    print("Upload request received")
    print("Files:", request.files)
    print("Form:", request.form)
    
    if 'file' not in request.files:
        print("Error: No file in request")
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    print(f"File received: {file.filename}")
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be CSV format'}), 400
    
    try:
        # Read CSV
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        records_processed = 0
        for row in csv_reader:
            # Insert patient
            cursor.execute('''
                INSERT OR REPLACE INTO patients 
                (patient_id, name, age, gender, admission_date, diagnosis, previous_admissions, comorbidities)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row.get('patient_id'),
                row.get('name'),
                int(row.get('age', 0)),
                row.get('gender'),
                row.get('admission_date'),
                row.get('diagnosis'),
                int(row.get('previous_admissions', 0)),
                int(row.get('comorbidities', 0))
            ))
            
            # Insert vitals if provided
            if 'heart_rate' in row:
                cursor.execute('''
                    INSERT INTO vitals 
                    (patient_id, heart_rate, blood_pressure_systolic, blood_pressure_diastolic, temperature, oxygen_saturation)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('patient_id'),
                    int(row.get('heart_rate', 75)),
                    int(row.get('blood_pressure_systolic', 120)),
                    int(row.get('blood_pressure_diastolic', 80)),
                    float(row.get('temperature', 37.0)),
                    int(row.get('oxygen_saturation', 98))
                ))
            
            records_processed += 1
        
        conn.commit()
        
        # Calculate risk scores for uploaded patients
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
        conn.close()
        
        return jsonify({
            'success': True,
            'recordsProcessed': records_processed,
            'message': f'Uploaded {records_processed} patients and calculated risk scores'
        })
    
    except Exception as e:
        print(f"Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@patients_bp.route('/api/ml/train', methods=['POST'])
def train_ml_model():
    """Train multiple ML models and compare performance"""
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
        conn.close()
        
        if len(patients) < 10:
            return jsonify({
                'error': 'Need at least 10 patients to train models',
                'currentCount': len(patients)
            }), 400
        
        # Convert to list of dicts
        patient_data_list = [dict(patient) for patient in patients]
        
        # Train all models
        results = predictor.train_all_models(patient_data_list)
        
        if results:
            return jsonify({
                'success': True,
                'message': f'Trained 4 models on {len(patients)} patients',
                'results': results,
                'bestModel': predictor.active_model_name,
                'bestAccuracy': round(predictor.model_accuracies[predictor.active_model_name], 4)
            })
        else:
            return jsonify({'error': 'Model training failed'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients_bp.route('/api/ml/comparison', methods=['GET'])
def get_model_comparison():
    """Get comparison of all trained models"""
    try:
        comparison = predictor.get_model_comparison()
        
        if comparison is None:
            return jsonify({
                'trained': False,
                'message': 'No models trained yet'
            })
        
        return jsonify({
            'trained': True,
            'models': comparison,
            'activeModel': predictor.active_model_name
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients_bp.route('/api/patients/calculate-risks', methods=['POST'])
def calculate_all_risks():
    """Manually trigger risk calculation for all patients"""
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
        updated = 0
        
        for patient in patients:
            patient_dict = dict(patient)
            try:
                prediction = predictor.predict(patient_dict)
                
                cursor.execute('''
                    UPDATE patients 
                    SET risk_score = ?, risk_level = ?
                    WHERE patient_id = ?
                ''', (prediction['riskScore'], prediction['riskLevel'], patient_dict['patient_id']))
                updated += 1
            except Exception as e:
                print(f"Error calculating risk for {patient_dict.get('patient_id')}: {e}")
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'patientsUpdated': updated,
            'message': f'Calculated risk scores for {updated} patients'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients_bp.route('/api/data/load-demo', methods=['POST'])
def load_demo_data():
    """Load demo patient data"""
    try:
        generate_demo_data(50)
        
        # Calculate risk scores for all patients
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
        conn.close()
        
        return jsonify({
            'success': True,
            'recordsLoaded': 50
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients_bp.route('/api/patients/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a specific patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete related records first
        cursor.execute('DELETE FROM notes WHERE patient_id = ?', (patient_id,))
        cursor.execute('DELETE FROM vitals WHERE patient_id = ?', (patient_id,))
        cursor.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Patient {patient_id} deleted successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients_bp.route('/api/data/clear-all', methods=['DELETE'])
def clear_all_data():
    """Clear all patient data from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete all records
        cursor.execute('DELETE FROM notes')
        cursor.execute('DELETE FROM vitals')
        cursor.execute('DELETE FROM patients')
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'All patient data cleared successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
