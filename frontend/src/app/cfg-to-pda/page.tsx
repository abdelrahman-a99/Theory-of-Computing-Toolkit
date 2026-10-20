'use client';

import { useState, type FormEvent } from 'react';
import Link from 'next/link';

import GrammarInput from '../../components/GrammarInput';
import PDAResult, {
  type PDAResultData,
} from '../../components/PDAResult';
import StringTester, {
  type StringTestResult,
} from '../../components/StringTester';

const API_URL = 'http://localhost:5000';

const DEFAULT_GRAMMAR = `S
a,b
S -> a S b | ε`;

async function postJson<T>(
  path: string,
  body: Record<string, string>,
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'The request failed.');
  }

  return data as T;
}

export default function CFGToPDAPage() {
  const [grammar, setGrammar] = useState(DEFAULT_GRAMMAR);
  const [result, setResult] = useState<PDAResultData | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const [word, setWord] = useState('aabb');
  const [testResult, setTestResult] =
    useState<StringTestResult | null>(null);
  const [testError, setTestError] = useState('');
  const [testing, setTesting] = useState(false);

  const busy = loading || testing;

  function changeGrammar(value: string) {
    setGrammar(value);
    setResult(null);
    setError('');
    setTestResult(null);
    setTestError('');
  }

  function changeWord(value: string) {
    setWord(value);
    setTestResult(null);
    setTestError('');
  }

  async function convert(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setError('');
    setResult(null);
    setTestResult(null);
    setTestError('');

    try {
      const data = await postJson<PDAResultData>(
        '/api/cfg-to-pda',
        { grammar },
      );

      setResult(data);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'Conversion failed.',
      );
    } finally {
      setLoading(false);
    }
  }

  async function testString(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setTesting(true);
    setTestError('');
    setTestResult(null);

    try {
      const data = await postJson<StringTestResult>(
        '/api/cfg-to-pda/test',
        { grammar, word },
      );

      setTestResult(data);
    } catch (error) {
      setTestError(
        error instanceof Error
          ? error.message
          : 'String testing failed.',
      );
    } finally {
      setTesting(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-12">
      <div className="max-w-5xl mx-auto">
        <Link
          href="/"
          className="text-sm text-indigo-600 hover:underline"
        >
          ← Back to tools
        </Link>

        <header className="mt-6 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-3">
            CFG → PDA Converter
          </h1>

          <p className="text-gray-600">
            Build a pushdown automaton from a context-free grammar.
          </p>
        </header>

        <section className="bg-white rounded-xl border border-gray-200 p-6">
          <form onSubmit={convert}>
            <GrammarInput
              grammar={grammar}
              onChange={changeGrammar}
              disabled={busy}
              isLoading={loading}
            />
          </form>

          {error && (
            <p
              role="alert"
              className="mt-5 rounded-md bg-red-50 p-4 text-sm text-red-700"
            >
              {error}
            </p>
          )}
        </section>

        {result && (
          <section className="mt-6 space-y-6">
            <PDAResult result={result} apiUrl={API_URL} />

            <StringTester
              word={word}
              onChange={changeWord}
              onSubmit={testString}
              disabled={busy}
              isLoading={testing}
              error={testError}
              result={testResult}
            />
          </section>
        )}
      </div>
    </main>
  );
}
