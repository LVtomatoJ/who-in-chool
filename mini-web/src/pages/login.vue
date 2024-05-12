<template>
    <v-card title="你在校园-登录" style="padding: 20px;margin: 30px;">
         <template v-slot:text>
          <v-combobox
            label="学校"
            v-model="selectSchoolName"
            :items="schoolNameList"
          ></v-combobox>
          <v-text-field v-model="phoneNumber" label="手机号" variant="underlined"></v-text-field>
          <v-text-field v-model="password" label="密码" variant="underlined"></v-text-field>
          <v-alert v-if="errorMessage" title="错误" :text="errorMessage" type="error"></v-alert>
        </template>
        <v-card-actions>
          <v-btn @click="handleLogin">登录</v-btn>
          <v-btn @click="handleResetPassword">忘记密码</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script setup>
import {
  ref, onMounted, computed
} from 'vue'
import { getSchoolListAPI, loginAPI } from '@/request/api/proxy';
import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router'

const appStore = useAppStore()
const router = useRouter()

const phoneNumber = ref('')
const password = ref('')
const schoolList = ref([])
const schoolNameList = computed(() => {
  return schoolList.value.map((item) => { return item.name })
})
const selectSchoolName = ref('')
const selectSchool = computed(() => {
  return schoolList.value.find(item => item.name === selectSchoolName.value)
})

const errorMessage = ref('')

const handleLogin = async () => {
  const { data, error } = await loginAPI(phoneNumber.value, password.value, selectSchool.value.id)
  if (error.value != null) {
    console.log('失败啦', error.value.detail)
    errorMessage.value = error.value.detail
  } else {
    errorMessage.value = ''
    const token = data.value.token
    appStore.token = token
    router.push("/home")
  }
}

const handleResetPassword = () => {
  router.push("/changePassword")
}

const getSchoolList = async () => {
  const { data } = await getSchoolListAPI();
  console.log(data.value)
  schoolList.value = data.value.data
}

onMounted(() => {
  getSchoolList()
})

</script>