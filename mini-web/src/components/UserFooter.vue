<template>
<v-bottom-navigation @update:modelValue='handleNavigation' :model-value='pageValue' :elevation="7" mode="shift">
  <v-btn value="home">
    <v-icon>mdi-home</v-icon>
    <span>首页</span>
  </v-btn>
  <v-btn value="message">
    <v-icon>mdi-message</v-icon>
    <span>留言</span>
  </v-btn>
   <v-btn value="account">
    <v-icon>mdi-account-edit</v-icon>
    <span>用户</span>
  </v-btn>
</v-bottom-navigation>
</template>
<script setup>
const props = defineProps(['pageValue'])
import { useRouter } from 'vue-router'
const router = useRouter();

const handleNavigation = (page) => {
  console.log('page')
  console.log(page)
  if (page === 'home') {
    router.push('/home')
  } else if (page === 'message') {
    router.push('/home/message')
  }else if(page === 'account'){
    router.push('/home/account')
  }
}
</script>