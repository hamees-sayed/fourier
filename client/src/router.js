import { createWebHistory, createRouter } from 'vue-router';
import Login from './pages/Login.vue';
import Register from './pages/Register.vue';
import Home from './pages/Home.vue';
import Account from './pages/Account.vue';
import PageNotFound from './pages/PageNotFound.vue';


const routes = [
    { path: '/', component: Home, meta: { auth: false } },
    { path: '/login', component: Login, meta: { auth: false } },
    { path: '/register', component: Register, meta: { auth: false } },
    { path: '/account', component: Account, meta: { auth: true } },
    { path: '/:pathMatch(.*)', component: PageNotFound, meta: { auth: false } },
]
  
const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.meta.auth && !localStorage.getItem('token')) {
    next('/login');
  } else {
    next();
  }
})

export default router;