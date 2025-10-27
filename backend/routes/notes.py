from flask import Blueprint, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.nlp_analyzer import analyzer

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/api/notes/analyze', methods=['POST'])
def analyze_note():
    """Analyze clinical note and extract entities"""
    data = request.get_json()
    
    if not data or 'noteText' not in data:
        return jsonify({'error': 'No note text provided'}), 400
    
    note_text = data['noteText']
    
    try:
        result = analyzer.analyze_note(note_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
