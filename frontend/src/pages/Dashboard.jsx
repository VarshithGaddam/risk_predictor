import { useState, useEffect } from 'react'
import { dashboardAPI } from '../services/api'
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, Legend
} from 'recharts'
import axios from 'axios'

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#14B8A6', '#F97316']

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null)
  const [distribution, setDistribution] = useState([])
  const [ageDistribution, setAgeDistribution] = useState([])
  const [diagnosisBreakdown, setDiagnosisBreakdown] = useState([])
  const [admissionsTimeline, setAdmissionsTimeline] = useState([])
  const [riskByAge, setRiskByAge] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchData = async () => {
    try {
      const [metricsRes, distRes, ageRes, diagRes, timelineRes, riskAgeRes] = await Promise.all([
        dashboardAPI.getMetrics(),
        dashboardAPI.getRiskDistribution(),
        axios.get('http://localhost:5000/api/dashboard/age-distribution'),
        axios.get('http://localhost:5000/api/dashboard/diagnosis-breakdown'),
        axios.get('http://localhost:5000/api/dashboard/admissions-timeline'),
        axios.get('http://localhost:5000/api/dashboard/risk-by-age')
      ])
      setMetrics(metricsRes.data)
      setDistribution(distRes.data)
      setAgeDistribution(ageRes.data)
      setDiagnosisBreakdown(diagRes.data)
      setAdmissionsTimeline(timelineRes.data)
      setRiskByAge(riskAgeRes.data)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-gray-600">Loading dashboard...</div>
      </div>
    )
  }

  const getMetricColor = (label) => {
    if (label === 'High Risk Patients') return 'bg-danger'
    if (label === 'Readmission Rate') return 'bg-warning'
    return 'bg-primary'
  }

  const metricCards = [
    { 
      label: 'Total Patients', 
      value: metrics?.totalPatients || 0, 
      unit: '',
      icon: '👥',
      color: 'from-blue-500 to-blue-600',
      textColor: 'text-blue-600'
    },
    { 
      label: 'High Risk Patients', 
      value: metrics?.highRiskCount || 0, 
      unit: '',
      icon: '⚠️',
      color: 'from-red-500 to-red-600',
      textColor: 'text-red-600'
    },
    { 
      label: 'Avg Length of Stay', 
      value: metrics?.avgLengthOfStay || 0, 
      unit: ' days',
      icon: '🏥',
      color: 'from-green-500 to-green-600',
      textColor: 'text-green-600'
    },
    { 
      label: 'Readmission Rate', 
      value: metrics?.readmissionRate || 0, 
      unit: '%',
      icon: '📊',
      color: 'from-yellow-500 to-yellow-600',
      textColor: 'text-yellow-600'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl shadow-lg p-8 text-white">
        <h2 className="text-4xl font-bold mb-2">Healthcare Analytics Dashboard</h2>
        <p className="text-blue-100">Real-time insights powered by Machine Learning</p>
      </div>
      
      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metricCards.map((metric, index) => (
          <div 
            key={index} 
            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`text-4xl`}>{metric.icon}</div>
              <div className={`px-3 py-1 rounded-full bg-gradient-to-r ${metric.color} text-white text-xs font-semibold`}>
                LIVE
              </div>
            </div>
            <div className="text-sm text-gray-600 font-medium mb-2">
              {metric.label}
            </div>
            <div className={`text-4xl font-bold ${metric.textColor}`}>
              {metric.value}{metric.unit}
            </div>
          </div>
        ))}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Distribution Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center mb-4">
            <span className="text-2xl mr-3">📊</span>
            <h3 className="text-xl font-bold text-gray-800">Risk Score Distribution</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={distribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="riskRange" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Age Distribution Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center mb-4">
            <span className="text-2xl mr-3">👥</span>
            <h3 className="text-xl font-bold text-gray-800">Age Distribution</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ageDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ageRange" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#10B981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Diagnosis Breakdown Pie Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center mb-4">
            <span className="text-2xl mr-3">🏥</span>
            <h3 className="text-xl font-bold text-gray-800">Top Diagnoses</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={diagnosisBreakdown}
                dataKey="count"
                nameKey="diagnosis"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => `${entry.count}`}
              >
                {diagnosisBreakdown.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
            {diagnosisBreakdown.slice(0, 6).map((item, index) => (
              <div key={index} className="flex items-center">
                <div 
                  className="w-3 h-3 rounded-full mr-2" 
                  style={{ backgroundColor: COLORS[index % COLORS.length] }}
                />
                <span className="truncate">{item.diagnosis.substring(0, 20)}...</span>
              </div>
            ))}
          </div>
        </div>

        {/* Risk by Age Group */}
        <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center mb-4">
            <span className="text-2xl mr-3">📈</span>
            <h3 className="text-xl font-bold text-gray-800">Average Risk by Age</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={riskByAge}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ageGroup" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="avgRisk" 
                stroke="#EF4444" 
                strokeWidth={3}
                name="Avg Risk Score"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Admissions Timeline */}
      <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
        <div className="flex items-center mb-4">
          <span className="text-2xl mr-3">📅</span>
          <h3 className="text-xl font-bold text-gray-800">Admissions Timeline (Last 30 Days)</h3>
        </div>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={admissionsTimeline}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tickFormatter={(date) => new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            />
            <YAxis />
            <Tooltip 
              labelFormatter={(date) => new Date(date).toLocaleDateString()}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="admissions" 
              stroke="#8B5CF6" 
              strokeWidth={2}
              name="Daily Admissions"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
