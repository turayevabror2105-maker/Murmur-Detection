import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { apiGet } from '../api'
import { resolveRunId } from '../utils'

interface QualityPageProps {
  onToast: (type: 'success' | 'error', message: string) => void
}

export default function QualityPage({ onToast }: QualityPageProps) {
  const { runId } = useParams()
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    const resolved = resolveRunId(runId)
    if (!resolved) return
    apiGet(`/run/${resolved}`)
      .then(setData)
      .catch((err) => onToast('error', err.message || 'Failed to load quality'))
  }, [runId])

  if (!data) return <div>Loading...</div>
  const quality = data.results.quality

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Quality Gate</h2>
        <span
          className={`px-3 py-1 rounded-full text-white ${quality.pass ? 'bg-emerald-500' : 'bg-rose-500'}`}
        >
          {quality.pass ? 'PASS' : 'FAIL'}
        </span>
      </div>

      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <table className="w-full text-sm">
          <thead>
            <tr>
              <th className="text-left">Metric</th>
              <th className="text-left">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Duration</td><td>{quality.metrics.duration.toFixed(2)}s</td></tr>
            <tr><td>Clipping rate</td><td>{quality.metrics.clipping_rate.toFixed(3)}</td></tr>
            <tr><td>Silence ratio</td><td>{quality.metrics.silence_ratio.toFixed(3)}</td></tr>
            <tr><td>SNR proxy</td><td>{quality.metrics.snr_proxy.toFixed(2)}</td></tr>
            <tr><td>Amplitude range</td><td>{quality.metrics.amplitude_range.toFixed(2)}</td></tr>
          </tbody>
        </table>
      </div>

      {!quality.pass && (
        <details className="bg-white dark:bg-slate-800 p-4 rounded shadow">
          <summary className="cursor-pointer font-semibold">How to re-record better</summary>
          <ul className="list-disc pl-5 mt-2 text-sm">
            <li>Find a quiet room and minimize background noise.</li>
            <li>Place the stethoscope firmly on the chest.</li>
            <li>Hold steady for at least 10 seconds.</li>
          </ul>
        </details>
      )}
    </div>
  )
}
