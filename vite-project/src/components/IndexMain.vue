<template>
      <el-descriptions
    class="margin-top"
    title="账号信息"
    :column="2"
    border
    direction="vertical"
  >
    <template #extra>
      <el-button type="primary" @click="getdUserInfo">刷新</el-button>
    </template>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
            <el-icon><Message /></el-icon>
            &nbsp邮箱
        </div>
      </template>
      {{store.UserInfo.email}}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon >
            <location />
          </el-icon>
          &nbsp等级
        </div>
      </template>
      {{store.UserInfo.level}}级
    </el-descriptions-item>

    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <tickets />
          </el-icon>
          &nbsp最大绑定
        </div>
      </template>
      {{store.UserInfo.maxbindnum}}个
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon >
            <office-building />
          </el-icon>
          &nbsp最大任务
        </div>
      </template>
     {{store.UserInfo.maxworknum}}个
    </el-descriptions-item>

  </el-descriptions>
</template>

<script lang="ts" setup>
import {store} from '../store'
import axios from '../defaultaxios'
import { onBeforeMount, reactive ,ref} from 'vue'
import router from '../router/router';
const Authorization = store.Authorization
// let UserInfo = ref(store.UserInfo)
// let UserInfo = reactive({
//     email:"",
//     openid:'demo',
//     level:2,
//     maxbindnum:1,
//     maxworknum:1
// })

onBeforeMount(() => {
    //   console.log(store.Authorization)
    getdUserInfo()
})

const getdUserInfo = ()=>{
    axios({
        method: 'get',
        url: '/v2/getuserinfo',
        headers: { Authorization: 'Bearer ' + store.Authorization }
    }).then(function (response) {
        // console.log(typeof(response))
        // console.log(response)
        if (response){

            store.UserInfo=response.data['data']['user']
        }else{
            // router.replace('/login')
        }
          
            // UserInfo.email="123"
        // console.log(UserInfo)
    })
}
    
</script>

<style>
.cell-item {
  display: flex;
  align-items: center;
}
</style>