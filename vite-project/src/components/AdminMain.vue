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

    <el-tab-pane label="绑定列表" name="bindlist">
        <el-table :data="binds" style="width: 100%">
            <el-table-column type="index"></el-table-column>
    <el-table-column prop="bindid" label="bindid" />
    <el-table-column prop="password" label="password"/>
    <el-table-column prop="jwsession" label="jwsession" />
    <el-table-column prop="status" label="status" />
    <el-table-column prop="email" label="email" />
    <el-table-column prop="notes" label="notes" />
    <el-table-column prop="school" label="school" />
        <el-table-column>
          <template #default="scope">
            <!-- <el-button link type="danger" size="small" @click="deleteUser(scope.$index)">
              删除
            </el-button> -->
            <el-button link type="success" size="small" @click="editBind(scope.$index)">
              编辑
            </el-button>
          </template>
        </el-table-column>
  </el-table>
    </el-tab-pane>

    <el-tab-pane label="任务列表" name="worklist">
        <el-table :data="works" style="width: 100%">
            <el-table-column type="index"></el-table-column>
    <el-table-column prop="workid" label="workid" />
    <el-table-column prop="status" label="status"/>
    <el-table-column prop="bindid" label="bindid" />
    <el-table-column prop="starttime" label="starttime" />
    <el-table-column prop="endtime" label="endtime" />
    <el-table-column prop="email" label="email" />
    <el-table-column prop="templateid" label="templateid" />
        <el-table-column>
          <template #default="scope">
            <!-- <el-button link type="danger" size="small" @click="deleteUser(scope.$index)">
              删除
            </el-button> -->
            <el-button link type="success" size="small" @click="editWork(scope.$index)">
              编辑
            </el-button>
          </template>
        </el-table-column>
  </el-table>
    </el-tab-pane>

    
    </el-tabs>

    <el-drawer v-model="userdrawer " size="70%"
    title="编辑用户">
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
    title="编辑公告">
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


    <el-drawer v-model="binddrawer " size="70%"
    title="编辑绑定">
    <el-form>
        <el-form-item label="bindid">
            <el-input disabled v-model="bindform.bindid" />
        </el-form-item>
        <el-form-item label="password">
            <el-input v-model="bindform.password" />
        </el-form-item>
        <el-form-item label="jwsession">
            <el-input v-model="bindform.jwsession" />
        </el-form-item>
        <el-form-item label="status">
            <el-input v-model="bindform.status" />
        </el-form-item>
        <el-form-item label="email">
            <el-input v-model="bindform.email" />
        </el-form-item>
        <el-form-item label="notes">
            <el-input v-model="bindform.notes" />
        </el-form-item>
        <el-form-item label="school">
            <el-input v-model="bindform.school" />
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onBindChange">修改</el-button>
        </el-form-item>
    </el-form>
    </el-drawer>

    <el-drawer v-model="workdrawer " size="70%"
    title="编辑任务">
    <el-form>
        <el-form-item label="workid">
            <el-input disabled v-model="workform.workid" />
        </el-form-item>
        <el-form-item label="password">
            <el-input v-model="workform.templateid" />
        </el-form-item>
        <el-form-item label="jwsession">
            <el-input v-model="workform.bindid" />
        </el-form-item>
        <el-form-item label="status">
            <el-input v-model="workform.status" />
        </el-form-item>
        <el-form-item label="email">
            <el-input v-model="workform.starttime" />
        </el-form-item>
        <el-form-item label="notes">
            <el-input v-model="workform.endtime" />
        </el-form-item>
        <el-form-item label="school">
            <el-input v-model="workform.email" />
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onWorkChange">修改</el-button>
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
const binddrawer = ref(false)
const workdrawer = ref(false)
const activeName = ref('all')
var users = reactive<any[]>([])
var notics = reactive<any[]>([])
var binds = reactive<any[]>([])
var works = reactive<any[]>([])
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
const bindform = reactive({
    bindid: '',
    password: '',
    email: '',
    status: 0,
    school: '',
    notes:'',
    jwsession:''
})
const workform = reactive({
    bindid: '',
    workid: '',
    templateid: '',
    status: 0,
    starttime: '',
    endtime:'',
    email:''
})

const tanChange = (tabname: any) => {
    if (tabname=='userlist') {
        getUsers()
    } else if (tabname=='noticlist') {
        getNotics()
    } else if (tabname=='bindlist'){
        getBinds()
    } else if(tabname=='worklist'){
        getWorks()
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
      
    }

  })
}

const getBinds = () => {
  axios({
    method: 'get',
    url: '/v2/admin/getbinds',
    headers: { Authorization: 'Bearer ' + store.Authorization }
  }).then(function (response) {
    if (response) {
      let r_binds: any[] = response.data['data']['binds']
      binds.splice(0,binds.length)
      r_binds.forEach(e => {
        binds.push(e);
     });
    } else {
      
    }

  })
}

const getWorks = () => {
  axios({
    method: 'get',
    url: '/v2/admin/getworks',
    headers: { Authorization: 'Bearer ' + store.Authorization }
  }).then(function (response) {
    if (response) {
      let r_works: any[] = response.data['data']['works']
      works.splice(0,works.length)
      r_works.forEach(e => {
        works.push(e);
     });
    } else {
      
    }

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

const editBind = (index: number)=>{
    bindform.bindid=binds[index].bindid
    bindform.password=binds[index].password
    bindform.email=binds[index].email
    bindform.status=binds[index].status
    bindform.jwsession=binds[index].jwsession
    bindform.notes=binds[index].notes
    bindform.school=binds[index].school
    binddrawer.value = true
}

const editWork = (index: number)=>{
    workform.workid=works[index].workid
    workform.templateid=works[index].templateid
    workform.bindid=works[index].bindid
    workform.status=works[index].status
    workform.email=works[index].email
    workform.starttime=works[index].starttime
    workform.endtime=works[index].endtime

    workdrawer.value = true
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


const onBindChange=()=>{
    const bindid = bindform.bindid
    const password = bindform.password
    const email = bindform.email
    const jwsession = bindform.jwsession
    const status = bindform.status
    const notes = bindform.notes
    const school = bindform.school
    axios({
    method: 'get',
    url:'/v2/admin/changebind',
    headers: { Authorization: 'Bearer ' + store.Authorization},
    params: {
      bindid:bindid,password:password,email:email,jwsession:jwsession,status:status,notes:notes,school:school
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

const onWorkChange=()=>{
    const workid = workform.workid
    const templateid = workform.templateid
    const bindid = workform.bindid
    const starttime = workform.starttime
    const endtime = workform.endtime
    const status = workform.status
    const email = workform.email
    axios({
    method: 'get',
    url:'/v2/admin/changework',
    headers: { Authorization: 'Bearer ' + store.Authorization},
    params: {
      bindid:bindid,workid:workid,templateid:templateid,starttime:starttime,status:status,endtime:endtime,email:email
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