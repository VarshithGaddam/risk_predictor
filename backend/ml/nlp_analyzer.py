import spacy
import re

class NLPAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("⚠️  spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Medical entity patterns
        self.symptom_patterns = [
            'pain', 'fever', 'cough', 'shortness of breath', 'chest pain', 'headache',
            'nausea', 'vomiting', 'dizziness', 'fatigue', 'weakness', 'difficulty breathing',
            'edema', 'swelling', 'bleeding', 'confusion', 'dyspnea'
        ]
        
        self.medication_patterns = [
            'aspirin', 'atorvastatin', 'metformin', 'lisinopril', 'amlodipine',
            'metoprolol', 'furosemide', 'insulin', 'warfarin', 'clopidogrel',
            'morphine', 'ceftriaxone', 'azithromycin', 'vancomycin', 'heparin'
        ]
        
        self.procedure_patterns = [
            'catheterization', 'surgery', 'intubation', 'dialysis', 'transfusion',
            'biopsy', 'endoscopy', 'angioplasty', 'repair', 'resection'
        ]
        
        self.diagnosis_patterns = [
            'diabetes', 'hypertension', 'heart failure', 'pneumonia', 'sepsis',
            'myocardial infarction', 'stroke', 'fracture', 'infection', 'copd',
            'kidney disease', 'ketoacidosis'
        ]
    
    def extract_entities(self, text):
        """Extract medical entities from clinical note"""
        text_lower = text.lower()
        
        # Extract symptoms
        symptoms = []
        for symptom in self.symptom_patterns:
            if symptom in text_lower:
                # Find actual occurrence in original text
                pattern = re.compile(re.escape(symptom), re.IGNORECASE)
                matches = pattern.finditer(text)
                for match in matches:
                    symptoms.append({
                        'text': match.group(),
                        'confidence': 0.9
                    })
        
        # Extract medications
        medications = []
        for med in self.medication_patterns:
            if med in text_lower:
                pattern = re.compile(re.escape(med), re.IGNORECASE)
                matches = pattern.finditer(text)
                for match in matches:
                    # Extract dosage if present
                    dosage_pattern = r'(\d+\s*(?:mg|g|ml|mcg))'
                    dosage_match = re.search(dosage_pattern, text[max(0, match.start()-10):match.end()+20])
                    med_text = match.group()
                    if dosage_match:
                        med_text += f" {dosage_match.group()}"
                    medications.append({
                        'text': med_text,
                        'confidence': 0.95
                    })
        
        # Extract procedures
        procedures = []
        for proc in self.procedure_patterns:
            if proc in text_lower:
                pattern = re.compile(re.escape(proc), re.IGNORECASE)
                matches = pattern.finditer(text)
                for match in matches:
                    procedures.append({
                        'text': match.group(),
                        'confidence': 0.85
                    })
        
        # Extract diagnoses
        diagnoses = []
        for diag in self.diagnosis_patterns:
            if diag in text_lower:
                pattern = re.compile(re.escape(diag), re.IGNORECASE)
                matches = pattern.finditer(text)
                for match in matches:
                    diagnoses.append({
                        'text': match.group(),
                        'confidence': 0.9
                    })
        
        # Use spaCy for additional entity extraction if available
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ['DISEASE', 'SYMPTOM', 'DRUG']:
                    # Add to appropriate category if not already found
                    entity_text = ent.text
                    if ent.label_ == 'DISEASE' and not any(d['text'].lower() == entity_text.lower() for d in diagnoses):
                        diagnoses.append({'text': entity_text, 'confidence': 0.75})
        
        return {
            'symptoms': symptoms[:5],  # Limit to top 5
            'diagnoses': diagnoses[:5],
            'medications': medications[:5],
            'procedures': procedures[:5]
        }
    
    def generate_summary(self, entities):
        """Generate a comprehensive clinical summary from extracted entities"""
        summary_parts = []
        
        # Generate intelligent summary based on what was found
        if entities['diagnoses'] and entities['symptoms']:
            diagnoses = [d['text'] for d in entities['diagnoses']]
            symptoms = [s['text'] for s in entities['symptoms']]
            summary_parts.append(f"Patient presents with {', '.join(symptoms[:3])} consistent with {', '.join(diagnoses[:2])}.")
        elif entities['diagnoses']:
            diagnoses = [d['text'] for d in entities['diagnoses']]
            summary_parts.append(f"Patient diagnosed with {', '.join(diagnoses[:2])}.")
        elif entities['symptoms']:
            symptoms = [s['text'] for s in entities['symptoms']]
            summary_parts.append(f"Patient presenting with {', '.join(symptoms[:3])}.")
        
        # Add treatment information
        if entities['medications']:
            meds = [m['text'] for m in entities['medications'][:3]]
            summary_parts.append(f"Treatment initiated with {', '.join(meds)}.")
        
        # Add procedures if any
        if entities['procedures']:
            procs = [p['text'] for p in entities['procedures'][:2]]
            summary_parts.append(f"Procedures planned/performed: {', '.join(procs)}.")
        
        # Generate overall assessment
        if len(entities['diagnoses']) > 0 or len(entities['symptoms']) > 0:
            severity = "complex" if (len(entities['diagnoses']) > 1 or len(entities['medications']) > 2) else "standard"
            summary_parts.append(f"This appears to be a {severity} case requiring appropriate medical attention.")
        
        return ' '.join(summary_parts) if summary_parts else "Unable to generate clinical summary. Please ensure the note contains medical information."
    
    def analyze_note(self, note_text):
        """Main analysis method"""
        if not note_text or not note_text.strip():
            return {
                'symptoms': [],
                'diagnoses': [],
                'medications': [],
                'procedures': [],
                'summary': 'No text provided for analysis.'
            }
        
        entities = self.extract_entities(note_text)
        summary = self.generate_summary(entities)
        
        return {
            'symptoms': entities['symptoms'],
            'diagnoses': entities['diagnoses'],
            'medications': entities['medications'],
            'procedures': entities['procedures'],
            'summary': summary
        }

# Global analyzer instance
analyzer = NLPAnalyzer()
