import { createRouter,createWebHistory } from "vue-router";
import Login from '../components/Login.vue';
import Index from '../components/Index.vue';
import IndexMain from '../components/IndexMain.vue';
import UsersMain from '../components/UsersMain.vue';
import WorksMain from '../components/WorksMain.vue';
import AdminMain from '../components/AdminMain.vue';

import {store} from '../store'
const router = createRouter({
    history:createWebHistory(),
    routes:[
        {
            path:'/login',
            name:'Login',
            component:Login,
        },
        {
            path:'/',
            component:Login,
        },
        {
            path:'/index',
            name:'Index',
            component:Index,
            children: [
                {
                  // 当 /user/:id/profile 匹配成功
                  // UserProfile 将被渲染到 User 的 <router-view> 内部
                  path: 'index',
                  component: IndexMain,
                },
                {
                    // 当 /user/:id/profile 匹配成功
                    // UserProfile 将被渲染到 User 的 <router-view> 内部
                    path: 'users',
                    component: UsersMain,
                  },
                  {
                    // 当 /user/:id/profile 匹配成功
                    // UserProfile 将被渲染到 User 的 <router-view> 内部
                    path: 'works',
                    component: WorksMain,
                  },
                  {
                    // 当 /user/:id/profile 匹配成功
                    // UserProfile 将被渲染到 User 的 <router-view> 内部
                    path: 'admin',
                    component: AdminMain,
                  },
            ]
        },
    ]
})


// 守护路由
router.beforeEach(async (to, from) => {
    if (
      // 检查用户是否已登录
      !store.Authorization &&
      // ❗️ 避免无限重定向
      to.name !== 'Login'
    ) {
      // 将用户重定向到登录页面
      return { name: 'Login' }
    }
  })



export default router;

