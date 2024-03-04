import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { tokenPayloadDecoding, type userData } from '@/utils/jwt'

export const useTokenStore = defineStore('mytoken', () => {
  const token = ref('')

  const getToken = computed(() => {
    return token.value || window.localStorage.getItem('TokenInfo') || ''
  })

  const getUserObj = computed((): userData | null => {
    const token = getToken.value
    if (token == '') {
      return null
    } else {
      try {
        const UserJson = tokenPayloadDecoding(token)
        return UserJson
      } catch (error) {
        return null
      }
    }
  })

  function saveToken(data: string) {
    window.localStorage.setItem('TokenInfo', data)
  }

  return { token, getToken, getUserObj, saveToken }
})
