import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { deleteHistory, fetchHistory } from '../api/client';
import ConfirmModal from '../components/ConfirmModal';

interface HistoryEntry {
  request_id: string;
  created_at: string;
  patient_id: string;
  visit_label?: string | null;
  auscultation_site: string;
  summary: {
    murmur_label: string;
    concern_level: string;
    quality_score: number;
  };
}

export default function HistoryPage() {
  const [entries, setEntries] = useState<HistoryEntry[]>([]);
  const [patientId, setPatientId] = useState('');
  const [loading, setLoading] = useState(false);
  const [deleteId, setDeleteId] = useState<string | null>(null);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const response = await fetchHistory(patientId || undefined);
      setEntries(response.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleDelete = async () => {
    if (!deleteId) return;
    await deleteHistory(deleteId);
    setDeleteId(null);
    loadHistory();
  };

  return (
    <div className="space-y-6">
      <div className="neo-card">
        <h2 className="text-2xl font-semibold text-emerald-200">History Archive</h2>
        <p className="text-slate-300 mt-2">Search by patient ID to filter entries.</p>
        <div className="flex flex-wrap gap-3 mt-4">
          <input
            value={patientId}
            onChange={(event) => setPatientId(event.target.value)}
            className="rounded-lg bg-slate-800 border border-slate-700 p-2"
            placeholder="Patient ID"
          />
          <button className="neo-button" onClick={loadHistory}>
            {loading ? 'Loading...' : 'Search'}
          </button>
        </div>
      </div>

      <div className="neo-card overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-400">
              <th className="py-2">Created</th>
              <th>Patient</th>
              <th>Visit</th>
              <th>Murmur</th>
              <th>Concern</th>
              <th>Quality</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {entries.map((entry) => (
              <tr key={entry.request_id} className="border-t border-slate-800">
                <td className="py-2">{new Date(entry.created_at).toLocaleString()}</td>
                <td>{entry.patient_id}</td>
                <td>{entry.visit_label || '—'}</td>
                <td>{entry.summary.murmur_label}</td>
                <td>{entry.summary.concern_level}</td>
                <td>{entry.summary.quality_score}</td>
                <td className="text-right space-x-2">
                  <Link
                    to={`/history/${entry.request_id}`}
                    className="text-emerald-300 hover:text-emerald-200"
                  >
                    View
                  </Link>
                  <button
                    className="text-rose-400 hover:text-rose-300"
                    onClick={() => setDeleteId(entry.request_id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
            {entries.length === 0 && (
              <tr>
                <td colSpan={7} className="py-6 text-center text-slate-400">
                  No history entries yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <ConfirmModal
        open={!!deleteId}
        title="Delete Entry"
        description="This will permanently remove the selected analysis from the local archive."
        onCancel={() => setDeleteId(null)}
        onConfirm={handleDelete}
      />
    </div>
  );
}
