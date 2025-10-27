# Design Document

## Overview

A full-stack web application built with modern technologies to demonstrate AI-powered healthcare analytics. The system uses a Python backend with Flask for APIs and machine learning, a React frontend for the dashboard, and SQLite for simple data storage. The architecture prioritizes simplicity and demo-ability while showcasing real ML capabilities.

**Tech Stack:**
- **Frontend:** React + Vite, TailwindCSS, Recharts for visualizations
- **Backend:** Python Flask, scikit-learn for ML, spaCy for NLP
- **Database:** SQLite (simple, no setup required)
- **Deployment:** Can run locally or deploy to Vercel (frontend) + Render/Railway (backend)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Vite)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dashboard   │  │  Patients    │  │  Note        │      │
│  │  Page        │  │  List Page   │  │  Analyzer    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                    HTTP REST API (JSON)
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Flask Backend API                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Patient     │  │  Risk        │  │  NLP         │      │
│  │  Routes      │  │  Predictor   │  │  Analyzer    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                    SQLite Database
                            │
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  patients    │  │  vitals      │  │  notes       │      │
│  │  table       │  │  table       │  │  table       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Frontend Components

#### 1. Dashboard Component
- **Purpose:** Main landing page showing key metrics and charts
- **State:** 
  - `metrics`: Object with totalPatients, highRiskCount, avgLengthOfStay, readmissionRate
  - `riskDistribution`: Array for chart data
  - `loading`: Boolean
- **API Calls:**
  - `GET /api/dashboard/metrics` - Fetch summary statistics
  - `GET /api/dashboard/risk-distribution` - Get risk score distribution data

#### 2. PatientList Component
- **Purpose:** Display all patients with risk scores and filtering
- **State:**
  - `patients`: Array of patient objects
  - `filters`: Object with riskLevel, diagnosis filters
  - `sortBy`: String (risk, date, name)
- **API Calls:**
  - `GET /api/patients?risk={level}&sort={field}` - Fetch filtered patient list
  - `GET /api/patients/{id}` - Get individual patient details

#### 3. NoteAnalyzer Component
- **Purpose:** Input clinical notes and display AI-extracted entities
- **State:**
  - `noteText`: String (user input)
  - `extractedEntities`: Object with symptoms, diagnoses, medications, procedures
  - `processing`: Boolean
- **API Calls:**
  - `POST /api/notes/analyze` - Send note text, receive extracted entities

#### 4. DataUpload Component
- **Purpose:** Upload CSV files or load demo data
- **State:**
  - `file`: File object
  - `uploadStatus`: String (idle, uploading, success, error)
  - `recordCount`: Number
- **API Calls:**
  - `POST /api/data/upload` - Upload CSV file
  - `POST /api/data/load-demo` - Load sample data

### Backend API Endpoints

#### Patient Management
```
GET /api/patients
- Query params: risk (low/medium/high), sort (risk/date/name), limit
- Returns: Array of patient objects with risk scores

GET /api/patients/{id}
- Returns: Detailed patient object with full history

POST /api/data/upload
- Body: multipart/form-data with CSV file
- Returns: {success: boolean, recordsProcessed: number}

POST /api/data/load-demo
- Returns: {success: boolean, recordsLoaded: number}
```

#### Dashboard Analytics
```
GET /api/dashboard/metrics
- Returns: {
    totalPatients: number,
    highRiskCount: number,
    avgLengthOfStay: number,
    readmissionRate: number
  }

GET /api/dashboard/risk-distribution
- Returns: Array of {riskRange: string, count: number}
```

#### ML Prediction
```
POST /api/predict/risk
- Body: {patientId: string} or patient data object
- Returns: {
    riskScore: number (0-100),
    riskLevel: string (low/medium/high),
    topFactors: Array of strings,
    confidence: number,
    recommendations: Array of strings
  }
```

#### NLP Analysis
```
POST /api/notes/analyze
- Body: {noteText: string}
- Returns: {
    symptoms: Array of {text: string, confidence: number},
    diagnoses: Array of {text: string, confidence: number},
    medications: Array of {text: string, confidence: number},
    procedures: Array of {text: string, confidence: number},
    summary: string
  }
```

## Data Models

### Patient Table
```sql
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT,
    admission_date TEXT NOT NULL,
    discharge_date TEXT,
    diagnosis TEXT NOT NULL,
    risk_score REAL,
    risk_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Vitals Table
```sql
CREATE TABLE vitals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    heart_rate INTEGER,
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    temperature REAL,
    oxygen_saturation INTEGER,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
```

### Notes Table
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    note_text TEXT NOT NULL,
    extracted_entities TEXT, -- JSON string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
```

## Machine Learning Model

### Risk Prediction Model

**Algorithm:** Random Forest Classifier (simple, interpretable, works well with small datasets)

**Features:**
- Age (normalized)
- Length of stay (days)
- Number of previous admissions
- Vital signs (heart rate, BP, temperature, O2 saturation)
- Diagnosis category (encoded)
- Comorbidity count

**Training Approach:**
1. Use synthetic/demo data for initial model
2. Features are scaled using StandardScaler
3. Model trained with 80/20 train-test split
4. Feature importance extracted for explainability

**Output:**
- Risk probability (0-1) converted to score (0-100)
- Risk level: Low (<40), Medium (40-70), High (>70)
- Top 3 contributing features with explanations

**Model Storage:** Saved as `risk_model.pkl` using joblib

### NLP Entity Extraction

**Library:** spaCy with `en_core_web_sm` model

**Approach:**
1. Load pre-trained spaCy model
2. Process clinical note text
3. Extract entities using pattern matching and NER
4. Custom patterns for medical terms:
   - Symptoms: Pattern matching for common symptoms
   - Diagnoses: Medical condition entities
   - Medications: Drug name patterns
   - Procedures: Medical procedure patterns

**Enhancement:** Use scispaCy for better medical entity recognition (optional upgrade)

## Error Handling

### Frontend Error Handling
- API call failures: Show toast notifications with retry option
- Invalid file uploads: Display validation errors inline
- Network errors: Show offline indicator and queue requests
- Loading states: Skeleton screens for better UX

### Backend Error Handling
```python
# Standard error response format
{
    "error": true,
    "message": "Human-readable error message",
    "code": "ERROR_CODE",
    "details": {} # Optional additional info
}
```

**Error Codes:**
- `INVALID_INPUT`: Validation errors
- `NOT_FOUND`: Resource doesn't exist
- `MODEL_ERROR`: ML prediction failed
- `DATABASE_ERROR`: Data access issues
- `SERVER_ERROR`: Unexpected errors

## Testing Strategy

### Frontend Testing
- **Component Tests:** React Testing Library for key components
- **Focus Areas:**
  - Dashboard renders metrics correctly
  - Patient list filtering works
  - Note analyzer displays extracted entities
  - File upload validation

### Backend Testing
- **Unit Tests:** pytest for individual functions
- **Focus Areas:**
  - Risk prediction model returns valid scores
  - NLP extraction identifies entities correctly
  - API endpoints return correct status codes
  - Database operations work as expected

### Integration Testing
- **End-to-End:** Manual testing of complete workflows
- **Test Scenarios:**
  1. Upload data → View dashboard → Check metrics update
  2. Select patient → View risk score → See recommendations
  3. Enter clinical note → Analyze → Verify extracted entities
  4. Load demo data → Verify all features work

### Demo Data
- 50 realistic patient records with varied risk profiles
- Mix of diagnoses (diabetes, heart disease, pneumonia, etc.)
- Realistic vital signs and admission patterns
- Sample clinical notes for NLP testing

## Deployment Considerations

### Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py

# Frontend
cd frontend
npm install
npm run dev
```

### Production Deployment
- **Frontend:** Vercel (automatic deployment from Git)
- **Backend:** Render or Railway (free tier with Python support)
- **Database:** SQLite file persisted in backend container
- **Environment Variables:** API URL, model paths

### Performance Optimization
- Frontend: Code splitting, lazy loading for routes
- Backend: Response caching for dashboard metrics
- Database: Indexes on patient_id and risk_score
- ML Model: Load once at startup, keep in memory

## Innovation Highlights

1. **Explainable AI:** Not just risk scores, but WHY a patient is at risk
2. **Real-time Updates:** Dashboard refreshes automatically as data changes
3. **Visual Intelligence:** Color-coded risk levels, interactive charts
4. **AI-Powered Efficiency:** Automated clinical note analysis saves time
5. **Demo-Ready:** One-click demo data loading for presentations
