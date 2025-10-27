import { useState } from 'react'
import { patientsAPI } from '../services/api'
import { useNavigate } from 'react-router-dom'

export default function DataUpload() {
  const [file, setFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState('idle')
  const [message, setMessage] = useState('')
  const navigate = useNavigate()

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.name.endsWith('.csv')) {
      setFile(selectedFile)
      setUploadStatus('idle')
      setMessage('')
    } else {
      alert('Please select a CSV file')
    }
  }

  const handleUpload = async () => {
    if (!file) return

    try {
      setUploadStatus('uploading')
      setMessage('Uploading...')
      
      const response = await patientsAPI.uploadCSV(file)
      
      setUploadStatus('success')
      setMessage(`Successfully uploaded ${response.data.recordsProcessed} records!`)
      setFile(null)
      
      setTimeout(() => {
        navigate('/patients')
      }, 2000)
    } catch (error) {
      setUploadStatus('error')
      setMessage('Error uploading file. Please check the format and try again.')
      console.error('Upload error:', error)
    }
  }

  const handleLoadDemo = async () => {
    try {
      setUploadStatus('uploading')
      setMessage('Loading demo data...')
      
      const response = await patientsAPI.loadDemo()
      
      setUploadStatus('success')
      setMessage(`Successfully loaded ${response.data.recordsLoaded} demo patients!`)
      
      setTimeout(() => {
        navigate('/')
      }, 2000)
    } catch (error) {
      setUploadStatus('error')
      setMessage('Error loading demo data. Please try again.')
      console.error('Demo load error:', error)
    }
  }

  const handleCalculateRisks = async () => {
    try {
      setUploadStatus('uploading')
      setMessage('Calculating risk scores...')
      
      const response = await fetch('http://localhost:5000/api/patients/calculate-risks', {
        method: 'POST'
      })
      const data = await response.json()
      
      setUploadStatus('success')
      setMessage(`Calculated risk scores for ${data.patientsUpdated} patients!`)
      
      setTimeout(() => {
        navigate('/patients')
      }, 2000)
    } catch (error) {
      setUploadStatus('error')
      setMessage('Error calculating risks. Please try again.')
      console.error('Risk calculation error:', error)
    }
  }

  const handleTrainModel = async () => {
    try {
      setUploadStatus('uploading')
      setMessage('Training ML model... This may take a moment.')
      
      const response = await fetch('http://localhost:5000/api/ml/train', {
        method: 'POST'
      })
      const data = await response.json()
      
      if (data.success) {
        setUploadStatus('success')
        setMessage(`🤖 ML Model trained! Accuracy: ${(data.accuracy * 100).toFixed(1)}% on ${data.message}`)
      } else {
        setUploadStatus('error')
        setMessage(data.error || 'Training failed')
      }
    } catch (error) {
      setUploadStatus('error')
      setMessage('Error training model. Please try again.')
      console.error('Training error:', error)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Upload Data</h2>

      {/* Demo Data Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-xl font-bold text-gray-800 mb-3">🚀 Quick Start</h3>
        <p className="text-gray-600 mb-4">
          Load demo data and train the ML model to see AI-powered risk prediction in action!
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            onClick={handleLoadDemo}
            disabled={uploadStatus === 'uploading'}
            className="bg-success text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            1️⃣ Load Demo Data
          </button>
          <button
            onClick={handleTrainModel}
            disabled={uploadStatus === 'uploading'}
            className="bg-primary text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            2️⃣ Train ML Model
          </button>
          <button
            onClick={handleCalculateRisks}
            disabled={uploadStatus === 'uploading'}
            className="bg-warning text-white px-6 py-3 rounded-lg font-medium hover:bg-yellow-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            3️⃣ Calculate Risks
          </button>
        </div>
        <div className="mt-3 p-3 bg-blue-50 rounded-lg text-sm text-blue-800">
          💡 <strong>Tip:</strong> Click buttons in order for best results. Training takes ~5 seconds.
        </div>
      </div>

      {/* CSV Upload Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-3">Upload CSV File</h3>
        <p className="text-gray-600 mb-4">
          Upload a CSV file with patient data. Required columns: patient_id, name, age, admission_date, diagnosis
        </p>

        {/* File Input */}
        <div className="mb-4">
          <label className="block w-full">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer">
              <div className="text-4xl mb-2">📁</div>
              <div className="text-gray-600">
                {file ? (
                  <span className="font-medium text-primary">{file.name}</span>
                ) : (
                  <>
                    <span className="font-medium text-primary">Click to select</span> or drag and drop
                  </>
                )}
              </div>
              <div className="text-sm text-gray-500 mt-1">CSV files only</div>
            </div>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>
        </div>

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          disabled={!file || uploadStatus === 'uploading'}
          className="w-full bg-primary text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {uploadStatus === 'uploading' ? 'Uploading...' : 'Upload File'}
        </button>

        {/* Status Message */}
        {message && (
          <div className={`mt-4 p-4 rounded-lg ${
            uploadStatus === 'success' ? 'bg-green-100 text-green-800' :
            uploadStatus === 'error' ? 'bg-red-100 text-red-800' :
            'bg-blue-100 text-blue-800'
          }`}>
            {message}
          </div>
        )}

        {/* CSV Format Help */}
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">CSV Format Example:</h4>
          <pre className="text-xs text-gray-600 overflow-x-auto">
{`patient_id,name,age,gender,admission_date,diagnosis,previous_admissions,comorbidities
P00001,John Doe,65,M,2024-01-15,Type 2 Diabetes,2,3`}
          </pre>
        </div>
      </div>
    </div>
  )
}
