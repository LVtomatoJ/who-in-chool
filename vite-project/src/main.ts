import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './style.css'
import App from './App.vue'
import router from './router/router'


const app = createApp(App)
// const app = createApp({})

app.use(ElementPlus)
// app.use(router)
app.use(router)

app.mount('#app')
