import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import PatientList from './pages/PatientList'
import NoteAnalyzer from './pages/NoteAnalyzer'
import DataUpload from './pages/DataUpload'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/patients" element={<PatientList />} />
            <Route path="/analyzer" element={<NoteAnalyzer />} />
            <Route path="/upload" element={<DataUpload />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
