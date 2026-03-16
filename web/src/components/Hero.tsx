"use client";

import { Inter } from 'next/font/google';

const interBold = Inter({ weight: ['700'], subsets: ['latin'] });

export default function Hero() {
  return (
    <section className="text-center mb-8">
      <h1 className={`${interBold.className} text-4xl md:text-5xl font-bold text-primary`}>Creator Batch Studio</h1>
      <p className="mt-4 text-lg text-foreground max-w-2xl mx-auto">Batch‑plan, shoot, and publish short‑form videos in seconds with an editorial board that does the heavy lifting.</p>
      <div className="flex justify-center space-x-4 mt-6">
        <span className="inline-flex items-center px-3 py-1 bg-success text-sm rounded-full text-white">Powered by a state‑of‑the‑art LLM</span>
        <span className="inline-flex items-center px-3 py-1 bg-muted text-sm rounded-full text-foreground">Open‑source Transparency</span>
        <span className="inline-flex items-center px-3 py-1 bg-primary text-sm rounded-full text-white">No uploads – all client‑side</span>
      </div>
    </section>
  );
}