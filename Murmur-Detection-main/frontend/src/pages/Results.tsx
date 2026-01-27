import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiGet } from '../api'
import Modal from '../components/Modal'
import { resolveRunId } from '../utils'

interface ResultsPageProps {
  onToast: (type: 'success' | 'error', message: string) => void
}

export default function ResultsPage({ onToast }: ResultsPageProps) {
  const { runId } = useParams()
  const [data, setData] = useState<any>(null)
  const [modalOpen, setModalOpen] = useState(false)

  useEffect(() => {
    const resolved = resolveRunId(runId)
    if (!resolved) return
    apiGet(`/run/${resolved}`)
      .then(setData)
      .catch((err) => onToast('error', err.message || 'Failed to load results'))
  }, [runId])

  if (!data) {
    return <div>Loading...</div>
  }

  const results = data.results

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Summary</h2>
        <p>Predicted label: {results.predicted_label}</p>
        <p>Calibrated confidence: {(results.calibrated_confidence * 100).toFixed(1)}%</p>
        <button id="btn_view_explain" className="mt-3 px-3 py-1 border rounded" onClick={() => setModalOpen(true)}>
          View Explanation
        </button>
      </div>

      <Modal isOpen={modalOpen} title="Explanation" onClose={() => setModalOpen(false)}>
        <h3 className="font-semibold mb-2">Top Features</h3>
        <ul className="list-disc pl-5">
          {results.explanation.top_features.map((f: string) => (
            <li key={f}>{f}</li>
          ))}
        </ul>
        <h3 className="font-semibold mt-4 mb-2">Top Time Segments</h3>
        <ul className="list-disc pl-5">
          {results.explanation.top_segments.map((seg: any, idx: number) => (
            <li key={idx}>
              {seg.start.toFixed(2)}s - {seg.end.toFixed(2)}s (score {seg.score.toFixed(2)})
            </li>
          ))}
        </ul>
      </Modal>

      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Waveform</h2>
        <img
          src={`http://localhost:8000${results.paths.waveform_png_url}`}
          alt="waveform"
          className="w-full border rounded"
        />
      </div>

      <div className="flex gap-3">
        <a
          id="btn_download_report"
          href={`http://localhost:8000${results.paths.report_url}`}
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          Download Report
        </a>
        <Link id="btn_back_upload" to="/" className="px-4 py-2 border rounded">
          Back to Upload
        </Link>
      </div>
    </div>
  )
}
