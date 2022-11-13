<template>
    <h1>index page</h1>
    <p><el-button type="primary"  @click="toLogin">Login</el-button></p>
    <p>{{store.Authorization}}</p>
    
    
</template>


<script lang="ts" setup>
import {useRoute,useRouter} from 'vue-router'
import {store} from '../store'

const router = useRouter()
const route = useRoute()

const toLogin = ()=>{
    router.push('/login')
}

</script>