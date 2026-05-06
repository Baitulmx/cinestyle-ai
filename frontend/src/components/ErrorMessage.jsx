export default function ErrorMessage({ error, onRetry }) {
  return (
    <div className="max-w-md mx-auto py-12">
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-start">
          <svg
            className="w-6 h-6 text-red-600 mt-0.5 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>

          <div className="ml-4">
            <h3 className="text-lg font-medium text-red-800">Error Processing Image</h3>
            <p className="mt-2 text-sm text-red-700">{error}</p>
            
            <button
              onClick={onRetry}
              className="mt-4 inline-block px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition font-medium"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
