export default function FeatureSummary({ features, image }) {
  if (!features) return null

  const textureKeys = ['edge_density', 'contrast', 'brightness', 'saturation']

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Extracted Features</h3>

      {/* Uploaded Image Preview */}
      {image && (
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Your Image</label>
          <img
            src={URL.createObjectURL(image)}
            alt="Uploaded outfit"
            className="w-full h-48 object-cover rounded-lg border border-gray-200"
          />
        </div>
      )}

      {/* Dominant Colors */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">Dominant Colours</label>
        <div className="flex gap-2">
          {features.dominant_colors && features.dominant_colors.slice(0, 5).map((color, idx) => (
            <div
              key={idx}
              className="w-10 h-10 rounded border border-gray-200"
              style={{
                backgroundColor: `rgb(${color[0]}, ${color[1]}, ${color[2]})`,
              }}
              title={`RGB(${color[0]}, ${color[1]}, ${color[2]})`}
            ></div>
          ))}
        </div>
      </div>

      {/* Category Hint */}
      {features.clothing_hints && (
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Likely Category</label>
          <div className="inline-block px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">
            {features.clothing_hints.likely_category}
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Confidence: {(features.clothing_hints.confidence * 100).toFixed(0)}%
          </p>
        </div>
      )}

      {/* Style Tags */}
      {features.style_tags && features.style_tags.length > 0 && (
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Style Tags</label>
          <div className="flex flex-wrap gap-2">
            {features.style_tags.map((tag, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-medium"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Texture Features */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">Texture Analysis</label>
        <div className="space-y-1 text-sm">
          {features.texture && textureKeys.map((key) => (
            <div key={key} className="flex justify-between text-gray-600">
              <span className="capitalize">{key}:</span>
              <span className="font-medium">
                {(features.texture[key] * 100).toFixed(0)}%
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Explanation */}
      {features.explanation && features.explanation.length > 0 && (
        <div className="pt-4 border-t border-gray-200">
          <label className="block text-sm font-medium text-gray-700 mb-2">Analysis</label>
          <ul className="space-y-1">
            {features.explanation.map((exp, idx) => (
              <li key={idx} className="text-sm text-gray-600 flex items-start">
                <span className="text-indigo-600 mr-2">•</span>
                <span>{exp}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
