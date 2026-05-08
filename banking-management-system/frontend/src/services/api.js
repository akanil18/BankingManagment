import axios from 'axios'
import { getToken, getRefreshToken, setToken, setRefreshToken, clearTokens } from '@/utils/tokenHelper'

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
})

api.interceptors.request.use(config => {
  const token = getToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  async err => {
    const original = err.config
    if (err.response?.status === 401 && !original._retry) {
      original._retry = true
      try {
        const refreshToken = getRefreshToken()
        const { data } = await axios.post(
          `${process.env.VUE_APP_API_URL}/auth/refresh`,
          { refresh_token: refreshToken }
        )
        setToken(data.access_token)
        setRefreshToken(data.refresh_token)
        original.headers.Authorization = `Bearer ${data.access_token}`
        return api(original)
      } catch {
        clearTokens()
        window.location.href = '/login'
      }
    }
    return Promise.reject(err)
  }
)

export default api
