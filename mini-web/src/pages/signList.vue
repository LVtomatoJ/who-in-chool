<template>
    <v-alert v-if="errorMessage" title="错误" :text="errorMessage" type="error"></v-alert>
    <v-list lines="two">
        <template v-for="(item, index) in signList" :key="index">
            <v-list-item >
                <v-list-item-content>
                    <v-list-item-title>{{ item.signTitle }}</v-list-item-title>
                    <v-list-item-subtitle>
                        <!-- 时间戳转string -->
                        开始时间：{{ new Date(item.start).toLocaleString() }} 
                        <br>结束时间： {{ new Date(item.end).toLocaleString() }}
                       
                    </v-list-item-subtitle>
                </v-list-item-content>
                <template v-slot:append>
                        <v-btn v-if="item.signStatus != 2" :loading="item.loading" @click="doSign(item.id)">校区暴力签到</v-btn>
                        <v-btn variant="text" v-else>已签到</v-btn>
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

const scrollToTop = () => {
    // 平滑滚动页面到顶部
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

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
    signList.value.map(item => {
        if (item.id === id) {
            item.loading = true
        }
    })
    const firstArea = signInfo.areaList[0]
    const latitude = firstArea.latitude
    const longitude = firstArea.longitude
    const { data, error } = await doSignAPI(appStore.jwSession, id, signInfo.signId, signInfo.schoolId, latitude, longitude);
    if (error.value != null) {
        console.log('失败啦', error.value.detail)
        scrollToTop()
        errorMessage.value = error.value.detail
        signList.value.map(item => {
            if (item.id === id) {
                item.loading = false
            }
        })
        setTimeout(() => {
            errorMessage.value = ''
        }, 3000);
    } else {
        signList.value.map(item => {
            if (item.id === id) {
                item.loading = false
            }
        })
        errorMessage.value = ''
    }
}

onMounted(() => {
    getSignList()
})


</script>

