from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import blueprints
from routes.patients import patients_bp
from routes.dashboard import dashboard_bp
from routes.predict import predict_bp
from routes.notes import notes_bp

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:3000',
    'http://localhost:5173',
    'https://risk-predictor.vercel.app',
    'https://*.vercel.app'
])

# Configuration
app.config['DATABASE'] = 'healthcare.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Register blueprints
app.register_blueprint(patients_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(notes_bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Healthcare Analytics API is running'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
