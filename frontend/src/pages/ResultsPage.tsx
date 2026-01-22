import { useLocation, Link } from 'react-router-dom';
import ResultsView, { PredictResponse } from '../components/ResultsView';

export default function ResultsPage() {
  const location = useLocation();
  const data = location.state as PredictResponse | undefined;

  if (!data) {
    return (
      <div className="neo-card">
        <p className="text-slate-300">No results loaded. Please upload a WAV file first.</p>
        <Link to="/upload" className="neo-button mt-4 inline-block">
          Go to Upload
        </Link>
      </div>
    );
  }

  return <ResultsView data={data} />;
}
