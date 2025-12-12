type Stat = { label: string; value: string | number };

export const StatCards = ({ stats }: { stats: Stat[] }) => (
  <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
    {stats.map((stat) => (
      <div key={stat.label} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <div className="text-xs uppercase tracking-wide text-slate-500">{stat.label}</div>
        <div className="mt-2 text-2xl font-semibold text-slate-900">{stat.value}</div>
      </div>
    ))}
  </div>
);
