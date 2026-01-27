import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchHistoryDetail } from '../api/client';
import ResultsView, { PredictResponse } from '../components/ResultsView';

export default function HistoryDetailPage() {
  const { requestId } = useParams();
  const [data, setData] = useState<PredictResponse | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadDetail = async () => {
      if (!requestId) return;
      try {
        const response = await fetchHistoryDetail(requestId);
        setData(response.data);
      } catch {
        setError('Unable to load history entry.');
      }
    };
    loadDetail();
  }, [requestId]);

  if (error) {
    return (
      <div className="neo-card">
        <p className="text-rose-300">{error}</p>
        <Link to="/history" className="neo-button mt-4 inline-block">
          Back to History
        </Link>
      </div>
    );
  }

  if (!data) {
    return <div className="neo-card">Loading...</div>;
  }

  return <ResultsView data={data} showExport={false} />;
}
