import RecommendationCard from './RecommendationCard'

export default function ResultsGrid({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 text-lg">No recommendations found matching your filters.</p>
        <p className="text-gray-500 text-sm mt-2">Try adjusting your filters and try again.</p>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        Recommendations ({recommendations.length})
      </h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {recommendations.map((item) => (
          <RecommendationCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  )
}
