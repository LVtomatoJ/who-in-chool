import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router/router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'


const app = createApp(App)
// const app = createApp({})

app.use(ElementPlus)
// app.use(router)
app.use(router)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.mount('#app')
