import { useState } from 'react'
import { notesAPI } from '../services/api'

export default function NoteAnalyzer() {
  const [noteText, setNoteText] = useState('')
  const [result, setResult] = useState(null)
  const [processing, setProcessing] = useState(false)

  const sampleNote = "Patient presents with shortness of breath and chest pain. Diagnosed with acute myocardial infarction. Started on aspirin 325mg and atorvastatin 80mg. Scheduled for cardiac catheterization."

  const handleAnalyze = async () => {
    if (!noteText.trim()) return

    try {
      setProcessing(true)
      const response = await notesAPI.analyze(noteText)
      setResult(response.data)
    } catch (error) {
      console.error('Error analyzing note:', error)
      alert('Error analyzing note. Please try again.')
    } finally {
      setProcessing(false)
    }
  }

  const loadSample = () => {
    setNoteText(sampleNote)
  }

  const EntityList = ({ title, entities, color }) => (
    <div className="mb-4">
      <h4 className="font-semibold text-gray-700 mb-2">{title}</h4>
      {entities && entities.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {entities.map((entity, index) => (
            <span
              key={index}
              className={`px-3 py-1 rounded-full text-white text-sm ${color}`}
            >
              {entity.text}
              {entity.confidence < 0.8 && (
                <span className="ml-1 text-xs opacity-75">
                  ({Math.round(entity.confidence * 100)}%)
                </span>
              )}
            </span>
          ))}
        </div>
      ) : (
        <p className="text-gray-500 text-sm">None detected</p>
      )}
    </div>
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl shadow-lg p-8 text-white">
        <h2 className="text-4xl font-bold mb-2">🤖 AI Clinical Note Analyzer</h2>
        <p className="text-purple-100">Extract medical entities using Natural Language Processing</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Section */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center mb-4">
            <span className="text-2xl mr-3">📝</span>
            <h3 className="text-xl font-bold text-gray-800">Clinical Note Input</h3>
          </div>
          
          <textarea
            value={noteText}
            onChange={(e) => setNoteText(e.target.value)}
            placeholder="Enter clinical note here... (e.g., Patient presents with chest pain, fever, shortness of breath...)"
            className="w-full h-64 border-2 border-gray-200 rounded-lg p-4 mb-4 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-200 font-mono text-sm"
          />

          <div className="flex gap-3">
            <button
              onClick={handleAnalyze}
              disabled={processing || !noteText.trim()}
              className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-lg font-medium hover:from-purple-700 hover:to-pink-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
            >
              {processing ? '🔄 Analyzing...' : '🤖 Analyze with AI'}
            </button>
            
            <button
              onClick={loadSample}
              className="px-6 py-3 border-2 border-purple-300 text-purple-600 rounded-lg font-medium hover:bg-purple-50 transition-all duration-200"
            >
              📋 Load Sample
            </button>
          </div>
        </div>

        {/* Results Section */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center mb-4">
            <span className="text-2xl mr-3">✨</span>
            <h3 className="text-xl font-bold text-gray-800">AI Extracted Entities</h3>
          </div>

          {result ? (
            <div>
              <EntityList 
                title="Symptoms" 
                entities={result.symptoms} 
                color="bg-blue-500" 
              />
              
              <EntityList 
                title="Diagnoses" 
                entities={result.diagnoses} 
                color="bg-danger" 
              />
              
              <EntityList 
                title="Medications" 
                entities={result.medications} 
                color="bg-success" 
              />
              
              <EntityList 
                title="Procedures" 
                entities={result.procedures} 
                color="bg-purple-500" 
              />

              {/* Summary */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h4 className="font-semibold text-gray-700 mb-2">Summary</h4>
                <p className="text-gray-600 text-sm">{result.summary}</p>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-500">
              Enter a clinical note and click "Analyze Note" to see extracted entities
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
