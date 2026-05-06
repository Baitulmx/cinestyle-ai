import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const analyzeImage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const response = await api.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error analyzing image')
  }
}

export const recommendFromImage = async (file, filters = {}) => {
  const formData = new FormData()
  formData.append('file', file)
  
  if (filters.min_price !== undefined) {
    formData.append('min_price', filters.min_price)
  }
  if (filters.max_price !== undefined) {
    formData.append('max_price', filters.max_price)
  }
  if (filters.style_tags && filters.style_tags.length > 0) {
    formData.append('style_tags', filters.style_tags.join(','))
  }
  if (filters.categories && filters.categories.length > 0) {
    formData.append('categories', filters.categories.join(','))
  }
  
  try {
    const response = await api.post('/recommend-from-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error getting recommendations')
  }
}

export const recommendFromFeatures = async (features, filters) => {
  try {
    const response = await api.post('/recommend', {
      features,
      filters,
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error getting recommendations')
  }
}

export const getItems = async () => {
  try {
    const response = await api.get('/items')
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error fetching items')
  }
}

export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    return null
  }
}
