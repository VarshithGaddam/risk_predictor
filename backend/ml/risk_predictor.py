import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime

class RiskPredictor:
    def __init__(self):
        self.models = {}
        self.active_model = None
        self.active_model_name = 'Random Forest'
        self.scaler = StandardScaler()
        self.feature_names = [
            'age', 'length_of_stay', 'previous_admissions', 'comorbidities',
            'heart_rate', 'bp_systolic', 'bp_diastolic', 'temperature', 'oxygen_saturation',
            'diagnosis_risk'
        ]
        self.diagnosis_risk_map = {
            'Type 2 Diabetes Mellitus': 0.3,
            'Congestive Heart Failure': 0.7,
            'Chronic Obstructive Pulmonary Disease': 0.6,
            'Pneumonia': 0.5,
            'Acute Myocardial Infarction': 0.8,
            'Sepsis': 0.9,
            'Chronic Kidney Disease': 0.6,
            'Stroke': 0.7,
            'Hip Fracture': 0.5,
            'Urinary Tract Infection': 0.3
        }
        self.is_trained = False
        self.model_accuracies = {}
        
        # Try to load pre-trained model
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model if exists"""
        model_path = 'risk_model.pkl'
        scaler_path = 'risk_scaler.pkl'
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                self.active_model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                self.is_trained = True
                print("✅ Loaded pre-trained ML model")
            except Exception as e:
                print(f"⚠️  Could not load model: {e}")
                self.is_trained = False
    
    def _save_model(self):
        """Save trained model"""
        try:
            joblib.dump(self.active_model, 'risk_model.pkl')
            joblib.dump(self.scaler, 'risk_scaler.pkl')
            joblib.dump(self.models, 'all_models.pkl')
            print("✅ Saved trained ML models")
        except Exception as e:
            print(f"⚠️  Could not save models: {e}")
    
    def extract_features(self, patient_data):
        """Extract and normalize features from patient data"""
        # Calculate length of stay
        if patient_data.get('discharge_date'):
            admission = datetime.strptime(patient_data['admission_date'], '%Y-%m-%d')
            discharge = datetime.strptime(patient_data['discharge_date'], '%Y-%m-%d')
            los = (discharge - admission).days
        else:
            # Still admitted - use current date
            admission = datetime.strptime(patient_data['admission_date'], '%Y-%m-%d')
            los = (datetime.now() - admission).days
        
        # Get diagnosis risk score
        diagnosis = patient_data.get('diagnosis', '')
        diagnosis_risk = self.diagnosis_risk_map.get(diagnosis, 0.4)
        
        features = {
            'age': patient_data.get('age', 50),
            'length_of_stay': max(los, 0),
            'previous_admissions': patient_data.get('previous_admissions', 0),
            'comorbidities': patient_data.get('comorbidities', 0),
            'heart_rate': patient_data.get('heart_rate', 75),
            'bp_systolic': patient_data.get('blood_pressure_systolic', 120),
            'bp_diastolic': patient_data.get('blood_pressure_diastolic', 80),
            'temperature': patient_data.get('temperature', 37.0),
            'oxygen_saturation': patient_data.get('oxygen_saturation', 98),
            'diagnosis_risk': diagnosis_risk
        }
        
        return features
    
    def train_all_models(self, patient_data_list):
        """Train multiple ML models and compare performance"""
        if len(patient_data_list) < 10:
            print("⚠️  Need at least 10 patients to train models")
            return False
        
        # Extract features for all patients
        X = []
        y = []
        
        for patient in patient_data_list:
            features = self.extract_features(patient)
            feature_vector = [features[name] for name in self.feature_names]
            X.append(feature_vector)
            
            # Generate synthetic labels based on risk factors
            is_high_risk = (
                features['age'] > 70 or
                features['previous_admissions'] > 2 or
                features['diagnosis_risk'] > 0.6 or
                features['heart_rate'] > 100 or
                features['oxygen_saturation'] < 93
            )
            y.append(1 if is_high_risk else 0)
        
        X = np.array(X)
        y = np.array(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define models to train
        model_configs = {
            'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'Decision Tree': DecisionTreeClassifier(max_depth=10, random_state=42)
        }
        
        # Train all models
        results = {}
        for name, model in model_configs.items():
            model.fit(X_train_scaled, y_train)
            accuracy = model.score(X_test_scaled, y_test)
            self.models[name] = model
            self.model_accuracies[name] = accuracy
            results[name] = accuracy
            print(f"✅ {name}: {accuracy:.2%} accuracy")
        
        # Set best model as active
        best_model_name = max(results, key=results.get)
        self.active_model = self.models[best_model_name]
        self.active_model_name = best_model_name
        self.is_trained = True
        
        print(f"\n🏆 Best Model: {best_model_name} with {results[best_model_name]:.2%} accuracy")
        
        # Save models
        self._save_model()
        
        return results
    
    def train_model(self, patient_data_list):
        """Train models (wrapper for backward compatibility)"""
        return self.train_all_models(patient_data_list)
    
    def calculate_risk_score(self, patient_data):
        """Calculate risk score using rule-based system (for demo without trained model)"""
        features = self.extract_features(patient_data)
        
        # Base risk from diagnosis
        diagnosis = patient_data.get('diagnosis', '')
        base_risk = self.diagnosis_risk_map.get(diagnosis, 0.4)
        
        # Age factor (higher age = higher risk)
        age_factor = min((features['age'] - 25) / 65, 1.0) * 0.3
        
        # Previous admissions factor
        admission_factor = min(features['previous_admissions'] / 5, 1.0) * 0.2
        
        # Comorbidities factor
        comorbidity_factor = min(features['comorbidities'] / 4, 1.0) * 0.15
        
        # Vital signs factors
        vital_risk = 0
        if features['heart_rate'] > 100 or features['heart_rate'] < 60:
            vital_risk += 0.1
        if features['bp_systolic'] > 140 or features['bp_systolic'] < 100:
            vital_risk += 0.1
        if features['temperature'] > 38.0:
            vital_risk += 0.1
        if features['oxygen_saturation'] < 95:
            vital_risk += 0.15
        
        # Length of stay factor
        los_factor = min(features['length_of_stay'] / 14, 1.0) * 0.1
        
        # Calculate total risk (0-1)
        total_risk = base_risk + age_factor + admission_factor + comorbidity_factor + vital_risk + los_factor
        total_risk = min(total_risk, 1.0)
        
        # Convert to 0-100 scale
        risk_score = int(total_risk * 100)
        
        return risk_score, features
    
    def get_risk_level(self, risk_score):
        """Convert risk score to risk level"""
        if risk_score < 40:
            return 'low'
        elif risk_score < 70:
            return 'medium'
        else:
            return 'high'
    
    def get_top_risk_factors(self, patient_data, features):
        """Identify top contributing risk factors"""
        factors = []
        
        # Check age
        if features['age'] > 70:
            factors.append(f"Advanced age ({features['age']} years)")
        
        # Check previous admissions
        if features['previous_admissions'] >= 2:
            factors.append(f"Multiple previous admissions ({features['previous_admissions']})")
        
        # Check comorbidities
        if features['comorbidities'] >= 2:
            factors.append(f"Multiple comorbidities ({features['comorbidities']})")
        
        # Check vitals
        if features['heart_rate'] > 100:
            factors.append(f"Elevated heart rate ({features['heart_rate']} bpm)")
        elif features['heart_rate'] < 60:
            factors.append(f"Low heart rate ({features['heart_rate']} bpm)")
        
        if features['bp_systolic'] > 140:
            factors.append(f"High blood pressure ({features['bp_systolic']}/{features['bp_diastolic']} mmHg)")
        
        if features['temperature'] > 38.0:
            factors.append(f"Fever ({features['temperature']}°C)")
        
        if features['oxygen_saturation'] < 95:
            factors.append(f"Low oxygen saturation ({features['oxygen_saturation']}%)")
        
        # Check diagnosis
        diagnosis = patient_data.get('diagnosis', '')
        if self.diagnosis_risk_map.get(diagnosis, 0) >= 0.6:
            factors.append(f"High-risk diagnosis: {diagnosis}")
        
        # Check length of stay
        if features['length_of_stay'] > 7:
            factors.append(f"Extended hospital stay ({features['length_of_stay']} days)")
        
        # Return top 3 factors
        return factors[:3] if factors else ["No significant risk factors identified"]
    
    def get_recommendations(self, risk_level, factors):
        """Generate recommendations based on risk level"""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.append("Schedule follow-up within 7 days of discharge")
            recommendations.append("Consider home health services")
            recommendations.append("Ensure medication reconciliation")
        elif risk_level == 'medium':
            recommendations.append("Schedule follow-up within 14 days")
            recommendations.append("Provide patient education materials")
        else:
            recommendations.append("Standard discharge protocol")
            recommendations.append("Follow-up as needed")
        
        return recommendations
    
    def predict(self, patient_data):
        """Main prediction method using ML model or fallback to rule-based"""
        features = self.extract_features(patient_data)
        
        if self.is_trained and self.active_model is not None:
            # Use ML model
            feature_vector = np.array([[features[name] for name in self.feature_names]])
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            # Get probability prediction
            risk_probability = self.active_model.predict_proba(feature_vector_scaled)[0][1]
            risk_score = int(risk_probability * 100)
            
            confidence = self.model_accuracies.get(self.active_model_name, 0.85)
        else:
            # Fallback to rule-based
            risk_score, _ = self.calculate_risk_score(patient_data)
            confidence = 0.75
        
        risk_level = self.get_risk_level(risk_score)
        top_factors = self.get_top_risk_factors(patient_data, features)
        recommendations = self.get_recommendations(risk_level, top_factors)
        
        return {
            'riskScore': risk_score,
            'riskLevel': risk_level,
            'topFactors': top_factors,
            'confidence': round(confidence, 2),
            'recommendations': recommendations,
            'modelType': self.active_model_name if self.is_trained else 'Rule-Based'
        }
    
    def get_model_comparison(self):
        """Get comparison of all trained models"""
        if not self.models:
            return None
        
        comparison = []
        for name, accuracy in self.model_accuracies.items():
            comparison.append({
                'name': name,
                'accuracy': round(accuracy, 4),
                'isActive': name == self.active_model_name
            })
        
        return sorted(comparison, key=lambda x: x['accuracy'], reverse=True)

# Global predictor instance
predictor = RiskPredictor()
