# Healthcare Analytics Platform 🏥

**AI-powered healthcare analytics for the SEED Hackathon 2025**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/healthcare-analytics)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

🔗 **Live Demo**: [https://your-app.vercel.app](https://your-app.vercel.app)

A simple yet innovative platform demonstrating how AI can transform healthcare decision-making through smart patient risk prediction, real-time visual analytics, and automated clinical note analysis.

## ✨ Key Features

### 🎯 Smart Patient Risk Prediction
- ML-powered readmission risk scoring (0-100 scale)
- Explainable AI showing top 3 risk factors
- Automated recommendations based on risk level
- Color-coded risk levels (Low/Medium/High)

### 📊 Real-time Analytics Dashboard
- Live metrics: Total patients, high-risk count, avg length of stay, readmission rate
- Interactive risk distribution chart
- Auto-refresh every 30 seconds
- Color-coded metric cards for quick insights

### 🤖 AI Clinical Note Analyzer
- Automated extraction of symptoms, diagnoses, medications, and procedures
- Color-coded entity highlighting
- Confidence scores for uncertain extractions
- Structured summary generation

### 📁 Easy Data Management
- One-click demo data loader (50 realistic patients)
- CSV file upload with validation
- Drag-and-drop interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Initialize database and generate demo data
python models/database.py
python models/demo_data.py

# Start server
python app.py
```

Backend runs on **http://localhost:5000**

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on **http://localhost:3000**

## 📖 Usage Guide

1. **Start the Application**
   - Ensure both backend and frontend servers are running
   - Open http://localhost:3000 in your browser

2. **Load Demo Data**
   - Navigate to "Upload Data" page
   - Click "Load Demo Data" button
   - Wait for confirmation (50 patients loaded)

3. **Explore the Dashboard**
   - View key metrics at a glance
   - Check risk distribution chart
   - Metrics auto-refresh every 30 seconds

4. **Browse Patients**
   - Navigate to "Patients" page
   - Filter by risk level (Low/Medium/High)
   - Sort by risk score, admission date, or name

5. **Analyze Clinical Notes**
   - Navigate to "Note Analyzer" page
   - Click "Load Sample" or enter your own note
   - Click "Analyze Note" to extract entities
   - View color-coded symptoms, diagnoses, medications, and procedures

## 🏗️ Project Structure

```
healthcare-analytics-platform/
├── backend/
│   ├── app.py                    # Flask application entry point
│   ├── requirements.txt          # Python dependencies
│   ├── models/
│   │   ├── database.py          # Database schema and initialization
│   │   └── demo_data.py         # Demo data generator
│   ├── routes/
│   │   ├── patients.py          # Patient management endpoints
│   │   ├── dashboard.py         # Dashboard analytics endpoints
│   │   ├── predict.py           # ML prediction endpoints
│   │   └── notes.py             # NLP analysis endpoints
│   └── ml/
│       ├── risk_predictor.py    # Risk prediction model
│       └── nlp_analyzer.py      # Clinical note NLP analyzer
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.jsx       # Navigation component
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx    # Dashboard page
│   │   │   ├── PatientList.jsx  # Patient list page
│   │   │   ├── NoteAnalyzer.jsx # Note analyzer page
│   │   │   └── DataUpload.jsx   # Data upload page
│   │   ├── services/
│   │   │   └── api.js           # API service layer
│   │   ├── App.jsx              # Main app component
│   │   └── main.jsx             # Entry point
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## 🔧 Tech Stack

### Backend
- **Flask** - Lightweight Python web framework
- **scikit-learn** - Machine learning for risk prediction
- **spaCy** - Natural language processing for clinical notes
- **SQLite** - Simple, file-based database
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Recharts** - Composable charting library
- **Axios** - HTTP client for API calls
- **React Router** - Client-side routing

## 🎨 Innovation Highlights

1. **Explainable AI**: Not just predictions, but clear explanations of WHY a patient is at risk
2. **Real-time Intelligence**: Dashboard updates automatically as data changes
3. **Visual Clarity**: Color-coded risk levels and interactive charts for instant insights
4. **AI-Powered Efficiency**: Automated clinical note analysis saves valuable time
5. **Demo-Ready**: One-click demo data for instant exploration

## 📊 API Endpoints

### Dashboard
- `GET /api/dashboard/metrics` - Summary statistics
- `GET /api/dashboard/risk-distribution` - Risk score distribution

### Patients
- `GET /api/patients` - List all patients (with filters)
- `GET /api/patients/:id` - Get patient details
- `POST /api/data/upload` - Upload CSV file
- `POST /api/data/load-demo` - Load demo data

### Predictions
- `POST /api/predict/risk` - Predict patient risk score

### Notes
- `POST /api/notes/analyze` - Analyze clinical note

## 🤝 Contributing

This is a hackathon project for SEED Hackathon 2025. Feel free to fork and build upon it!

## 📝 License

MIT License - feel free to use this project for learning and development.

## 🏆 SEED Hackathon 2025

Built for the Digital Systems domain, addressing the challenge of leveraging big data analytics for enhanced decision-making in healthcare.

**Team**: [Your Team Name]
**Challenge**: Digital Systems - Healthcare Analytics
**Date**: October 2024

---

Made with ❤️ for better healthcare outcomes
