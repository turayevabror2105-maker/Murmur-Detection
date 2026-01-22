import React from 'react';

interface StatCardProps {
  title: string;
  children: React.ReactNode;
}

export default function StatCard({ title, children }: StatCardProps) {
  return (
    <div className="neo-card">
      <h3 className="text-lg font-semibold text-emerald-200 mb-3">{title}</h3>
      <div className="text-sm text-slate-200 space-y-2">{children}</div>
    </div>
  );
}
