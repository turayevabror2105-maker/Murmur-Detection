import { Routes, Route, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import Navbar from './components/Navbar'
import Toast, { ToastMessage } from './components/Toast'
import Modal from './components/Modal'
import UploadPage from './pages/Upload'
import ResultsPage from './pages/Results'
import QualityPage from './pages/Quality'
import TriagePage from './pages/Triage'
import RiskPage from './pages/Risk'
import ReportsPage from './pages/Reports'
import HistoryPage from './pages/History'
import AdminPage from './pages/Admin'

function App() {
  const [toasts, setToasts] = useState<ToastMessage[]>([])
  const [aboutOpen, setAboutOpen] = useState(false)
  const navigate = useNavigate()

  const addToast = (type: 'success' | 'error', message: string) => {
    const id = `${Date.now()}-${Math.random()}`
    setToasts((prev) => [...prev, { id, type, message }])
    setTimeout(() => dismissToast(id), 4000)
  }

  const dismissToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }

  const toggleTheme = () => {
    document.body.classList.toggle('dark')
  }

  const handleAbout = () => setAboutOpen(true)

  const onRunComplete = (runId: number) => {
    localStorage.setItem('lastRunId', String(runId))
    navigate(`/results/${runId}`)
  }

  return (
    <div>
      <Navbar onToggleTheme={toggleTheme} onAbout={handleAbout} />
      <div className="max-w-6xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<UploadPage onToast={addToast} onRunComplete={onRunComplete} />} />
          <Route path="/results/:runId" element={<ResultsPage onToast={addToast} />} />
          <Route path="/quality/:runId" element={<QualityPage onToast={addToast} />} />
          <Route path="/triage/:runId" element={<TriagePage onToast={addToast} />} />
          <Route path="/risk/:runId" element={<RiskPage onToast={addToast} />} />
          <Route path="/reports/:runId" element={<ReportsPage onToast={addToast} />} />
          <Route path="/history" element={<HistoryPage onToast={addToast} />} />
          <Route path="/admin" element={<AdminPage onToast={addToast} />} />
        </Routes>
      </div>
      <Toast messages={toasts} onDismiss={dismissToast} />
      <Modal isOpen={aboutOpen} title="About" onClose={() => setAboutOpen(false)}>
        <p className="text-sm">
          Murmur Screen provides educational screening support only. It does not provide medical
          diagnosis or replace clinical evaluation.
        </p>
      </Modal>
    </div>
  )
}

export default App
