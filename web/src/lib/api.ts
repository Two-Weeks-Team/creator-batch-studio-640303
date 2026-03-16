export interface BatchResult {
  hooks: { platform: string; text: string }[];
  shot_list: string[];
  repurpose_lanes: { platform: string; duration: string; hook: string }[];
  publish_queue: string[];
}

export async function generateBatch(
  query: string,
  platforms: string[]
): Promise<BatchResult> {
  const response = await fetch('/api/plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, preferences: { platforms } })
  });
  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || 'Failed to generate batch');
  }
  return response.json();
}

export async function fetchInsights(selection: string, context: any) {
  const response = await fetch('/api/insights', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ selection, context })
  });
  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || 'Failed to fetch insights');
  }
  return response.json();
}
