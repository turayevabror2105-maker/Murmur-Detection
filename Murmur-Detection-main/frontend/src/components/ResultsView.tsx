import StatCard from './StatCard';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

export interface PredictResponse {
  request_id: string;
  created_at: string;
  input: {
    filename: string;
    patient_id: string;
    visit_label?: string | null;
    auscultation_site: string;
    duration_s: number;
    sample_rate: number;
  };
  murmur: {
    label: string;
    raw_probability: number;
    calibrated_probability: number;
    uncertainty_score: number;
  };
  timing: {
    label: string;
    systolic_probability: number;
    diastolic_probability: number;
  };
  quality: {
    quality_score_0_100: number;
    snr_db: number;
    clipping_pct: number;
    silence_pct: number;
    retake_recommended: boolean;
    retake_reasons: string[];
  };
  risk: {
    screening_concern_level: string;
    rationale: string;
  };
  safe_advice: string[];
  segments: Array<{ t0: number; t1: number; murmur_prob: number }>;
  artifacts: {
    waveform_png_base64: string;
    spectrogram_png_base64: string;
    timeline_png_base64: string;
    explainability_png_base64: string;
  };
}

interface ResultsViewProps {
  data: PredictResponse;
  showExport?: boolean;
}

export default function ResultsView({ data, showExport = true }: ResultsViewProps) {
  const timelineData = {
    labels: data.segments.map((seg) => ((seg.t0 + seg.t1) / 2).toFixed(1)),
    datasets: [
      {
        label: 'Murmur probability',
        data: data.segments.map((seg) => seg.murmur_prob),
        borderColor: '#f43f5e',
        backgroundColor: 'rgba(244,63,94,0.3)'
      }
    ]
  };

  const timelineOptions = {
    scales: {
      y: { min: 0, max: 1 }
    }
  };

  const handleDownloadJson = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `murmur-screening-${data.request_id}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    printWindow.document.write(`
      <html>
        <head>
          <title>Screening Summary</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 24px; }
            h1 { color: #111827; }
            .section { margin-bottom: 16px; }
            .badge { display: inline-block; padding: 4px 8px; background: #e2e8f0; border-radius: 6px; }
          </style>
        </head>
        <body>
          <h1>Murmur Screening Summary (Demo)</h1>
          <p class="section"><strong>Disclaimer:</strong> Screening/educational demo only. Not diagnosis.</p>
          <div class="section"><strong>Patient:</strong> ${data.input.patient_id}</div>
          <div class="section"><strong>Visit:</strong> ${data.input.visit_label || 'N/A'}</div>
          <div class="section"><strong>Auscultation Site:</strong> ${data.input.auscultation_site}</div>
          <div class="section"><strong>Murmur Label:</strong> <span class="badge">${data.murmur.label}</span></div>
          <div class="section"><strong>Calibrated Probability:</strong> ${(data.murmur.calibrated_probability * 100).toFixed(1)}%</div>
          <div class="section"><strong>Timing:</strong> ${data.timing.label}</div>
          <div class="section"><strong>Quality Score:</strong> ${data.quality.quality_score_0_100}/100</div>
          <div class="section"><strong>Screening Concern:</strong> ${data.risk.screening_concern_level}</div>
          <div class="section"><strong>Rationale:</strong> ${data.risk.rationale}</div>
          <div class="section"><strong>Advice:</strong><ul>${data.safe_advice.map((item) => `<li>${item}</li>`).join('')}</ul></div>
        </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
  };

  return (
    <div className="space-y-8">
      <div className="neo-card">
        <h2 className="text-2xl font-semibold text-emerald-200">Results Summary</h2>
        <p className="text-sm text-slate-300 mt-2">Request ID: {data.request_id}</p>
        <p className="text-sm text-slate-300">Recorded at: {new Date(data.created_at).toLocaleString()}</p>
        <p className="text-sm text-slate-300">Auscultation site: {data.input.auscultation_site}</p>
        <p className="text-sm text-slate-300">Patient ID: {data.input.patient_id}</p>
        <p className="text-sm text-slate-300">Visit label: {data.input.visit_label || 'N/A'}</p>
        <p className="text-sm text-slate-400 mt-2">
          Disclaimer: This screening demo is educational only and does not provide diagnosis or treatment.
        </p>
        {showExport && (
          <div className="flex flex-wrap gap-3 mt-4">
            <button className="neo-button" onClick={handleDownloadJson}>
              Download JSON
            </button>
            <button className="neo-button" onClick={handlePrint}>
              Print Summary
            </button>
          </div>
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <StatCard title="Murmur Screen">
          <p>Label: <span className="font-semibold">{data.murmur.label}</span></p>
          <p>Raw Probability: {(data.murmur.raw_probability * 100).toFixed(1)}%</p>
          <p>Calibrated Probability: {(data.murmur.calibrated_probability * 100).toFixed(1)}%</p>
          <p>Uncertainty Score: {data.murmur.uncertainty_score.toFixed(2)}</p>
        </StatCard>
        <StatCard title="Timing (S1–S2 vs S2–next S1)">
          <p>Label: <span className="font-semibold">{data.timing.label}</span></p>
          <p>Systolic Probability: {(data.timing.systolic_probability * 100).toFixed(1)}%</p>
          <p>Diastolic Probability: {(data.timing.diastolic_probability * 100).toFixed(1)}%</p>
        </StatCard>
        <StatCard title="Recording Quality">
          <p>Quality Score: {data.quality.quality_score_0_100}/100</p>
          <p>SNR: {data.quality.snr_db.toFixed(1)} dB</p>
          <p>Clipping: {data.quality.clipping_pct.toFixed(1)}%</p>
          <p>Silence: {data.quality.silence_pct.toFixed(1)}%</p>
          <p>Duration: {data.input.duration_s.toFixed(2)} s</p>
          <p>Sample Rate: {data.input.sample_rate} Hz</p>
          {data.quality.retake_recommended && (
            <div className="mt-3 text-rose-300">
              <p className="font-semibold">Retake recommended</p>
              <ul className="list-disc list-inside">
                {data.quality.retake_reasons.map((reason) => (
                  <li key={reason}>{reason}</li>
                ))}
              </ul>
            </div>
          )}
        </StatCard>
        <StatCard title="Screening Concern">
          <p>Level: <span className="font-semibold">{data.risk.screening_concern_level}</span></p>
          <p className="text-slate-300">{data.risk.rationale}</p>
        </StatCard>
        <StatCard title="Safe Advice">
          <ul className="list-disc list-inside">
            {data.safe_advice.map((advice) => (
              <li key={advice}>{advice}</li>
            ))}
          </ul>
        </StatCard>
      </div>

      <div className="neo-card">
        <h3 className="text-xl font-semibold text-emerald-200 mb-4">Graphs & Visualizations</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-sm text-slate-300 mb-2">Waveform</h4>
            <img
              src={`data:image/png;base64,${data.artifacts.waveform_png_base64}`}
              alt="Waveform"
              className="rounded-lg border border-slate-700"
            />
          </div>
          <div>
            <h4 className="text-sm text-slate-300 mb-2">Mel-Spectrogram</h4>
            <img
              src={`data:image/png;base64,${data.artifacts.spectrogram_png_base64}`}
              alt="Spectrogram"
              className="rounded-lg border border-slate-700"
            />
          </div>
          <div>
            <h4 className="text-sm text-slate-300 mb-2">Murmur Probability Timeline</h4>
            <div className="bg-slate-900 p-4 rounded-lg border border-slate-700">
              <Line data={timelineData} options={timelineOptions} />
            </div>
            <img
              src={`data:image/png;base64,${data.artifacts.timeline_png_base64}`}
              alt="Timeline"
              className="rounded-lg border border-slate-700 mt-4"
            />
          </div>
          <div>
            <h4 className="text-sm text-slate-300 mb-2">Explainability Heatmap Overlay</h4>
            <img
              src={`data:image/png;base64,${data.artifacts.explainability_png_base64}`}
              alt="Explainability"
              className="rounded-lg border border-slate-700"
            />
            <div className="mt-4">
              <h4 className="text-sm text-slate-300 mb-2">Quality Meter</h4>
              <div className="w-full bg-slate-800 rounded-full h-3">
                <div
                  className="h-3 rounded-full bg-emerald-400"
                  style={{ width: `${data.quality.quality_score_0_100}%` }}
                ></div>
              </div>
              <p className="text-xs text-slate-400 mt-1">Quality score {data.quality.quality_score_0_100}/100</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
