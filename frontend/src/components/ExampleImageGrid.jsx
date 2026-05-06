export default function ExampleImageGrid({ onImageSelect }) {
  // Sample outfit images (using placeholder URLs)
  const sampleOutfits = [
    {
      id: 'example_1',
      name: 'Dark Formal Jacket Look',
      description: 'Black leather jacket with professional styling',
      color: 'from-gray-900 to-gray-700',
      icon: '🧥'
    },
    {
      id: 'example_2',
      name: 'Casual White Minimalist',
      description: 'Clean, bright minimalist aesthetic',
      color: 'from-gray-100 to-gray-300',
      icon: '👕'
    },
    {
      id: 'example_3',
      name: 'Vintage Burgundy Style',
      description: 'Rich vintage colours and classic cuts',
      color: 'from-red-900 to-red-700',
      icon: '🧤'
    },
    {
      id: 'example_4',
      name: 'Edgy Dark Ensemble',
      description: 'Modern edgy black outfit',
      color: 'from-black to-gray-800',
      icon: '🖤'
    },
    {
      id: 'example_5',
      name: 'Professional Blue Formal',
      description: 'Navy blazer professional look',
      color: 'from-blue-900 to-blue-700',
      icon: '💼'
    },
    {
      id: 'example_6',
      name: 'Casual Denim Style',
      description: 'Classic denim and casual wear',
      color: 'from-blue-700 to-blue-500',
      icon: '👖'
    }
  ]

  const handleSelectExample = (outfit) => {
    const canvas = document.createElement('canvas')
    canvas.width = 400
    canvas.height = 500
    const ctx = canvas.getContext('2d')

    const colourMap = {
      example_1: ['#111827', '#374151'],
      example_2: ['#f9fafb', '#d1d5db'],
      example_3: ['#7f1d1d', '#991b1b'],
      example_4: ['#030712', '#1f2937'],
      example_5: ['#1e3a8a', '#1d4ed8'],
      example_6: ['#1d4ed8', '#60a5fa']
    }

    const [start, end] = colourMap[outfit.id] || ['#374151', '#111827']

    const grad = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
    grad.addColorStop(0, start)
    grad.addColorStop(1, end)
    ctx.fillStyle = grad
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    ctx.font = 'bold 120px Arial'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(outfit.icon, canvas.width / 2, canvas.height / 2 - 40)

    ctx.font = 'bold 24px Arial'
    ctx.fillStyle = '#ffffff'
    ctx.fillText(outfit.name, canvas.width / 2, canvas.height / 2 + 100)

    canvas.toBlob((blob) => {
      const file = new File([blob], `${outfit.id}.png`, { type: 'image/png' })
      onImageSelect(file)
    }, 'image/png')
  }

  return (
    <div className="mb-12">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Or Try an Example</h2>
        <p className="text-gray-600">Select a sample character outfit to see how the system works</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {sampleOutfits.map((outfit) => (
          <button
            key={outfit.id}
            onClick={() => handleSelectExample(outfit)}
            className="group cursor-pointer"
          >
            <div className={`bg-gradient-to-br ${outfit.color} rounded-lg p-6 h-48 flex flex-col items-center justify-center text-white hover:shadow-lg transition transform hover:scale-105`}>
              <div className="text-5xl mb-3">{outfit.icon}</div>
              <h3 className="font-bold text-sm text-center leading-tight">{outfit.name}</h3>
              <p className="text-xs text-gray-200 mt-2 text-center">{outfit.description}</p>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
