export interface userData {
  user_name: string
  id: number
  user_status: number
  super_admin: boolean
  exp: number
  role: Array<string>
}

export function tokenPayloadDecoding(Token: string): userData {
  try {
    const tokenList = Token.split('.')
    const data = tokenList[1]
    const decodedString = atob(data)
    const jsondata = JSON.parse(decodedString)
    return jsondata
  } catch (error) {
    throw new Error('Token parsing Error')
  }
}

export function tokenVertify(Token: string): boolean {
  try {
    const dataObj = tokenPayloadDecoding(Token)
    if (dataObj !== null) {
      const exptime = dataObj.exp
      const currentTimestamp: number = Math.floor(Date.now() / 1000)
      return exptime > currentTimestamp
    } else return false
  } catch (error) {
    return false
  }
}
