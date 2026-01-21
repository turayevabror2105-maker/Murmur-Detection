import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { apiGet } from '../api'
import { resolveRunId } from '../utils'

interface Props {
  onToast: (type: 'success' | 'error', message: string) => void
}

export default function TriagePage({ onToast }: Props) {
  const { runId } = useParams()
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    const resolved = resolveRunId(runId)
    if (!resolved) return
    apiGet(`/run/${resolved}`)
      .then(setData)
      .catch((err) => onToast('error', err.message || 'Failed to load triage'))
  }, [runId])

  if (!data) return <div>Loading...</div>
  const triage = data.results.triage

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Triage</h2>
        <p className="text-lg">{triage.level}</p>
        <p className="text-sm text-slate-500">Rule: {triage.rule_fired}</p>
      </div>

      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h3 className="font-semibold mb-2">Rule Table</h3>
        <table className="w-full text-sm">
          <thead>
            <tr><th className="text-left">Condition</th><th className="text-left">Triage</th></tr>
          </thead>
          <tbody>
            <tr><td>Quality gate failed</td><td>Needs re-record</td></tr>
            <tr><td>Confidence &lt; 0.40</td><td>Low</td></tr>
            <tr><td>0.40 ≤ Confidence &lt; 0.70</td><td>Medium</td></tr>
            <tr><td>Confidence ≥ 0.70</td><td>High</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}
