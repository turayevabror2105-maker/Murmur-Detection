import { useState } from 'react'
import { apiPost } from '../api'

interface Props {
  onToast: (type: 'success' | 'error', message: string) => void
}

export default function AdminPage({ onToast }: Props) {
  const [log, setLog] = useState<string[]>([])
  const [metrics, setMetrics] = useState<any>(null)

  const appendLog = (line: string) => {
    setLog((prev) => [...prev, line])
  }

  const handleTrain = async () => {
    try {
      appendLog('Training baseline...')
      const res = await apiPost('/train')
      appendLog(res.message)
      onToast('success', 'Training complete.')
    } catch (err: any) {
      onToast('error', err.message || 'Training failed.')
    }
  }

  const handleEval = async () => {
    try {
      appendLog('Evaluating model...')
      const res = await apiPost('/evaluate')
      setMetrics(res.metrics)
      appendLog('Evaluation done.')
      onToast('success', 'Evaluation complete.')
    } catch (err: any) {
      onToast('error', err.message || 'Evaluation failed.')
    }
  }

  const handleCalibrationPlot = () => {
    appendLog('Calibration plot generated during training.')
    onToast('success', 'Calibration plot ready.')
  }

  return (
    <div className="space-y-6">
      <div className="flex gap-3">
        <button id="btn_train" className="px-4 py-2 bg-blue-600 text-white rounded" onClick={handleTrain}>
          Train baseline
        </button>
        <button id="btn_eval" className="px-4 py-2 border rounded" onClick={handleEval}>
          Evaluate
        </button>
        <button id="btn_calibration_plot" className="px-4 py-2 border rounded" onClick={handleCalibrationPlot}>
          Generate calibration plot
        </button>
      </div>

      {metrics && (
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
            <h3 className="text-sm text-slate-500">Accuracy</h3>
            <p className="text-xl">{metrics.accuracy.toFixed(2)}</p>
          </div>
          <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
            <h3 className="text-sm text-slate-500">Macro F1</h3>
            <p className="text-xl">{metrics.macro_f1.toFixed(2)}</p>
          </div>
          <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
            <h3 className="text-sm text-slate-500">Confusion Matrix</h3>
            <pre className="text-xs">{JSON.stringify(metrics.confusion_matrix)}</pre>
          </div>
        </div>
      )}

      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h3 className="font-semibold mb-2">Calibration Plot</h3>
        <img src="http://localhost:8000/api/plots/calibration" alt="calibration plot" className="w-full border rounded" />
      </div>

      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h3 className="font-semibold mb-2">Log Console</h3>
        <div className="h-40 overflow-y-auto bg-slate-100 dark:bg-slate-900 p-2 text-xs">
          {log.map((line, idx) => (
            <div key={idx}>{line}</div>
          ))}
        </div>
      </div>
    </div>
  )
}
