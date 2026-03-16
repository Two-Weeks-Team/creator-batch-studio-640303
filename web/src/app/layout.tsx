import '@/app/globals.css';

export const metadata = {
  title: 'Creator Batch Studio',
  description: 'Batch‑plan, shoot, and publish short‑form videos in seconds.'
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full bg-background text-foreground">
      <body className="h-full flex flex-col antialiased">
        {children}
      </body>
    </html>
  );
}