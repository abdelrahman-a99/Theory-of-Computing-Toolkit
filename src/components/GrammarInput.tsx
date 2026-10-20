type GrammarInputProps = {
  grammar: string;
  onChange: (value: string) => void;
  disabled: boolean;
  isLoading: boolean;
};

export default function GrammarInput({
  grammar,
  onChange,
  disabled,
  isLoading,
}: GrammarInputProps) {
  return (
    <>
      <label
        htmlFor="grammar"
        className="block font-medium text-gray-800 mb-3"
      >
        Context-free grammar
      </label>

      <textarea
        id="grammar"
        value={grammar}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
        required
        spellCheck={false}
        maxLength={8000}
        rows={6}
        className="w-full rounded-md border border-gray-300 p-4 font-mono text-sm text-gray-900 disabled:opacity-60"
      />

      <p className="mt-3 text-sm text-gray-600 leading-relaxed">
        First line: start symbol. Second line: comma-separated
        terminals. Then production rules, with spaces between
        symbols. Use ε for an empty production.
      </p>

      <button
        type="submit"
        disabled={disabled}
        className="mt-5 rounded-md bg-indigo-600 px-5 py-3 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
      >
        {isLoading ? 'Converting…' : 'Convert to PDA'}
      </button>
    </>
  );
}
