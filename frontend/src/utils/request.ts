import axios, { type AxiosRequestHeaders } from 'axios'
import { useTokenStore } from '@/stores/token'

const axio = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})

//请求拦截器来添加token
axio.interceptors.request.use((config) => {
  if (config.headers) {
    config.headers = {} as AxiosRequestHeaders
  }
  const store = useTokenStore()
  config.headers.Authorization = `Bearer ${store.getToken}`
  //拦截器修改完config还要返回
  return config
})

export default axio
