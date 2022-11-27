<template >
    <div style="display: flex;justify-content:center;align-items: center;">
        <el-card class="box-card" >
            <template #header>
                <div class="card-header">
                    <span>登录</span>
                </div>
            </template>
            <div class="common-layout" style="width:auto ;">
    
                <el-form :model="form" label-width="70px" label-suffix=":">
                    <el-form-item label="用户名">
                        <el-input style="width:auto ;" v-model="form.username"></el-input>
                    </el-form-item>
                    <el-form-item label="密码">
                        <el-input style="width:auto ;" type="password" v-model="form.password" show-password></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">登录</el-button>
                        <!-- <el-button type="primary" @click="onHello">Hello</el-button> -->
                    </el-form-item>
                </el-form>
                <p>{{ store.Authorization }}</p>
                <!-- <el-row align="middle" justify="center">
                <el-col :span="3"><p>用户名:</p></el-col><el-col :span="6"><el-input v-model="username" placeholder="Please input" /></el-col>
            </el-row>
            <el-row align="middle" justify="center">
                <el-col :span="3"><p>密码:</p></el-col><el-col :span="6"><el-input  type="password" v-model="password" placeholder="Please input" show-password /></el-col>
            </el-row> -->
    
                <!-- <el-input v-model="password" type="password" placeholder="Please input password" show-password />
            <p>password is: {{ password }}</p> -->
            </div>
        </el-card>
    </div>
    <!-- <div style="font-size: 15px;position:absolute;bottom:10px;left: 45%;">
                           <a href="https://beian.miit.gov.cn/">
                            陕ICP备2022013710号-1     
                           </a>            
                        </div> -->
</template>



<script lang="ts" setup>
// import { ref } from 'vue'
// const username = ref('')
// const password = ref('')
import { onBeforeMount, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '../defaultaxios'
import { ElMessage } from 'element-plus'
import { store } from '../store.js'
onBeforeMount(() => {
    //   console.log(store.Authorization)
    store.setAuthorization('')
})

const router = useRouter()
const route = useRoute()

const form = reactive({
    username: '',
    password: ''
})




// let access_token = store.Authorization

const onSubmit = () => {
    // console.log('username:' + form.username)
    // console.log('password:' + form.password)
    if (!(form.username && form.password)) {
        ElMessage({
            message: '请填写用户名和密码后重试',
            grouping: true,
            type: 'warning',
        })
    } else {
        axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
        axios({
            method: 'post', url: '/v2/token',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            data: {
                grant_type: "",
                username: form.username,
                password: form.password,
                scope: "",
                client_id: "",
                client_secret: ""
            }
        }).then(function (response) {
            // console.log("test on")
            // console.log(response.data.access_token);
            if (response.data.access_token=="") {
                ElMessage({
                message: '登录失败，请检查用户名和密码后重试.',
                grouping: true,
                type: 'warning',
            })
            }else{
                store.setAuthorization(response.data.access_token)
                router.push('/index/index')
            }
            // console.log(response.status);
            // console.log(response.statusText);
            // console.log(response.headers);
            // console.log(response.config);
        }).catch(function (reason) {
            ElMessage({
                message: '登录失败，请检查用户名和密码后重试.',
                grouping: true,
                type: 'warning',
            })
        })
    }


    //     axios({method: 'post',url: 'http://127.0.0.1:8000/',params: {
    //     ID: 12345
    //   },}).then(function (response) {
    //     con dole.log(response)
    //   })
    // console.log("123")
}

// const onHello = () => {
//     // axios({
//     //     method: 'get',
//     //     url: 'http://127.0.0.1:8000/',
//     //     headers: { Authorization: 'Bearer ' + store.Authorization }
//     // }).then(function (response) {
//     //     console.log(response.data)
//     // })

// }


</script>