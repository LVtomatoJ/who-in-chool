import { createRouter,createWebHistory } from "vue-router";
import Login from '../components/Login.vue';
import Index from '../components/Index.vue';
const router = createRouter({
    history:createWebHistory(),
    routes:[
        {
            path:'/login',
            component:Login,
        },
        {
            path:'/',
            component:Login,
        },
        {
            path:'/index',
            component:Index,
        },
    ]
})


// 守护路由
// router.beforeEach(async (to, from) => {
//     if (
//       // 检查用户是否已登录
//       !isAuthenticated &&
//       // ❗️ 避免无限重定向
//       to.name !== 'Login'
//     ) {
//       // 将用户重定向到登录页面
//       return { name: 'Login' }
//     }
//   })

export default router;

