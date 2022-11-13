import { reactive } from 'vue'

export const store = reactive({
    Authorization: "",
    setAuthorization(auth: string) {
        this.Authorization=auth
      }
})