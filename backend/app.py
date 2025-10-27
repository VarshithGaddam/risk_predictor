from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import blueprints
from routes.patients import patients_bp
from routes.dashboard import dashboard_bp
from routes.predict import predict_bp
from routes.notes import notes_bp

# Initialize database on startup
from models.database import init_database
init_database()
print("✅ Database initialized")

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
app.config['DATABASE'] = 'healthcare.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Register blueprints
app.register_blueprint(patients_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(notes_bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Healthcare Analytics API is running'})

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'name': 'Healthcare Analytics API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'patients': '/api/patients',
            'dashboard': '/api/dashboard/metrics',
            'upload': '/api/data/upload',
            'demo': '/api/data/load-demo'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
