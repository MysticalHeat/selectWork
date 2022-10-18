import { createApp } from 'vue'
import App from './App.vue'
import router from "@/router/router"
import components from '@/components'
import store from "@/store";

const app = createApp(App)

Object.keys(components).forEach(([key, component]) => {
  app.component(component.name)
})

app
  .use(router)
  .use(store)
  .mount('#app')
