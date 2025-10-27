import { useState, useEffect } from 'react'
import { patientsAPI, predictAPI } from '../services/api'

export default function PatientDetailModal({ patientId, onClose }) {
  const [patient, setPatient] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPatientDetails()
  }, [patientId])

  const fetchPatientDetails = async () => {
    try {
      const [patientRes, predictionRes] = await Promise.all([
        patientsAPI.getById(patientId),
        predictAPI.predictRisk(patientId)
      ])
      setPatient(patientRes.data)
      setPrediction(predictionRes.data)
    } catch (error) {
      console.error('Error fetching patient details:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            <div className="h-32 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!patient) return null

  const getRiskColor = (level) => {
    if (level === 'high') return 'text-red-600 bg-red-100'
    if (level === 'medium') return 'text-yellow-600 bg-yellow-100'
    return 'text-green-600 bg-green-100'
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6 rounded-t-xl">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-3xl font-bold mb-2">{patient.name}</h2>
              <p className="text-blue-100">Patient ID: {patient.patient_id}</p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors"
            >
              ✕
            </button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Risk Assessment */}
          <div className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">🎯 Risk Assessment</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600 mb-1">Risk Score</p>
                <p className="text-4xl font-bold text-blue-600">{patient.risk_score || 'N/A'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Risk Level</p>
                <span className={`inline-block px-4 py-2 rounded-full font-bold text-lg ${getRiskColor(patient.risk_level)}`}>
                  {patient.risk_level?.toUpperCase() || 'N/A'}
                </span>
              </div>
            </div>
          </div>

          {/* Patient Info */}
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-lg font-bold text-gray-800">👤 Patient Information</h3>
              <div className="space-y-2">
                <InfoRow label="Age" value={`${patient.age} years`} />
                <InfoRow label="Gender" value={patient.gender === 'M' ? 'Male' : 'Female'} />
                <InfoRow label="Admission Date" value={new Date(patient.admission_date).toLocaleDateString()} />
                <InfoRow label="Discharge Date" value={patient.discharge_date ? new Date(patient.discharge_date).toLocaleDateString() : 'Still Admitted'} />
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-bold text-gray-800">🏥 Medical History</h3>
              <div className="space-y-2">
                <InfoRow label="Diagnosis" value={patient.diagnosis} />
                <InfoRow label="Previous Admissions" value={patient.previous_admissions || 0} />
                <InfoRow label="Comorbidities" value={patient.comorbidities || 0} />
              </div>
            </div>
          </div>

          {/* Vital Signs */}
          <div>
            <h3 className="text-lg font-bold text-gray-800 mb-4">💓 Vital Signs</h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <VitalCard label="Heart Rate" value={patient.heart_rate} unit="bpm" icon="💓" />
              <VitalCard label="BP Systolic" value={patient.blood_pressure_systolic} unit="mmHg" icon="🩺" />
              <VitalCard label="BP Diastolic" value={patient.blood_pressure_diastolic} unit="mmHg" icon="🩺" />
              <VitalCard label="Temperature" value={patient.temperature} unit="°C" icon="🌡️" />
              <VitalCard label="O2 Saturation" value={patient.oxygen_saturation} unit="%" icon="🫁" />
            </div>
          </div>

          {/* Risk Factors */}
          {prediction && prediction.topFactors && (
            <div>
              <h3 className="text-lg font-bold text-gray-800 mb-4">⚠️ Top Risk Factors</h3>
              <div className="space-y-2">
                {prediction.topFactors.map((factor, index) => (
                  <div key={index} className="flex items-center bg-red-50 border-l-4 border-red-500 p-3 rounded">
                    <span className="text-red-600 font-medium">{index + 1}. {factor}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations */}
          {prediction && prediction.recommendations && (
            <div>
              <h3 className="text-lg font-bold text-gray-800 mb-4">💡 Recommendations</h3>
              <div className="space-y-2">
                {prediction.recommendations.map((rec, index) => (
                  <div key={index} className="flex items-start bg-blue-50 p-3 rounded">
                    <span className="text-blue-600 mr-2">✓</span>
                    <span className="text-gray-700">{rec}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Clinical Notes */}
          {patient.notes && patient.notes.length > 0 && (
            <div>
              <h3 className="text-lg font-bold text-gray-800 mb-4">📝 Clinical Notes</h3>
              <div className="space-y-3">
                {patient.notes.map((note, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600 mb-2">
                      {new Date(note.created_at).toLocaleString()}
                    </p>
                    <p className="text-gray-800">{note.note_text}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 p-6 rounded-b-xl flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

function InfoRow({ label, value }) {
  return (
    <div className="flex justify-between">
      <span className="text-gray-600">{label}:</span>
      <span className="font-medium text-gray-800">{value}</span>
    </div>
  )
}

function VitalCard({ label, value, unit, icon }) {
  return (
    <div className="bg-white border-2 border-gray-200 rounded-lg p-3 text-center">
      <div className="text-2xl mb-1">{icon}</div>
      <div className="text-xs text-gray-600 mb-1">{label}</div>
      <div className="text-lg font-bold text-gray-800">
        {value || 'N/A'}{value && unit}
      </div>
    </div>
  )
}
