<template>
    <v-alert v-if="errorMessage" title="错误" :text="errorMessage" type="error"></v-alert>
    <v-list lines="two">
        <template v-for="(item, index) in signList" :key="index">
            <v-list-item >
                <v-list-item-content>
                    <v-list-item-title>{{ item.signTitle }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.signContext }}</v-list-item-subtitle>
                </v-list-item-content>
                <template v-slot:append>
                        <v-btn @click="doSign(item.id)">签到</v-btn>
                </template>
            </v-list-item>
        </template>
    </v-list>
    <v-btn block v-if="haveMore" @click="getSignList">加载更多</v-btn>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'

import { getSignListAPI, doSignAPI } from '@/request/api/proxy'


const errorMessage = ref('')

const router = useRouter()
const appStore = useAppStore()

const signList = ref([])
const page = ref(1)

const haveMore = ref(true)

const getSignList = async () => {
    const { data, error } = await getSignListAPI(page.value, 10, appStore.jwSession);
    if (error.value != null) {
        console.log('失败啦', error.value.detail)
        errorMessage.value = error.value.detail
    } else {
        errorMessage.value = ''
        signList.value = signList.value.concat(data.value.data)
        if (data.value.data.length < 10) {
            haveMore.value = false
        }
        page.value++
    }
}


const doSign = async (id) => {
    const signInfo = signList.value.find(item => item.id === id)
    console.log(signInfo)
    const { data, error } = await doSignAPI(appStore.jwSession, id, signInfo.signId, signInfo.schoolId, signInfo.latitude, signInfo.longitude);
    if (error.value != null) {
        console.log('失败啦', error.value.detail)
        errorMessage.value = error.value.detail
    } else {
        errorMessage.value = ''
    }
}

onMounted(() => {
    getSignList()
})


</script>

