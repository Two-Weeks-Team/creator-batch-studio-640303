"use client";

export default function StatsStrip() {
  const stats = [
    { label: 'Generation Speed', value: '<5 s' },
    { label: 'Platforms Supported', value: 'TikTok, Reels, Shorts' },
    { label: 'Data Privacy', value: 'Client‑side only' }
  ];
  return (
    <div className="flex justify-center gap-6 mb-6">
      {stats.map((s, i) => (
        <div key={i} className="text-center">
          <div className="text-sm text-muted">{s.label}</div>
          <div className="text-lg font-medium text-primary">{s.value}</div>
        </div>
      ))}
    </div>
  );
}