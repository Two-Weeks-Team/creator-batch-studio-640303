"use client";

type Props = {
  status: 'idle' | 'loading' | 'error';
  errorMsg: string;
};

export default function StatePanel({ status, errorMsg }: Props) {
  if (status === 'loading') {
    return (
      <div className="flex items-center justify-center py-4 text-primary">
        <svg className="animate-spin h-6 w-6 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
        </svg>
        Generating your batch…
      </div>
    );
  }
  if (status === 'error') {
    return (
      <div className="bg-warning text-white p-3 rounded-md mt-4">
        <p className="font-medium">Oops! Something went wrong.</p>
        <p>{errorMsg}</p>
      </div>
    );
  }
  return null;
}