import { useParams } from 'react-router-dom'
import { resolveRunId } from '../utils'

interface Props {
  onToast: (type: 'success' | 'error', message: string) => void
}

export default function ReportsPage({ onToast }: Props) {
  const { runId } = useParams()
  const resolved = resolveRunId(runId)
  if (!resolved) {
    return <div>No run selected.</div>
  }

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Report Preview</h2>
        <iframe
          src={`http://localhost:8000/api/report/${resolved}`}
          title="Report"
          className="w-full h-[600px] border rounded"
        />
      </div>
      <a
        href={`http://localhost:8000/api/report/${resolved}`}
        className="px-4 py-2 bg-blue-600 text-white rounded inline-block"
      >
        Download Report
      </a>
    </div>
  )
}
