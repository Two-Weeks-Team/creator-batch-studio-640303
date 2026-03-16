"use client";
import { useEffect, useState } from "react";

type Batch = {
  batch_name: string;
  idea: string;
  created_at: string;
};

export default function CollectionPanel() {
  const [saved, setSaved] = useState<Batch[]>([]);

  useEffect(() => {
    // Mock loading from IndexedDB/localStorage for demo purposes
    const mock = [
      { batch_name: 'Coffee Hack', idea: '3‑minute coffee hack', created_at: '2024-09-01' },
      { batch_name: 'Mini Plant Tour', idea: 'Showcase three low‑light houseplants', created_at: '2024-08-28' },
      { batch_name: 'Quick Workout', idea: '5‑minute home workout', created_at: '2024-08-20' }
    ];
    setSaved(mock);
  }, []);

  return (
    <section className="card mb-8">
      <h2 className="text-2xl font-bold text-primary mb-3">Saved Batches</h2>
      {saved.length === 0 ? (
        <p className="text-muted">No saved batches yet.</p>
      ) : (
        <ul className="space-y-2">
          {saved.map((b, i) => (
            <li key={i} className="p-2 border border-muted rounded-md bg-card flex justify-between items-center">
              <div>
                <span className="font-medium text-foreground">{b.batch_name}</span> – {b.idea}
                <br />
                <small className="text-muted">Saved on {b.created_at}</small>
              </div>
              <button className="text-primary hover:underline">Load</button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}