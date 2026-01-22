export default function PrivacyPage() {
  return (
    <div className="space-y-6">
      <div className="neo-card">
        <h2 className="text-2xl font-semibold text-emerald-200">Privacy</h2>
        <p className="text-slate-300 mt-2">
          This demo runs locally and stores analysis results in a local SQLite database. Do not upload
          personal health information or sensitive identifiers.
        </p>
      </div>
      <div className="neo-card border-rose-500/40">
        <h3 className="text-xl font-semibold text-rose-300">Safety Disclaimer</h3>
        <p className="text-slate-300 mt-2">
          Screening/educational demo only. It does not provide diagnosis, treatment, or clinical advice.
        </p>
      </div>
    </div>
  );
}
