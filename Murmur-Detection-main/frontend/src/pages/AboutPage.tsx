export default function AboutPage() {
  return (
    <div className="space-y-6">
      <div className="neo-card">
        <h2 className="text-2xl font-semibold text-emerald-200">About & Method</h2>
        <p className="text-slate-300 mt-3">
          This project is a screening/educational demo that analyzes heart sound WAV recordings. It does
          not provide diagnosis, treatment, or prognostic information.
        </p>
      </div>

      <div className="neo-card">
        <h3 className="text-xl font-semibold text-emerald-200">Baseline Timing</h3>
        <p className="text-slate-300 mt-2">
          The baseline timing classifier only distinguishes systolic vs diastolic phases (S1–S2 vs S2–next
          S1). It does not perform precise timestamp localization.
        </p>
      </div>

      <div className="neo-card">
        <h3 className="text-xl font-semibold text-emerald-200">Gap 1: Confidence Calibration</h3>
        <p className="text-slate-300 mt-2">
          The model applies temperature scaling to adjust probabilities so they better match real-world
          accuracy over many samples.
        </p>
      </div>

      <div className="neo-card">
        <h3 className="text-xl font-semibold text-emerald-200">Gap 2: Recording Quality Gate</h3>
        <p className="text-slate-300 mt-2">
          We compute SNR, clipping, and silence percentages to produce a quality score and determine
          whether a retake is recommended.
        </p>
      </div>

      <div className="neo-card">
        <h3 className="text-xl font-semibold text-emerald-200">Gap 3: Uncertainty Estimation</h3>
        <p className="text-slate-300 mt-2">
          MC-dropout runs multiple forward passes to estimate uncertainty and adjust screening concern
          levels.
        </p>
      </div>

      <div className="neo-card">
        <h3 className="text-xl font-semibold text-emerald-200">Gap 4: Explainability</h3>
        <p className="text-slate-300 mt-2">
          Gradient-based saliency highlights time-frequency regions that influence the screening output. It
          is descriptive only and not clinical guidance.
        </p>
      </div>

      <div className="neo-card">
        <h3 className="text-xl font-semibold text-emerald-200">Datasets & Licenses</h3>
        <p className="text-slate-300 mt-2">
          Demo WAV files are synthetic tones generated locally for this project. For optional exploration,
          the README lists open datasets such as PhysioNet/CinC 2016 with their licensing terms.
        </p>
      </div>

      <div className="neo-card border-rose-500/40">
        <h3 className="text-xl font-semibold text-rose-300">Safety Disclaimer</h3>
        <p className="text-slate-300 mt-2">
          This tool is for screening and educational use only. It does not diagnose, treat, or predict
          disease. Always consult a qualified clinician.
        </p>
      </div>
    </div>
  );
}
