import { useState, useEffect } from 'react'
import { patientsAPI } from '../services/api'
import PatientDetailModal from '../components/PatientDetailModal'

export default function PatientList() {
  const [patients, setPatients] = useState([])
  const [filteredPatients, setFilteredPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ risk: '', sort: 'risk' })
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPatientId, setSelectedPatientId] = useState(null)

  useEffect(() => {
    fetchPatients()
  }, [filters])

  useEffect(() => {
    filterPatients()
  }, [patients, searchTerm])

  const fetchPatients = async () => {
    try {
      setLoading(true)
      const response = await patientsAPI.getAll(filters)
      setPatients(response.data)
      setFilteredPatients(response.data)
    } catch (error) {
      console.error('Error fetching patients:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterPatients = () => {
    if (!searchTerm.trim()) {
      setFilteredPatients(patients)
      return
    }

    const term = searchTerm.toLowerCase()
    const filtered = patients.filter(patient =>
      patient.name.toLowerCase().includes(term) ||
      patient.patient_id.toLowerCase().includes(term) ||
      patient.diagnosis.toLowerCase().includes(term)
    )
    setFilteredPatients(filtered)
  }

  const exportToExcel = () => {
    const headers = ['Patient ID', 'Name', 'Age', 'Gender', 'Diagnosis', 'Risk Score', 'Risk Level']
    const rows = filteredPatients.map(p => [
      p.patient_id,
      p.name,
      p.age,
      p.gender,
      p.diagnosis,
      p.risk_score || 'N/A',
      p.risk_level || 'N/A'
    ])

    let csv = headers.join(',') + '\n'
    rows.forEach(row => {
      csv += row.map(cell => `"${cell}"`).join(',') + '\n'
    })

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `patients_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  }

  const handleDeletePatient = async (patientId, patientName) => {
    if (!window.confirm(`Are you sure you want to delete patient ${patientName} (${patientId})?`)) {
      return
    }

    try {
      await patientsAPI.deletePatient(patientId)
      alert('Patient deleted successfully')
      fetchPatients() // Refresh list
    } catch (error) {
      console.error('Error deleting patient:', error)
      alert('Error deleting patient. Please try again.')
    }
  }

  const handleClearAll = async () => {
    if (!window.confirm('⚠️ WARNING: This will delete ALL patient data. Are you sure?')) {
      return
    }
    
    if (!window.confirm('This action cannot be undone. Type YES to confirm.')) {
      return
    }

    try {
      await patientsAPI.clearAll()
      alert('All patient data cleared successfully')
      fetchPatients() // Refresh list
    } catch (error) {
      console.error('Error clearing data:', error)
      alert('Error clearing data. Please try again.')
    }
  }

  const getRiskBadgeColor = (level) => {
    if (level === 'high') return 'bg-danger'
    if (level === 'medium') return 'bg-warning'
    return 'bg-success'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl shadow-lg p-8 text-white">
        <h2 className="text-4xl font-bold mb-2">👥 Patient Management</h2>
        <p className="text-indigo-100">View and filter patients by risk level</p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex flex-col md:flex-row gap-4 mb-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">🔍 Search Patients</label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by name, ID, or diagnosis..."
              className="w-full border-2 border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        <div className="flex justify-between items-end">
          <div className="flex gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Risk Level</label>
              <select
                value={filters.risk}
                onChange={(e) => setFilters({ ...filters, risk: e.target.value })}
                className="border border-gray-300 rounded-lg px-4 py-2"
              >
                <option value="">All</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
              <select
                value={filters.sort}
                onChange={(e) => setFilters({ ...filters, sort: e.target.value })}
                className="border border-gray-300 rounded-lg px-4 py-2"
              >
                <option value="risk">Risk Score</option>
                <option value="date">Admission Date</option>
                <option value="name">Name</option>
              </select>
            </div>
          </div>

          <div className="flex gap-2">
            <button
              onClick={exportToExcel}
              className="px-6 py-2 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors"
            >
              📊 Export to Excel
            </button>
            <button
              onClick={handleClearAll}
              className="px-6 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors"
            >
              🗑️ Clear All
            </button>
          </div>
        </div>
      </div>

      {/* Patient Table */}
      {loading ? (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <div className="animate-spin text-6xl mb-4">⚕️</div>
          <p className="text-gray-600 text-lg">Loading patients...</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Patient ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Age</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Diagnosis</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Level</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredPatients.map((patient) => (
                <tr 
                  key={patient.patient_id} 
                  onClick={() => setSelectedPatientId(patient.patient_id)}
                  className="hover:bg-blue-50 transition-colors duration-150 cursor-pointer"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {patient.patient_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{patient.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{patient.age}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{patient.diagnosis}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                    {patient.risk_score || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {patient.risk_level && (
                      <span className={`px-3 py-1 rounded-full text-white text-xs font-medium ${getRiskBadgeColor(patient.risk_level)}`}>
                        {patient.risk_level.toUpperCase()}
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDeletePatient(patient.patient_id, patient.name)
                      }}
                      className="text-red-600 hover:text-red-800 font-medium text-sm hover:underline"
                      title="Delete patient"
                    >
                      🗑️ Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredPatients.length === 0 && !loading && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🔍</div>
              <p className="text-xl text-gray-600 mb-2">No patients found</p>
              <p className="text-gray-500">Try adjusting your search or filters</p>
            </div>
          )}
        </div>
      )}

      {/* Patient Detail Modal */}
      {selectedPatientId && (
        <PatientDetailModal
          patientId={selectedPatientId}
          onClose={() => setSelectedPatientId(null)}
        />
      )}
    </div>
  )
}
