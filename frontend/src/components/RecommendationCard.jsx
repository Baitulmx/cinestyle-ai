export default function RecommendationCard({ item }) {
  const score = typeof item.score === 'number' ? item.score : 0
  const matchPercentage = Math.round(score * 100)

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:scale-105 hover:-translate-y-1">
      {/* Image */}
      <div className="relative bg-gray-200 h-56 overflow-hidden group">
        <img
          src={item.image}
          alt={item.name}
          className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
          onError={(e) => {
            e.target.style.display = 'none'
            e.target.nextElementSibling.style.display = 'flex'
          }}
        />
        <div
          className="hidden w-full h-full bg-gray-300 items-center justify-center text-gray-600"
          style={{ display: 'none' }}
        >
          <span className="text-sm">Image not available</span>
        </div>

        {/* Match Score Badge */}
        <div className="absolute top-4 right-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-2 rounded-full text-lg font-bold shadow-xl animate-pulse">
          {matchPercentage}% ✓
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        {/* Name */}
        <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2">{item.name}</h3>

        {/* Category & Price */}
        <div className="flex justify-between items-center mb-4 pb-3 border-b border-gray-200">
          <span className="inline-block px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-bold capitalize">
            {item.category}
          </span>
          <span className="text-2xl font-bold text-indigo-600">£{Number(item.price || 0).toFixed(2)}</span>
        </div>

        {/* Style Tags */}
        {item.style_tags && item.style_tags.length > 0 && (
          <div className="mb-3 flex flex-wrap gap-1">
            {item.style_tags.slice(0, 2).map((tag, idx) => (
              <span key={idx} className="inline-block px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">
                {tag}
              </span>
            ))}
            {item.style_tags.length > 2 && (
              <span className="text-xs text-gray-500">+{item.style_tags.length - 2}</span>
            )}
          </div>
        )}

        {/* Match Reasons */}
        {item.reasons && item.reasons.length > 0 && (
          <div className="mb-4 pt-3 border-t border-gray-200">
            <p className="text-xs font-medium text-gray-700 mb-2">Why this match:</p>
            <ul className="space-y-1">
              {item.reasons.map((reason, idx) => (
                <li key={idx} className="text-xs text-gray-600 flex items-start">
                  <span className="text-indigo-600 mr-1">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Score Breakdown */}
        {item.score_breakdown && (
          <div className="mb-4 pt-3 border-t border-gray-200">
            <p className="text-xs font-medium text-gray-700 mb-2">Match Breakdown:</p>
            <div className="space-y-1 text-xs text-gray-600">
              <div className="flex justify-between">
                <span>Colour</span>
                <span className="font-medium">{Math.round(item.score_breakdown.colour * 100)}%</span>
              </div>
              <div className="flex justify-between">
                <span>Category</span>
                <span className="font-medium">{Math.round(item.score_breakdown.category * 100)}%</span>
              </div>
              <div className="flex justify-between">
                <span>Style</span>
                <span className="font-medium">{Math.round(item.score_breakdown.style_tags * 100)}%</span>
              </div>
            </div>
          </div>
        )}

        {/* View Button */}
        <a
          href={item.link}
          target="_blank"
          rel="noopener noreferrer"
          className="block w-full text-center px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition font-bold text-sm transform hover:scale-105 active:scale-95"
        >
          🛍️ View Item
        </a>
      </div>
    </div>
  )
}
