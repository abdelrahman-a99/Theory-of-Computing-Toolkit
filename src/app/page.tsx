import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 px-6 py-16">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12">
          <p className="text-sm font-medium text-indigo-600 mb-3">
            Theory of Computing
          </p>

          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Theory Toolkit
          </h1>

          <p className="text-gray-600 leading-relaxed">
            Convert regular expressions and context-free grammars
            into automata, inspect their transitions, and explore
            their behavior.
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2">
          <Link
            href="/regex-to-nfa"
            className="block rounded-xl border border-gray-200 bg-white p-8 shadow-sm transition hover:border-indigo-400 hover:shadow-md"
          >
            <span className="text-sm font-medium text-indigo-600">
              Project 01
            </span>

            <h2 className="text-2xl font-semibold text-gray-900 mt-4 mb-3">
              Regex → NFA
            </h2>

            <p className="text-gray-600 leading-relaxed">
              Convert a regular expression into a nondeterministic
              finite automaton and view its states and transitions.
            </p>

            <p className="text-indigo-600 font-medium mt-6">
              Open converter →
            </p>
          </Link>

          <Link
            href="/cfg-to-pda"
            className="block rounded-xl border border-gray-200 bg-white p-8 shadow-sm transition hover:border-indigo-400 hover:shadow-md"
          >
            <span className="text-sm font-medium text-indigo-600">
              Project 02
            </span>

            <h2 className="text-2xl font-semibold text-gray-900 mt-4 mb-3">
              CFG → PDA
            </h2>

            <p className="text-gray-600 leading-relaxed">
              Build a pushdown automaton from a context-free grammar
              and test whether strings belong to its language.
            </p>

            <p className="text-indigo-600 font-medium mt-6">
              Open converter →
            </p>
          </Link>
        </div>
      </div>
    </main>
  );
}
