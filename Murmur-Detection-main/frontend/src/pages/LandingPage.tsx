import { Link } from 'react-router-dom';

export default function LandingPage() {
  return (
    <div className="space-y-10">
      <section className="neo-card">
        <p className="text-sm uppercase tracking-widest text-emerald-300">Screening & Education Demo</p>
        <h1 className="text-4xl font-bold text-white mt-2">
          Heart Sound Murmur Screening Demo
        </h1>
        <p className="text-slate-200 mt-4 max-w-2xl">
          Upload a WAV recording of a heart sound, select the auscultation site, and receive a
          non-diagnostic screening summary with quality checks, uncertainty, and visual explanations.
        </p>
        <div className="mt-6">
          <Link to="/upload" className="neo-button">
            Start Screening
          </Link>
        </div>
      </section>

      <section className="neo-card border-rose-500/40">
        <h2 className="text-2xl font-semibold text-rose-300">Important Disclaimer</h2>
        <p className="text-slate-200 mt-3">
          This app is for screening and educational purposes only. It does not provide a diagnosis,
          treatment, or medical advice, and should never be used to make clinical decisions.
        </p>
      </section>
    </div>
  );
}
