import { useState } from 'react'

export default function FilterPanel({ filters, onFilterChange, categories, styleTags }) {
  const [maxPrice, setMaxPrice] = useState(filters.max_price)
  const [selectedCategories, setSelectedCategories] = useState(filters.categories || [])
  const [selectedTags, setSelectedTags] = useState(filters.style_tags || [])

  const applyFilters = () => {
    onFilterChange({
      min_price: filters.min_price,
      max_price: maxPrice,
      categories: selectedCategories,
      style_tags: selectedTags,
    })
  }

  const handleCategoryToggle = (cat) => {
    const updated = selectedCategories.includes(cat)
      ? selectedCategories.filter(c => c !== cat)
      : [...selectedCategories, cat]
    setSelectedCategories(updated)
  }

  const handleTagToggle = (tag) => {
    const updated = selectedTags.includes(tag)
      ? selectedTags.filter(t => t !== tag)
      : [...selectedTags, tag]
    setSelectedTags(updated)
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 sticky top-4">
      <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <span>🎨</span> Filters & Preferences
      </h3>

      {/* Budget */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-3">
          <label className="block text-sm font-bold text-gray-800">💰 Max Budget</label>
          <span className="text-2xl font-bold text-indigo-600">£{maxPrice}</span>
        </div>
        <input
          type="range"
          min="0"
          max="500"
          value={maxPrice}
          onChange={(e) => setMaxPrice(parseInt(e.target.value))}
          className="w-full h-3 bg-gradient-to-r from-indigo-200 to-indigo-400 rounded-full appearance-none cursor-pointer accent-indigo-600 hover:shadow-lg transition"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-2">
          <span>£0</span>
          <span>£500</span>
        </div>
      </div>

      {/* Categories */}
      <div className="mb-8">
        <label className="block text-sm font-bold text-gray-800 mb-3">👕 Categories</label>
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {categories.map((cat) => (
            <label key={cat} className="flex items-center">
              <input
                type="checkbox"
                checked={selectedCategories.includes(cat)}
                onChange={() => handleCategoryToggle(cat)}
                className="w-4 h-4 text-indigo-600 rounded cursor-pointer"
              />
              <span className="ml-2 text-sm text-gray-700 capitalize cursor-pointer">{cat}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Style Tags */}
      <div className="mb-8">
        <label className="block text-sm font-bold text-gray-800 mb-3">✨ Style Tags</label>
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {styleTags.map((tag) => (
            <label key={tag} className="flex items-center">
              <input
                type="checkbox"
                checked={selectedTags.includes(tag)}
                onChange={() => handleTagToggle(tag)}
                className="w-5 h-5 text-indigo-600 rounded cursor-pointer accent-indigo-600"
              />
              <span className="ml-3 text-sm text-gray-700 capitalize cursor-pointer hover:text-indigo-600 transition">{tag}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Apply Filters Button */}
      <button
        onClick={applyFilters}
        className="w-full px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:shadow-lg transition font-bold text-base transform hover:scale-105 active:scale-95"
      >
        ✓ Apply Filters
      </button>
    </div>
  )
}
