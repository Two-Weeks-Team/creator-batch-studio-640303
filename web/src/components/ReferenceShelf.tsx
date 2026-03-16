"use client";

export default function ReferenceShelf() {
  const sample = {
    batch_name: 'Coffee Hack',
    idea: '3‑minute coffee hack to boost energy',
    hooks: [
      { platform: 'TikTok', text: 'Boost your morning in 3 min – coffee hack!' },
      { platform: 'Reels', text: 'Quick coffee trick for all‑day energy 🌟' },
      { platform: 'Shorts', text: '3‑minute coffee boost – try it now!' }
    ],
    shot_list: [
      'Intro – creator on kitchen counter',
      'Close‑up of coffee beans',
      'Pour water & stir',
      'Taste test reaction',
      'Call‑to‑action overlay'
    ]
  };
  return (
    <section className="card mb-8">
      <h2 className="text-2xl font-bold text-primary mb-3">Live Sample Batch</h2>
      <pre className="bg-muted p-4 rounded-md text-sm overflow-x-auto max-w-full overflow-y-auto max-h-64">
        {JSON.stringify(sample, null, 2)}
      </pre>
    </section>
  );
}