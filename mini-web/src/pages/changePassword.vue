<template>
    <v-card title="谁在校园-忘记密码" style="padding: 20px;margin: 30px;">
         <template v-slot:text>
          <v-text-field v-model="phoneNumber" label="手机号" variant="underlined"></v-text-field>
          <v-text-field v-model="code" label="验证码" variant="underlined">
            <template v-slot:append>
              <v-btn :loading="sendCodeLoading" @click="handleSendCode">发送验证码</v-btn>
            </template>
        </v-text-field>
          <v-text-field v-model="password" label="新密码" variant="underlined"></v-text-field>
          <v-alert v-if="errorMessage" title="错误" :text="errorMessage" type="error"></v-alert>
        </template>
        <v-card-actions>
          <v-btn :loading="resetPasswordLoading" @click="handleResetPassword">保存密码</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { resetPasswordAPI, sendCodeAPI } from '@/request/api/proxy';

const errorMessage = ref('')

const router = useRouter()
const phoneNumber = ref('')
const password = ref('')
const code = ref('')
const sendCodeLoading = ref(false)
const resetPasswordLoading = ref(false)


const handleResetPassword = async () => {
    resetPasswordLoading.value = true
    const { data, error } = await resetPasswordAPI(phoneNumber.value, password.value, code.value)
    resetPasswordLoading.value = false
    if (error.value != null) {
        errorMessage.value = error.value.message
        setTimeout(() => {
            errorMessage.value = ''
        }, 3000);
    } else {
        errorMessage.value = ''
        router.push('/login')
    }
}

const handleSendCode = async () => {
    sendCodeLoading.value = true
    const { data, error } = await sendCodeAPI(phoneNumber.value)
    sendCodeLoading.value = false
    if (error.value != null) {
        errorMessage.value = error.value.message
        setTimeout(() => {
            errorMessage.value = ''
        }, 3000);
    } else {
        errorMessage.value = ''
    }
}

</script>