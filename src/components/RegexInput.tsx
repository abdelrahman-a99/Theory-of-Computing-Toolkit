import React from 'react';

interface RegexInputProps {
  regex: string;
  setRegex: React.Dispatch<React.SetStateAction<string>>;
  isLoading: boolean;
}

const RegexInput: React.FC<RegexInputProps> = ({ regex, setRegex, isLoading }) => {
  return (
    <div className="mb-4">
      <label htmlFor="regex" className="block text-sm font-medium text-gray-700 mb-2">
        Regular Expression
      </label>

      <input
        type="text"
        id="regex"
        value={regex}
        onChange={(e) => setRegex(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        placeholder="Enter regex (e.g., a|b*)"
        required
      />

      <button
        type="submit"
        disabled={isLoading}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? 'Converting...' : 'Convert to NFA'}
      </button>
    </div>
  );
};

export default RegexInput;
