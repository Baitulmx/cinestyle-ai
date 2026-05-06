import { useState } from 'react'

export default function UploadPanel({ onImageSelect }) {
  const [isDragActive, setIsDragActive] = useState(false)
  const [selectedFileName, setSelectedFileName] = useState(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true)
    } else if (e.type === "dragleave") {
      setIsDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (isValidFile(file)) {
        setSelectedFileName(file.name)
        onImageSelect(file)
      }
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (isValidFile(file)) {
        setSelectedFileName(file.name)
        onImageSelect(file)
      }
    }
  }

  const isValidFile = (file) => {
    const validTypes = ['image/jpeg', 'image/png', 'image/webp']
    const validSize = file.size < 10 * 1024 * 1024 // 10MB

    if (!validTypes.includes(file.type)) {
      alert('Invalid file type. Please upload JPG, PNG, or WebP.')
      return false
    }
    
    if (!validSize) {
      alert('File is too large. Maximum size is 10MB.')
      return false
    }
    
    return true
  }

  return (
    <div className="mb-16">
      <div className="text-center mb-10">
        <h2 className="text-4xl font-bold text-gray-900 mb-3">📸 Upload Your Outfit</h2>
        <p className="text-lg text-gray-600">Drag a character outfit image or click to browse for similar real-world items</p>
      </div>

      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`border-3 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-all duration-300 ${
          isDragActive
            ? 'border-indigo-500 bg-indigo-50 scale-105 shadow-xl'
            : 'border-gray-300 hover:border-indigo-400 bg-gradient-to-br from-gray-50 to-white hover:shadow-lg'
        }`}
      >
        <input
          type="file"
          id="imageInput"
          onChange={handleChange}
          accept="image/jpeg,image/png,image/webp"
          style={{ display: 'none' }}
        />

        <label htmlFor="imageInput" className="cursor-pointer block">
          <svg
            className={`mx-auto h-20 w-20 mb-6 transition-all ${
              isDragActive ? 'text-indigo-500 scale-110' : 'text-gray-400'
            }`}
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20a4 4 0 004 4h24a4 4 0 004-4V20m-18-8l-4-4m0 0l-4 4m4-4v16m12-12l4 4m0 0l4-4m-4 4v8"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          
          <p className="text-xl font-bold text-gray-800 mb-3">
            {selectedFileName ? `✓ ${selectedFileName}` : '🎬 Drag & Drop Your Image Here'}
          </p>
          <p className="text-base text-gray-600 mb-6">or click below to browse your files</p>
          
          <button
            type="button"
            onClick={(e) => {
              e.preventDefault()
              document.getElementById('imageInput').click()
            }}
            className="inline-block px-8 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:shadow-lg transition font-bold transform hover:scale-105 active:scale-95"
          >
            Choose Image
          </button>
        </label>

        <p className="text-sm text-gray-500 mt-6">Supported: JPG, PNG, WebP • Max 10MB</p>
      </div>
    </div>
  )
}
