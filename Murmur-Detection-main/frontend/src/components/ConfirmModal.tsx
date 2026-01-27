import React from 'react';

interface ConfirmModalProps {
  open: boolean;
  title: string;
  description: string;
  onCancel: () => void;
  onConfirm: () => void;
}

export default function ConfirmModal({ open, title, description, onCancel, onConfirm }: ConfirmModalProps) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
      <div className="neo-card max-w-md w-full">
        <h3 className="text-lg font-semibold text-emerald-200 mb-2">{title}</h3>
        <p className="text-slate-300 mb-4">{description}</p>
        <div className="flex justify-end gap-3">
          <button className="px-4 py-2 rounded-lg bg-slate-700 text-slate-200" onClick={onCancel}>
            Cancel
          </button>
          <button className="px-4 py-2 rounded-lg bg-rose-500 text-white" onClick={onConfirm}>
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
