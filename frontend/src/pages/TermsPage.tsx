export default function TermsPage() {
  return (
    <div className="space-y-6">
      <div className="neo-card">
        <h2 className="text-2xl font-semibold text-emerald-200">Terms</h2>
        <p className="text-slate-300 mt-2">
          This open-source demo is provided as-is for educational screening use. You are responsible for
          ensuring appropriate consent and privacy when using it.
        </p>
      </div>
      <div className="neo-card border-rose-500/40">
        <h3 className="text-xl font-semibold text-rose-300">Safety Disclaimer</h3>
        <p className="text-slate-300 mt-2">
          This tool does not diagnose or treat disease and should not be used to make medical decisions.
        </p>
      </div>
    </div>
  );
}
