<template>

    <div  class="common-layout">
        <el-container>
            <el-header style="height:120px;background-color:white;padding-top: 0px;">
                <el-divider />
                <!-- <el-row align="middle"> -->
                <!-- <div class="flex-grow" /> -->
                <!-- <el-col :span="3"> -->
                <el-button type="primary" text>谁在校园</el-button>
                <!-- </el-col> -->
                <!-- <div class="flex-grow" /> -->
                <!-- <el-col :span="3">
                        <el-button  type="primary" @click="toLoginOut">退出</el-button>
                    </el-col> -->
                <!-- </el-row> -->
                <el-divider />
            </el-header>
            <el-container>
                <el-aside width="auto">
                    <!-- <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
                        <el-radio-button size="small" :label="false">展开</el-radio-button>
                        <el-radio-button size="small" :label="true">缩小</el-radio-button>
                    </el-radio-group> -->
                    <el-button :icon="Expand" style="margin-left: 10px;margin-bottom: 10px;"
                        @click="isCollapse = !isCollapse" />
                    <el-menu :collapse="isCollapse" router default-active="index">
                        <el-menu-item index="index">
                            <el-icon>
                                <HomeFilled />
                            </el-icon>
                            <span>首页</span>
                        </el-menu-item>
                        <el-menu-item index="users">
                            <el-icon>
                                <User />
                            </el-icon>
                            <span>绑定用户管理</span>
                        </el-menu-item>
                        <el-menu-item index="works">
                            <el-icon>
                                <Tickets />
                            </el-icon>
                            <span>任务管理</span>
                        </el-menu-item>
                        <template v-if="store.UserInfo.level == 999">

                            <el-menu-item index="admin">
                                <el-icon>
                                    <setting />
                                </el-icon>
                                <span>管理</span>
                            </el-menu-item>
                        </template>
                    </el-menu>

                </el-aside>
                <el-container>
                    <el-main style="background-color:white;">
                        <router-view />
                    </el-main>
                    <el-footer>
                        <!-- <div style="font-size: 15px;position:absolute;bottom:10px;left: 45%;">
                           <a href="https://beian.miit.gov.cn/">
                            陕ICP备2022013710号-1     
                           </a>            
                        </div> -->
                    </el-footer>
                </el-container>
            </el-container>

        </el-container>

    </div>



</template>



<script lang="ts" setup>
import {
    Expand, Ticket
} from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { store } from '../store'
import axios from '../defaultaxios'
import { onBeforeMount, ref } from 'vue'

const router = useRouter()
const route = useRoute()

const isCollapse = ref(true)
const toLoginOut = () => {
    router.push('/login')
}

onBeforeMount(() => {
    //   console.log(store.Authorization)
    getBinds()
    getdUserInfo()
})

const getBinds = () => {
    axios({
        method: 'get',
        url: '/v2/getbinds',
        headers: { Authorization: 'Bearer ' + store.Authorization }
    }).then(function (response) {
        // console.log(typeof(response))
        // console.log(response)
        if (response) {
            const r_binds = response.data['data']['binds']
            store.Binds = r_binds
            // console.log(r_binds)
        } else {
            // router.replace('/login')
        }

        // UserInfo.email="123"
        // console.log(UserInfo)
    })
}

const getdUserInfo = () => {
    axios({
        method: 'get',
        url: '/v2/getuserinfo',
        headers: { Authorization: 'Bearer ' + store.Authorization }
    }).then(function (response) {
        // console.log(typeof(response))
        // console.log(response)
        if (response) {

            store.UserInfo = response.data['data']['user']
        } else {
            // router.replace('/login')
        }

        // UserInfo.email="123"
        // console.log(UserInfo)
    })
}

</script>

<style>
.flex-grow {
    flex-grow: 1;
}
</style>