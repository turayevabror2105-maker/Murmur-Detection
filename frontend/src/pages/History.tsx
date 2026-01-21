import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiGet } from '../api'

interface Props {
  onToast: (type: 'success' | 'error', message: string) => void
}

export default function HistoryPage({ onToast }: Props) {
  const [rows, setRows] = useState<any[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    apiGet('/history')
      .then(setRows)
      .catch((err) => onToast('error', err.message || 'Failed to load history'))
  }, [])

  return (
    <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
      <h2 className="font-semibold mb-2">History</h2>
      <table className="w-full text-sm">
        <thead>
          <tr>
            <th className="text-left">Run ID</th>
            <th className="text-left">Filename</th>
            <th className="text-left">Timestamp</th>
            <th className="text-left">Label</th>
            <th className="text-left">Triage</th>
            <th className="text-left">Quality</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr
              key={row.run_id}
              className="cursor-pointer hover:bg-slate-100"
              onClick={() => navigate(`/results/${row.run_id}`)}
            >
              <td>{row.run_id}</td>
              <td>{row.filename}</td>
              <td>{new Date(row.timestamp).toLocaleString()}</td>
              <td>{row.label}</td>
              <td>{row.triage}</td>
              <td>{row.quality_pass ? 'PASS' : 'FAIL'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
