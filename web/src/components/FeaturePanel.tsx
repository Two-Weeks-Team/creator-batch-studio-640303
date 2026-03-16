"use client";

export default function FeaturePanel() {
  const features = [
    'AI‑generated hooks per platform',
    'Drag‑and‑drop shot list with live duration sync',
    'One‑click export to markdown/CSV/PDF',
    'IndexedDB persistence with versioning',
    'Zero uploads – everything stays client‑side'
  ];
  return (
    <section className="card mb-8">
      <h2 className="text-2xl font-bold text-primary mb-4">Why Creators Love It</h2>
      <ul className="list-disc list-inside space-y-1 text-foreground">
        {features.map((f, i) => (
          <li key={i}>{f}</li>
        ))}
      </ul>
    </section>
  );
}