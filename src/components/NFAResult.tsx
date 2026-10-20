import React from 'react';
// import Image from 'next/image';

interface NFA {
  start_state: string;
  accept_state: string;
  transitions: Record<string, Record<string, string[]>>;
  image_url: string;
}

interface NFAResultProps {
  nfa: NFA;
}

const NFAResult: React.FC<NFAResultProps> = ({ nfa }) => {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-800">NFA Result</h2>

      <div className="bg-gray-50 p-4 rounded-md">
        <h3 className="font-medium text-gray-700">Start State: <span className="font-bold">{nfa.start_state}</span></h3>
        <h3 className="font-medium text-gray-700">Accept State: <span className="font-bold">{nfa.accept_state}</span></h3>
      </div>

      <div>
        <h3 className="font-medium text-gray-700 mb-2">Transitions:</h3>
        <div className="bg-gray-50 p-4 rounded-md overflow-auto max-h-60">
          <pre className="text-sm text-gray-800">{JSON.stringify(nfa.transitions, null, 2)}</pre>
        </div>
      </div>

      <h3 className="font-medium mb-2">Visualization</h3>
      {nfa.image_url && (
        <div className="border rounded-lg p-4">
          <img
            src={`http://localhost:5000${nfa.image_url}`}
            alt="NFA Diagram"
            className="mx-auto"
          />

          {/* <Image
            src={`http://localhost:5000${nfa.image_url}`}
            alt="NFA Diagram"
            width={200} // Replace with your actual image width
            height={200} // Replace with your actual image height
            className="mx-auto"
            unoptimized // If the image is remote and not from a Next.js domain
          /> */}
        </div>
      )}
    </div>
  );
};

export default NFAResult;
