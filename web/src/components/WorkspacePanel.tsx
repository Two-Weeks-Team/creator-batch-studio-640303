"use client";

import { useState } from "react";
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

type Props = {
  onGenerate: (query: string, platforms: string[]) => void;
};

const AVAILABLE_PLATFORMS = ['TikTok', 'Reels', 'Shorts'];

export default function WorkspacePanel({ onGenerate }: Props) {
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState<string[]>(['TikTok', 'Reels', 'Shorts']);

  const togglePlatform = (platform: string) => {
    setSelected(prev =>
      prev.includes(platform) ? prev.filter(p => p !== platform) : [...prev, platform]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onGenerate(query.trim(), selected);
    }
  };

  return (
    <section className="card mb-8">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="block">
          <span className={`text-sm font-medium ${inter.className}`}>Video Idea</span>
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="e.g., 3‑minute coffee hack"
            className="mt-1 block w-full rounded-md border border-border bg-muted px-3 py-2 focus:outline-none focus:border-primary"
            required
          />
        </label>
        <fieldset className="flex flex-wrap gap-2">
          <legend className="text-sm font-medium mb-1">Platforms</legend>
          {AVAILABLE_PLATFORMS.map(p => (
            <label key={p} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={selected.includes(p)}
                onChange={() => togglePlatform(p)}
                className="form-checkbox h-4 w-4 text-primary border-border rounded"
              />
              <span className="text-sm">{p}</span>
            </label>
          ))}
        </fieldset>
        <button
          type="submit"
          className="self-start bg-primary text-white px-4 py-2 rounded-md hover:bg-primary/90 transition-colors"
        >
          Generate Batch
        </button>
      </form>
    </section>
  );
}