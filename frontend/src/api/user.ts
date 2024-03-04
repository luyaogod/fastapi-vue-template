import axio from '@/utils/request'

interface loginInfo {
  username: string
  password: string
  scope?: string
}

interface LoginResult {
  access_token: string
  token_type: string
}

export async function login(loginInfo: loginInfo): Promise<LoginResult> {
  const response = await axio.post(
    '/login/token',
    `username=${loginInfo.username}&password=${loginInfo.password}`
  )
  return response.data
}
