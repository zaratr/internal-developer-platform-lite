import { useState, useEffect } from 'react'
import './App.css'
import ServiceList from './components/ServiceList'
import CreateServiceModal from './components/CreateServiceModal'

const API_BASE = 'http://localhost:8000/api/v1'

export interface Service {
  name: string
  path: string
  template?: string
  status: string
}

function App() {
  const [services, setServices] = useState<Service[]>([])
  const [showModal, setShowModal] = useState(false)
  const [loading, setLoading] = useState(true)

  const fetchServices = async () => {
    try {
      const response = await fetch(`${API_BASE}/services/`)
      const data = await response.json()
      setServices(data)
    } catch (error) {
      console.error('Failed to fetch services:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchServices()
  }, [])

  const handleServiceCreated = () => {
    setShowModal(false)
    fetchServices()
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1 className="logo">IDP-Lite Control Plane</h1>
          <button className="btn-primary" onClick={() => setShowModal(true)}>
            + Create Service
          </button>
        </div>
      </header>

      <main className="main-content">
        {loading ? (
          <div className="loading">Loading services...</div>
        ) : (
          <ServiceList services={services} />
        )}
      </main>

      {showModal && (
        <CreateServiceModal
          onClose={() => setShowModal(false)}
          onSuccess={handleServiceCreated}
        />
      )}
    </div>
  )
}

export default App
