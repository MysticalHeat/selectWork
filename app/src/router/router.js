import eventForm from '@/pages/eventForm'
import {createRouter, createWebHistory} from "vue-router";

const routes = [
  {
    path: '/',
    component: eventForm
  }
]

const router = createRouter( {
  routes,
  history: createWebHistory(process.env.BASE_URL)
})

export default router;
