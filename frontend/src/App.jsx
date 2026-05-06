import { useState, useEffect } from 'react'
import Header from './components/Header'
import UploadPanel from './components/UploadPanel'
import ProcessingState from './components/ProcessingState'
import FeatureSummary from './components/FeatureSummary'
import FilterPanel from './components/FilterPanel'
import ResultsGrid from './components/ResultsGrid'
import ErrorMessage from './components/ErrorMessage'
import ExampleImageGrid from './components/ExampleImageGrid'
import { recommendFromImage, recommendFromFeatures, healthCheck } from './api/api'

function App() {
  const [currentState, setCurrentState] = useState('initial') // initial, uploading, results, error
  const [selectedImage, setSelectedImage] = useState(null)
  const [extractedFeatures, setExtractedFeatures] = useState(null)
  const [recommendations, setRecommendations] = useState([])
  const [filters, setFilters] = useState({
    min_price: 0,
    max_price: 200,
    style_tags: [],
    categories: [],
  })
  const [error, setError] = useState(null)
  const [backendAvailable, setBackendAvailable] = useState(true)
  const [allCategories, setAllCategories] = useState([
    'jacket', 'coat', 'shirt', 't-shirt', 'hoodie', 'trousers', 
    'jeans', 'shoes', 'boots', 'dress', 'skirt', 'accessory'
  ])
  const [allStyleTags, setAllStyleTags] = useState([
    'formal', 'casual', 'vintage', 'dark', 'edgy', 'professional',
    'streetwear', 'minimalist', 'sporty'
  ])

  // Check backend availability on mount
  useEffect(() => {
    const checkBackend = async () => {
      const health = await healthCheck()
      setBackendAvailable(!!health)
    }
    checkBackend()
  }, [])

  const handleImageSelect = async (file) => {
    if (!backendAvailable) {
      setError('Backend server is not available. Please ensure it\'s running on http://localhost:8000')
      setCurrentState('error')
      return
    }

    setSelectedImage(file)
    setCurrentState('uploading')
    setError(null)

    try {
      const result = await recommendFromImage(file, filters)
      setExtractedFeatures(result.query_features)
      setRecommendations(result.recommendations)
      setCurrentState('results')
    } catch (err) {
      setError(err.message || 'Error processing image. Please try again.')
      setCurrentState('error')
      setSelectedImage(null)
    }
  }

  const handleFilterChange = async (newFilters) => {
    setFilters(newFilters)
    
    if (extractedFeatures) {
      setCurrentState('uploading')
      try {
        const result = await recommendFromFeatures(extractedFeatures, newFilters)
        setRecommendations(result.recommendations)
        setCurrentState('results')
      } catch (err) {
        setError(err.message || 'Error applying filters')
        setCurrentState('error')
      }
    }
  }

  const handleReset = () => {
    setCurrentState('initial')
    setSelectedImage(null)
    setExtractedFeatures(null)
    setRecommendations([])
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header onReset={handleReset} />
      
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Initial State */}
        {currentState === 'initial' && (
          <>
            <UploadPanel onImageSelect={handleImageSelect} />
            <ExampleImageGrid onImageSelect={handleImageSelect} />
          </>
        )}

        {/* Processing State */}
        {currentState === 'uploading' && (
          <ProcessingState />
        )}

        {/* Error State */}
        {currentState === 'error' && (
          <ErrorMessage error={error} onRetry={handleReset} />
        )}

        {/* Results State */}
        {currentState === 'results' && extractedFeatures && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
              <div className="lg:col-span-1">
                <div className="sticky top-8">
                  <FeatureSummary features={extractedFeatures} image={selectedImage} />
                  <FilterPanel 
                    filters={filters}
                    onFilterChange={handleFilterChange}
                    categories={allCategories}
                    styleTags={allStyleTags}
                  />
                </div>
              </div>
              <div className="lg:col-span-2">
                <ResultsGrid recommendations={recommendations} />
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default App
