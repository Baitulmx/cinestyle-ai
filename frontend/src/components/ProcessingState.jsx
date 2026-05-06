export default function ProcessingState() {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="relative w-16 h-16 mb-8">
        <div className="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-indigo-600 rounded-full border-t-transparent animate-spin"></div>
      </div>
      
      <h3 className="text-xl font-semibold text-gray-900 mb-2">Analyzing Your Outfit</h3>
      <p className="text-gray-600 text-center max-w-md">
        Extracting colours, texture, shape and style characteristics...
      </p>
      
      <div className="mt-8 flex gap-2">
        <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
        <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
      </div>
    </div>
  )
}
