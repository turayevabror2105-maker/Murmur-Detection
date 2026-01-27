import { useRef, useState } from 'react'
import { uploadFile, apiPost } from '../api'

interface UploadPageProps {
  onToast: (type: 'success' | 'error', message: string) => void
  onRunComplete: (runId: number) => void
}

export default function UploadPage({ onToast, onRunComplete }: UploadPageProps) {
  const [file, setFile] = useState<File | null>(null)
  const [meta, setMeta] = useState<{ duration: number; sampleRate: number; channels: number } | null>(null)
  const [runId, setRunId] = useState<number | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const canvasRef = useRef<HTMLCanvasElement | null>(null)

  const handleFile = async (selected: File) => {
    if (!selected.name.endsWith('.wav')) {
      onToast('error', 'Only .wav files are supported.')
      return
    }
    setFile(selected)
    try {
      const arrayBuffer = await selected.arrayBuffer()
      const audioContext = new AudioContext()
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer.slice(0))
      setMeta({
        duration: audioBuffer.duration,
        sampleRate: audioBuffer.sampleRate,
        channels: audioBuffer.numberOfChannels
      })
      drawWaveform(audioBuffer.getChannelData(0))
    } catch {
      onToast('error', 'Failed to decode audio file.')
    }
  }

  const drawWaveform = (data: Float32Array) => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.strokeStyle = '#2563eb'
    ctx.beginPath()
    const step = Math.ceil(data.length / canvas.width)
    for (let i = 0; i < canvas.width; i++) {
      const start = i * step
      const slice = data.slice(start, start + step)
      const min = Math.min(...slice)
      const max = Math.max(...slice)
      ctx.moveTo(i, (1 + min) * 0.5 * canvas.height)
      ctx.lineTo(i, (1 + max) * 0.5 * canvas.height)
    }
    ctx.stroke()
  }

  const upload = async () => {
    if (!file) {
      onToast('error', 'Select a WAV file first.')
      return
    }
    try {
      const response = await uploadFile(file)
      setRunId(response.run_id)
      onToast('success', 'File uploaded successfully.')
    } catch (err: any) {
      onToast('error', err.message || 'Upload failed.')
    }
  }

  const run = async (mode: 'real' | 'demo') => {
    if (!runId) {
      onToast('error', 'Upload a file before running analysis.')
      return
    }
    setIsRunning(true)
    try {
      const data = await apiPost(`/run/${runId}`, { mode })
      onToast('success', 'Analysis complete.')
      onRunComplete(data.run_id)
    } catch (err: any) {
      onToast('error', err.message || 'Run failed.')
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Upload PCG (.wav)</h2>
        <div
          className="border-2 border-dashed rounded p-6 text-center cursor-pointer"
          onClick={() => document.getElementById('fileInput')?.click()}
          onDrop={(e) => {
            e.preventDefault()
            const dropped = e.dataTransfer.files[0]
            if (dropped) handleFile(dropped)
          }}
          onDragOver={(e) => e.preventDefault()}
        >
          <p className="text-sm text-slate-500">Drag & drop a WAV file here</p>
          <button id="btn_upload_file" className="mt-3 px-3 py-1 border rounded" onClick={upload}>
            Upload
          </button>
          <input
            id="fileInput"
            type="file"
            accept=".wav"
            className="hidden"
            onChange={(e) => {
              const selected = e.target.files?.[0]
              if (selected) handleFile(selected)
            }}
          />
        </div>
      </div>

      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Audio Preview</h2>
        <canvas ref={canvasRef} width={800} height={120} className="w-full border rounded" />
        <div className="mt-2 text-sm">
          <p>Duration: {meta ? meta.duration.toFixed(2) : '--'} s</p>
          <p>Sample rate: {meta ? meta.sampleRate : '--'} Hz</p>
          <p>Channels: {meta ? meta.channels : '--'}</p>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-800 p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Run</h2>
        <div className="flex gap-3">
          <button
            id="btn_run_analysis"
            className="px-4 py-2 bg-blue-600 text-white rounded"
            onClick={() => run('real')}
            disabled={isRunning}
          >
            Run Analysis
          </button>
          <button
            id="btn_run_demo"
            className="px-4 py-2 border rounded"
            onClick={() => run('demo')}
            disabled={isRunning}
          >
            Try Demo File
          </button>
        </div>
        {isRunning && (
          <div className="mt-3">
            <div className="h-2 bg-slate-200 rounded">
              <div className="h-2 bg-blue-500 rounded animate-pulse w-1/2" />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
