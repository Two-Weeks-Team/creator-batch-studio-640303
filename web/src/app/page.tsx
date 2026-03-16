"use client";

import { useState } from "react";
import Hero from '@/components/Hero';
import WorkspacePanel from '@/components/WorkspacePanel';
import InsightPanel from '@/components/InsightPanel';
import StatePanel from '@/components/StatePanel';
import FeaturePanel from '@/components/FeaturePanel';
import CollectionPanel from '@/components/CollectionPanel';
import StatsStrip from '@/components/StatsStrip';
import ReferenceShelf from '@/components/ReferenceShelf';
import { generateBatch } from '@/lib/api';

type Hook = { platform: string; text: string };
type Lane = { platform: string; duration: string; hook: string };

interface BatchResult {
  hooks: Hook[];
  shot_list: string[];
  repurpose_lanes: Lane[];
  publish_queue: string[];
}

export default function HomePage() {
  const [batch, setBatch] = useState<BatchResult | null>(null);
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState<string>('');

  const handleGenerate = async (query: string, platforms: string[]) => {
    setStatus('loading');
    setErrorMsg('');
    try {
      const data = await generateBatch(query, platforms);
      setBatch(data);
      setStatus('idle');
    } catch (e: any) {
      setErrorMsg(e.message || 'Unexpected error');
      setStatus('error');
    }
  };

  return (
    <main className="flex-1 flex flex-col gap-8 p-6 md:p-12 max-w-7xl mx-auto">
      <Hero />
      <StatsStrip />
      <WorkspacePanel onGenerate={handleGenerate} />
      <StatePanel status={status} errorMsg={errorMsg} />
      {batch && <InsightPanel batch={batch} />}
      <FeaturePanel />
      <CollectionPanel />
      <ReferenceShelf />
    </main>
  );
}