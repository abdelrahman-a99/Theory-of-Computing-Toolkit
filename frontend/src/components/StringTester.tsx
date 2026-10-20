import type { FormEventHandler } from 'react';

export type StringTestResult = {
  word: string;
  accepted: boolean | null;
  status: 'accepted' | 'rejected' | 'inconclusive';
  message?: string;
};

type StringTesterProps = {
  word: string;
  onChange: (value: string) => void;
  onSubmit: FormEventHandler<HTMLFormElement>;
  disabled: boolean;
  isLoading: boolean;
  error: string;
  result: StringTestResult | null;
};

export default function StringTester({
  word,
  onChange,
  onSubmit,
  disabled,
  isLoading,
  error,
  result,
}: StringTesterProps) {
  const resultClass =
    result?.status === 'accepted'
      ? 'bg-green-50 text-green-800'
      : result?.status === 'rejected'
        ? 'bg-red-50 text-red-800'
        : 'bg-amber-50 text-amber-800';

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-2">
        Test a string
      </h2>

      <p className="text-sm text-gray-600 mb-5">
        Leave the input empty to test the empty string ε.
      </p>

      <form
        onSubmit={onSubmit}
        className="flex flex-col gap-3 sm:flex-row"
      >
        <label htmlFor="test-word" className="sr-only">
          String to test
        </label>

        <input
          id="test-word"
          value={word}
          onChange={(event) => onChange(event.target.value)}
          disabled={disabled}
          maxLength={120}
          spellCheck={false}
          placeholder="Empty string (ε)"
          className="min-w-0 flex-1 rounded-md border border-gray-300 p-3 font-mono text-gray-900"
        />

        <button
          type="submit"
          disabled={disabled}
          className="rounded-md bg-indigo-600 px-5 py-3 text-sm font-medium text-white disabled:opacity-50"
        >
          {isLoading ? 'Testing…' : 'Test string'}
        </button>
      </form>

      {error && (
        <p role="alert" className="mt-4 text-sm text-red-700">
          {error}
        </p>
      )}

      {result && (
        <div
          role="status"
          className={`mt-5 rounded-md p-4 text-sm ${resultClass}`}
        >
          <p className="font-semibold">
            {result.status === 'accepted'
              ? '✓ Accepted'
              : result.status === 'rejected'
                ? '✗ Rejected'
                : '? Inconclusive'}
          </p>

          <p className="mt-2">
            {result.message ??
              `Test string: ${result.word || 'ε'}`}
          </p>
        </div>
      )}
    </div>
  );
}
