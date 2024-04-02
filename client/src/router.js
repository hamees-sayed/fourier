import { createWebHistory, createRouter } from 'vue-router';
import Login from './pages/Login.vue';
import Register from './pages/Register.vue';
import Home from './pages/Home.vue';


const routes = [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
]
  
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router;