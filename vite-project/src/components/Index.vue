<template>

    <div class="common-layout">
        <el-container>
            <el-header  style="height:120px;background-color:white;padding-top: 0px;">
                <el-divider />
                <el-row align="middle">
                    <el-col :span="5">
                        谁在校园
                        
                    </el-col>
                    <div class="flex-grow" />
                    <el-col :span="2" >
                        <el-button type="primary" @click="toLoginOut">LogOut</el-button>
                    </el-col>
                </el-row>
                <el-divider />
            </el-header>
            <el-container>
                <el-aside width="200px">

                    <el-menu router=true default-active="index">
                        <el-menu-item index="index">
                            <el-icon>
                                <HomeFilled />
                            </el-icon>
                            <span>首页</span>
                        </el-menu-item>
                        <el-menu-item index="users" >
                            <el-icon>
                                <document />
                            </el-icon>
                            <span>绑定用户管理</span>
                        </el-menu-item>
                        <el-menu-item index="works" >
                            <el-icon>
                                <document />
                            </el-icon>
                            <span>任务管理</span>
                        </el-menu-item>
                        <el-menu-item index="admin" disabled>
                            <el-icon>
                                <setting />
                            </el-icon>
                            <span>管理</span>
                        </el-menu-item>
                    </el-menu>

                </el-aside>
                <el-main style="background-color:white;">
                    <router-view />
                </el-main>
            </el-container>
        </el-container>
    </div>



</template>



<script lang="ts" setup>
import { useRoute, useRouter } from 'vue-router'
import { store } from '../store'

const router = useRouter()
const route = useRoute()

const toLoginOut = () => {
    router.push('/login')
}

</script>

<style>
.flex-grow {
  flex-grow: 1;
}
</style>