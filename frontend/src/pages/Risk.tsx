import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { apiGet } from '../api'
import { resolveRunId } from '../utils'

interface Props {
  onToast: (type: 'success' | 'error', message: string) => void
}

export default function RiskPage({ onToast }: Props) {
  const { runId } = useParams()
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    const resolved = resolveRunId(runId)
    if (!resolved) return
    apiGet(`/run/${resolved}`)
      .then(setData)
      .catch((err) => onToast('error', err.message || 'Failed to load risk'))
  }, [runId])

  if (!data) return <div>Loading...</div>
  const risk = data.results.risk

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Urgency Score</h2>
        <p className="text-2xl">{risk.urgency_score.toFixed(1)} / 100</p>
        <p className="text-sm text-slate-500">Category: {risk.category}</p>
      </div>

      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h3 className="font-semibold mb-2">Breakdown</h3>
        <ul className="list-disc pl-5 text-sm">
          {risk.breakdown.map((item: string, idx: number) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </div>

      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h3 className="font-semibold mb-2">Disclaimer</h3>
        <p className="text-sm">
          The urgency score is an educational proxy based on signal features and quality. It does not
          provide medical diagnosis or urgency classification.
        </p>
      </div>
    </div>
  )
}
