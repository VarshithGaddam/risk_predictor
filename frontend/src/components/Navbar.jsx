import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path
  
  const linkClass = (path) => `px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
    isActive(path) 
      ? 'bg-white text-blue-600 shadow-md' 
      : 'text-white hover:bg-white/20'
  }`
  
  return (
    <nav className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="text-3xl">🏥</div>
            <div>
              <h1 className="text-xl font-bold text-white">Healthcare Analytics</h1>
              <p className="text-xs text-blue-100">AI-Powered Risk Prediction</p>
            </div>
          </div>
          
          <div className="flex space-x-2">
            <Link to="/" className={linkClass('/')}>
              📊 Dashboard
            </Link>
            <Link to="/patients" className={linkClass('/patients')}>
              👥 Patients
            </Link>
            <Link to="/analyzer" className={linkClass('/analyzer')}>
              🤖 AI Analyzer
            </Link>
            <Link to="/upload" className={linkClass('/upload')}>
              📁 Upload
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
