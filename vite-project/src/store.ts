import { reactive } from 'vue'

export const store = reactive({
    Authorization: "",
    setAuthorization(auth: string) {
        this.Authorization=auth
      },
    UserInfo:{
      email:'',
      level:0,
      maxbindnum:0,
      maxworknum:0
    },
    Binds:<any[]>[],
    Works:<any[]>[],
})