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

    <el-tab-pane label="公告列表" name="noticlist">
        <el-table :data="notics" style="width: 100%">
            <el-table-column type="index"></el-table-column>
    <el-table-column prop="title" label="title" />
    <el-table-column prop="content" label="content"/>
    <el-table-column prop="time" label="time" />
    <el-table-column prop="show" label="show" />
    <el-table-column prop="noticid" label="noticid" />
        <el-table-column>
          <template #default="scope">
            <!-- <el-button link type="danger" size="small" @click="deleteUser(scope.$index)">
              删除
            </el-button> -->
            <el-button link type="success" size="small" @click="editNotic(scope.$index)">
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
            <el-input disabled v-model="userform.email" />
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

    <el-drawer v-model="noticdrawer " size="70%"
    title="编辑">
    <el-form>
        <el-form-item label="noticid">
            <el-input disabled v-model="noticform.noticid" />
        </el-form-item>
        <el-form-item label="title">
            <el-input v-model="noticform.title" />
        </el-form-item>
        <el-form-item label="content">
            <el-input v-model="noticform.content" />
        </el-form-item>
        <el-form-item label="time">
            <el-input v-model="noticform.time" />
        </el-form-item>
        <el-form-item label="show">
            <el-input v-model="noticform.show" />
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onNoticChange">修改</el-button>
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
import { stubFalse } from 'lodash';
const userdrawer = ref(false)
const noticdrawer = ref(false)
const activeName = ref('all')
var users = reactive<any[]>([])
var notics = reactive<any[]>([])
const userform = reactive({
    email: '',
    password: '',
    openid: '',
    level: 0,
    maxbindnum: 0,
    maxworknum: 0
})
const noticform = reactive({
    title: '',
    content: '',
    time: '',
    show: 0,
    noticid: '',
})
const tanChange = (tabname: any) => {
    if (tabname=='userlist') {
        getUsers()
    } else if (tabname=='noticlist') {
        getNotics()
    }{
        
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
      users.splice(0,users.length)
      r_users.forEach(e => {
        users.push(e);
     });
     console.log("users:")
     console.log(users)
    } else {
      // router.replace('/login')
    }

    // UserInfo.email="123"
    // console.log(UserInfo)
  })
}

const getNotics = () => {
  axios({
    method: 'get',
    url: '/v2/admin/getnotics',
    headers: { Authorization: 'Bearer ' + store.Authorization }
  }).then(function (response) {
    if (response) {
      let r_notics: any[] = response.data['data']['notics']
      notics.splice(0,notics.length)
      r_notics.forEach(e => {
        notics.push(e);
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

const editNotic = (index: number)=>{
    noticform.title=notics[index].title
    noticform.content=notics[index].content
    noticform.time=notics[index].time
    noticform.show=notics[index].show
    noticform.noticid=notics[index].noticid
    noticdrawer.value = true
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


const onNoticChange=()=>{
    const title = noticform.title
    const content = noticform.content
    const time = noticform.time
    const show = noticform.show
    const noticid = noticform.noticid
    axios({
    method: 'get',
    url:'/v2/admin/changenotic',
    headers: { Authorization: 'Bearer ' + store.Authorization},
    params: {
      title:title,content:content,time:time,show:show,noticid:noticid
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