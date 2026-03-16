"use client";

type Hook = { platform: string; text: string };
type Lane = { platform: string; duration: string; hook: string };

type Props = {
  batch: {
    hooks: Hook[];
    shot_list: string[];
    repurpose_lanes: Lane[];
    publish_queue: string[];
  };
};

export default function InsightPanel({ batch }: Props) {
  return (
    <section className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      {/* Hook Cards */}
      <div className="card overflow-auto max-h-96">
        <h2 className="text-xl font-semibold mb-2 text-primary">Hooks</h2>
        <div className="flex flex-col gap-2">
          {batch.hooks.map((h, i) => (
            <div key={i} className="p-2 border border-muted rounded-md bg-card hover:shadow-md transition-shadow">
              <span className="font-medium text-accent">{h.platform}:</span> {h.text}
            </div>
          ))}
        </div>
      </div>
      {/* Shot List Timeline */}
      <div className="card overflow-auto max-h-96">
        <h2 className="text-xl font-semibold mb-2 text-primary">Shot List</h2>
        <ol className="list-decimal list-inside space-y-1">
          {batch.shot_list.map((shot, i) => (
            <li key={i}>{shot}</li>
          ))}
        </ol>
      </div>
      {/* Publish Queue */}
      <div className="card overflow-auto max-h-96">
        <h2 className="text-xl font-semibold mb-2 text-primary">Publish Queue</h2>
        <ul className="list-disc list-inside space-y-1">
          {batch.publish_queue.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
        <button
          className="mt-4 bg-success text-white px-3 py-1 rounded-md hover:bg-success/90 transition-colors"
          onClick={() => {
            const blob = new Blob([JSON.stringify(batch, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${batch.hooks[0].platform}-batch.json`;
            a.click();
            URL.revokeObjectURL(url);
          }}
        >
          Export Checklist
        </button>
      </div>
    </section>
  );
}