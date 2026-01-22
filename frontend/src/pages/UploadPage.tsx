import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { predictMurmur } from '../api/client';

const AUSCULTATION_SITES = ['Aortic', 'Pulmonic', 'Tricuspid', 'Mitral', 'Unknown'];

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [duration, setDuration] = useState<number | null>(null);
  const [patientId, setPatientId] = useState('');
  const [visitLabel, setVisitLabel] = useState('');
  const [site, setSite] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFile = async (selected: File) => {
    if (!selected.name.toLowerCase().endsWith('.wav')) {
      setError('Please upload a WAV file.');
      return;
    }
    setError('');
    setFile(selected);

    try {
      const arrayBuffer = await selected.arrayBuffer();
      const audioCtx = new AudioContext();
      const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer.slice(0));
      setDuration(audioBuffer.duration);
      audioCtx.close();
    } catch {
      setDuration(null);
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      handleFile(event.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Upload a WAV file to continue.');
      return;
    }
    if (!patientId.trim()) {
      setError('Patient ID is required.');
      return;
    }
    if (!site) {
      setError('Select an auscultation site.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('patient_id', patientId.trim());
    formData.append('visit_label', visitLabel.trim());
    formData.append('auscultation_site', site);

    setLoading(true);
    try {
      const response = await predictMurmur(formData);
      navigate('/results', { state: response.data });
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="neo-card">
        <h2 className="text-2xl font-semibold text-emerald-200">Upload Heart Sound</h2>
        <p className="text-slate-300 mt-2">Only WAV files are supported. Please record in a quiet space.</p>

        <div
          onDrop={handleDrop}
          onDragOver={(event) => event.preventDefault()}
          className="mt-6 border-2 border-dashed border-slate-700 rounded-2xl p-8 text-center"
        >
          <p className="text-slate-300">Drag & drop your WAV file here</p>
          <p className="text-slate-500 text-sm mt-1">or</p>
          <label className="neo-button inline-block mt-4 cursor-pointer">
            Browse File
            <input
              type="file"
              className="hidden"
              accept=".wav"
              onChange={(event) => event.target.files && handleFile(event.target.files[0])}
            />
          </label>
          {file && (
            <div className="mt-4 text-sm text-slate-200">
              <p>Selected: {file.name}</p>
              {duration && <p>Detected duration: {duration.toFixed(2)} s</p>}
            </div>
          )}
        </div>

        <div className="grid md:grid-cols-2 gap-4 mt-6">
          <div>
            <label className="text-sm text-slate-300">Patient ID *</label>
            <input
              value={patientId}
              onChange={(event) => setPatientId(event.target.value)}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 p-2"
              placeholder="e.g., P-001"
            />
          </div>
          <div>
            <label className="text-sm text-slate-300">Visit Label (optional)</label>
            <input
              value={visitLabel}
              onChange={(event) => setVisitLabel(event.target.value)}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 p-2"
              placeholder="Baseline or follow-up"
            />
          </div>
        </div>

        <div className="mt-4">
          <label className="text-sm text-slate-300">Auscultation Site *</label>
          <select
            value={site}
            onChange={(event) => setSite(event.target.value)}
            className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 p-2"
          >
            <option value="">Select a site</option>
            {AUSCULTATION_SITES.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        {error && <p className="text-rose-400 mt-4">{error}</p>}

        <button onClick={handleSubmit} className="neo-button mt-6" disabled={loading}>
          {loading ? 'Processing...' : 'Submit for Screening'}
        </button>
      </div>
    </div>
  );
}
