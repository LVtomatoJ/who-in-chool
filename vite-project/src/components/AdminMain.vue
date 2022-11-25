<template>
    <el-tabs v-model="activeName" @tab-change="tanChange">
    <el-tab-pane label="总览" name="all">
        总览
    </el-tab-pane>

    <el-tab-pane label="用户列表" name="userlist">
        <el-table :data="users" style="width: 100%">
            <el-table-column type="index"></el-table-column>
    <el-table-column prop="email" label="email" />
    <el-table-column prop="password" label="passowrd"/>
    <el-table-column prop="openid" label="openid" />
    <el-table-column prop="level" label="level" />
    <el-table-column prop="maxbindnum" label="maxbind" />
    <el-table-column prop="maxworknum" label="maxwork" />
    <el-table-column fixed="right" label="操作" width="auto">
          <template #default="scope">
            <!-- <el-button link type="danger" size="small" @click="deleteUser(scope.$index)">
              删除
            </el-button> -->
            <el-button link type="success" size="small" @click="editUser(scope.$index)">
              编辑
            </el-button>
          </template>
        </el-table-column>
  </el-table>
    </el-tab-pane>
    </el-tabs>

    <el-drawer v-model="userdrawer " size="70%"
    title="编辑">
    <el-form>
        <el-form-item label="email">
            <el-input v-model="userform.email" />
        </el-form-item>
        <el-form-item label="password">
            <el-input v-model="userform.password" />
        </el-form-item>
        <el-form-item label="openid">
            <el-input v-model="userform.openid" />
        </el-form-item>
        <el-form-item label="level">
            <el-input v-model="userform.level" />
        </el-form-item>
        <el-form-item label="maxbindnum">
            <el-input v-model="userform.maxbindnum" />
        </el-form-item>
        <el-form-item label="maxworknum">
            <el-input v-model="userform.maxworknum" />
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onUserChange">修改</el-button>
        </el-form-item>
    </el-form>

    </el-drawer>

</template>

<script lang="ts" setup>
import { onBeforeMount } from 'vue';
import { ElMessage, ElMessageBox, formContextKey } from 'element-plus'
import { ref, reactive } from 'vue'
import type { TabsPaneContext } from 'element-plus'
import axios from '../defaultaxios';
import { store } from '../store'
const userdrawer = ref(false)
const activeName = ref('all')
var users = reactive<any[]>([])
const userform = reactive({
    email: '',
    password: '',
    openid: '',
    level: 0,
    maxbindnum: 0,
    maxworknum: 0
})
const tanChange = (tabname: any) => {
    if (tabname=='userlist') {
        getUsers()
    } else {
        
    }
//   console.log(tabname)
}

const getUsers = () => {
  axios({
    method: 'get',
    url: '/v2/admin/getusers',
    headers: { Authorization: 'Bearer ' + store.Authorization }
  }).then(function (response) {
    if (response) {
      let r_users: any[] = response.data['data']['users']
      users = users.slice(0,0)
      r_users.forEach(e => {
        users.push(e);
     });
    } else {
      // router.replace('/login')
    }

    // UserInfo.email="123"
    // console.log(UserInfo)
  })
}

const editUser = (index: number)=>{
    userform.email=users[index].email
    userform.password=users[index].password
    userform.openid=users[index].openid
    userform.level=users[index].level
    userform.maxbindnum=users[index].maxbindnum
    userform.maxworknum=users[index].maxworknum
    userdrawer.value = true
}

const onUserChange=()=>{
    const email = userform.email
    const password = userform.password
    const openid = userform.openid
    const level = userform.level
    const maxbindnum = userform.maxbindnum
    const maxworknum = userform.maxworknum
    axios({
    method: 'get',
    url:'/v2/admin/changeuser',
    headers: { Authorization: 'Bearer ' + store.Authorization},
    params: {
      email:email,password:password,openid:openid,level:level,maxbindnum:maxbindnum,maxworknum:maxworknum
    },
  }).then(function (response){
    if(response.data['code']==0){
      ElMessage({
        message: "修改成功",
        grouping: true,
        type: 'success',
      })
      getUsers()
      userdrawer.value = false

    }else{
      ElMessage({
        message: "修改失败：,"+response.data['msg'],
        grouping: true,
        type: 'error',
      })
    }
  })
}

</script>