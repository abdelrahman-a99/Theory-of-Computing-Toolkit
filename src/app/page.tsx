'use client';

import { useState, useEffect } from 'react';
import RegexInput from '../components/RegexInput';
import NFAResult from '../components/NFAResult';

type NFA = {
  start_state: string;
  accept_state: string;
  transitions: Record<string, Record<string, string[]>>;
  image_url: string;
};

export default function Home() {
  const [regex, setRegex] = useState('');
  const [nfa, setNfa] = useState<NFA | null>(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    if (nfa && nfa.image_url) {
      setImageUrl(nfa.image_url);
    }
  }, [nfa]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/api/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ regex }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to convert regex');
      }

      const data = await response.json();
      setNfa(data);
    }

    catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      setNfa(null);
    }

    finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Regex to NFA Converter</h1>

        <form onSubmit={handleSubmit} className="mb-6">
          <RegexInput regex={regex} setRegex={setRegex} isLoading={isLoading} />
        </form>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700">
            <p>{error}</p>
          </div>
        )}

        {nfa && <NFAResult nfa={nfa} />}
      </div>
    </main>
  );
}
