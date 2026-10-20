type Transition = {
  from: string;
  input: string;
  pop: string;
  to: string;
  push: string;
};

export type PDAResultData = {
  start_state: string;
  accept_state: string;
  states: string[];
  transitions: Transition[];
  image_url: string;
};

type PDAResultProps = {
  result: PDAResultData;
  apiUrl: string;
};

export default function PDAResult({
  result,
  apiUrl,
}: PDAResultProps) {
  const summary = [
    { label: 'States', value: result.states.length },
    { label: 'Transitions', value: result.transitions.length },
    { label: 'Start state', value: result.start_state },
    { label: 'Accept state', value: result.accept_state },
  ];

  const imageUrl = `${apiUrl}${result.image_url}`;

  return (
    <>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {summary.map(({ label, value }) => (
          <div
            key={label}
            className="rounded-lg border border-gray-200 bg-white p-4"
          >
            <p className="text-sm text-gray-600">{label}</p>
            <p className="mt-2 font-mono text-xl text-gray-900">
              {value}
            </p>
          </div>
        ))}
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-5">
          <h2 className="text-xl font-semibold text-gray-900">
            PDA diagram
          </h2>

          <a
            href={imageUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-indigo-600 hover:underline"
          >
            Open full image ↗
          </a>
        </div>

        <div className="overflow-auto">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={imageUrl}
            alt="Generated pushdown automaton"
            className="mx-auto h-auto max-w-full"
          />
        </div>

        <p className="mt-4 text-sm text-gray-600">
          Edge labels: input, pop → push. Acceptance requires
          all input consumed, an empty stack, and the accept state.
        </p>
      </div>

      <details className="rounded-xl border border-gray-200 bg-white p-6">
        <summary className="cursor-pointer font-semibold text-gray-900">
          Transition table
        </summary>

        <div className="mt-5 overflow-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-gray-50 text-gray-700">
              <tr>
                {['From', 'Input', 'Pop', 'Push', 'To'].map(
                  (column) => (
                    <th key={column} className="p-3">
                      {column}
                    </th>
                  ),
                )}
              </tr>
            </thead>

            <tbody className="font-mono text-gray-800">
              {result.transitions.map((transition, index) => (
                <tr
                  key={index}
                  className="border-t border-gray-100"
                >
                  <td className="p-3">{transition.from}</td>
                  <td className="p-3">{transition.input}</td>
                  <td className="p-3">{transition.pop}</td>
                  <td className="p-3">{transition.push}</td>
                  <td className="p-3">{transition.to}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </>
  );
}
