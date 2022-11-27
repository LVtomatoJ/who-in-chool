import axios from 'axios'
// import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import router from './router/router'
import {store} from './store'
// const router = useRouter()
// const route = useRoute()

// axios.defaults.baseURL = 'https://www.wozaixiaoyuan.cn/'
axios.defaults.baseURL = 'http://127.0.0.1:8000/'
axios.defaults.withCredentials = true
// axios.defaults.headers.common['Authorization'] = 'Bearer' + store.Authorization;
// function redirectLogin () {
//     router.push('/login')
//   }

// axios.interceptors.request.use(function (config) {
//     // Do something before request is sent
//     if (store.Authorization){
//         config.headers.Authorization = 'Bearer' + store.Authorization;
//     }
//     return config;
//   }, function (error) {
//     // Do something with request error
//     return Promise.reject(error);
//   });


axios.interceptors.response.use(res => {
    // console.log('headers:'+res.headers);
    return res
}, err => {
    
    const status = err.response.status
    if (status==401){
        ElMessage({
            message: '登录失效请重新登录',
            grouping: true,
            type: 'error',
        })
        router.push('/login')
    }else{
        return Promise.reject(err)
    }
})



// axios.interceptors.response.use(function (data){
//     return data
// },function (error){
//     router.push('/login')
//     console.log("gogologin")
// })


export default axios;