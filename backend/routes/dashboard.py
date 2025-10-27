from flask import Blueprint, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_db_connection
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/metrics', methods=['GET'])
def get_metrics():
    """Get summary metrics for dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total patients
    cursor.execute('SELECT COUNT(*) as count FROM patients')
    total_patients = cursor.fetchone()['count']
    
    # High risk patients
    cursor.execute("SELECT COUNT(*) as count FROM patients WHERE risk_level = 'high'")
    high_risk_count = cursor.fetchone()['count']
    
    # Average length of stay
    cursor.execute('''
        SELECT AVG(
            CASE 
                WHEN discharge_date IS NOT NULL 
                THEN julianday(discharge_date) - julianday(admission_date)
                ELSE julianday('now') - julianday(admission_date)
            END
        ) as avg_los
        FROM patients
    ''')
    avg_los = cursor.fetchone()['avg_los'] or 0
    
    # Readmission rate (patients with previous admissions)
    cursor.execute('''
        SELECT 
            COUNT(CASE WHEN previous_admissions > 0 THEN 1 END) * 100.0 / COUNT(*) as rate
        FROM patients
    ''')
    readmission_rate = cursor.fetchone()['rate'] or 0
    
    conn.close()
    
    return jsonify({
        'totalPatients': total_patients,
        'highRiskCount': high_risk_count,
        'avgLengthOfStay': round(avg_los, 1),
        'readmissionRate': round(readmission_rate, 1)
    })

@dashboard_bp.route('/api/dashboard/risk-distribution', methods=['GET'])
def get_risk_distribution():
    """Get risk score distribution for charts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            CASE 
                WHEN risk_score < 20 THEN '0-20'
                WHEN risk_score < 40 THEN '20-40'
                WHEN risk_score < 60 THEN '40-60'
                WHEN risk_score < 80 THEN '60-80'
                ELSE '80-100'
            END as risk_range,
            COUNT(*) as count
        FROM patients
        WHERE risk_score IS NOT NULL
        GROUP BY risk_range
        ORDER BY risk_range
    ''')
    
    rows = cursor.fetchall()
    distribution = [{'riskRange': row['risk_range'], 'count': row['count']} for row in rows]
    
    conn.close()
    return jsonify(distribution)

@dashboard_bp.route('/api/dashboard/age-distribution', methods=['GET'])
def get_age_distribution():
    """Get age distribution for charts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            CASE 
                WHEN age < 30 THEN '18-29'
                WHEN age < 40 THEN '30-39'
                WHEN age < 50 THEN '40-49'
                WHEN age < 60 THEN '50-59'
                WHEN age < 70 THEN '60-69'
                WHEN age < 80 THEN '70-79'
                ELSE '80+'
            END as age_range,
            COUNT(*) as count
        FROM patients
        GROUP BY age_range
        ORDER BY age_range
    ''')
    
    rows = cursor.fetchall()
    distribution = [{'ageRange': row['age_range'], 'count': row['count']} for row in rows]
    
    conn.close()
    return jsonify(distribution)

@dashboard_bp.route('/api/dashboard/diagnosis-breakdown', methods=['GET'])
def get_diagnosis_breakdown():
    """Get diagnosis breakdown for pie chart"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT diagnosis, COUNT(*) as count
        FROM patients
        GROUP BY diagnosis
        ORDER BY count DESC
        LIMIT 8
    ''')
    
    rows = cursor.fetchall()
    breakdown = [{'diagnosis': row['diagnosis'], 'count': row['count']} for row in rows]
    
    conn.close()
    return jsonify(breakdown)

@dashboard_bp.route('/api/dashboard/admissions-timeline', methods=['GET'])
def get_admissions_timeline():
    """Get admissions over time"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            DATE(admission_date) as date,
            COUNT(*) as admissions
        FROM patients
        GROUP BY DATE(admission_date)
        ORDER BY date DESC
        LIMIT 30
    ''')
    
    rows = cursor.fetchall()
    timeline = [{'date': row['date'], 'admissions': row['admissions']} for row in rows]
    timeline.reverse()  # Show oldest to newest
    
    conn.close()
    return jsonify(timeline)

@dashboard_bp.route('/api/dashboard/risk-by-age', methods=['GET'])
def get_risk_by_age():
    """Get average risk score by age group"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            CASE 
                WHEN age < 40 THEN '<40'
                WHEN age < 50 THEN '40-49'
                WHEN age < 60 THEN '50-59'
                WHEN age < 70 THEN '60-69'
                WHEN age < 80 THEN '70-79'
                ELSE '80+'
            END as age_group,
            AVG(risk_score) as avg_risk
        FROM patients
        WHERE risk_score IS NOT NULL
        GROUP BY age_group
        ORDER BY age_group
    ''')
    
    rows = cursor.fetchall()
    data = [{'ageGroup': row['age_group'], 'avgRisk': round(row['avg_risk'], 1)} for row in rows]
    
    conn.close()
    return jsonify(data)
