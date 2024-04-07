import { createWebHistory, createRouter } from 'vue-router';
import Login from './pages/Login.vue';
import Register from './pages/Register.vue';
import Home from './pages/Home.vue';
import Account from './pages/Account.vue';
import PageNotFound from './pages/PageNotFound.vue';
import Albums from './pages/Albums.vue';
import SingleAlbum from './pages/SingleAlbum.vue';
import Form_RegisterCreator from './pages/Form_RegisterCreator.vue';
import Form_NewPlaylist from './pages/Form_NewPlaylist.vue';
import RateSong from './pages/RateSong.vue';
import SinglePlaylist from './pages/SinglePlaylist.vue';
import Form_UpdatePlaylist from './pages/Form_UpdatePlaylist.vue';
import Form_AddToPlaylist from './pages/Form_AddToPlaylist.vue';
import CreatorAccount from './pages/CreatorAccount.vue';
import CreatorAlbums from './pages/CreatorAlbums.vue';
import Form_NewAlbum from './pages/Form_NewAlbum.vue';
import Form_UpdateAlbum from './pages/Form_UpdateAlbum.vue';
import SingleCreatorAlbum from './pages/SingleCreatorAlbum.vue';


const routes = [
    { path: '/', component: Home, meta: { auth: false } },
    { path: '/login', component: Login, meta: { auth: false } },
    { path: '/register', component: Register, meta: { auth: false } },
    { path: '/account', component: Account, meta: { auth: true } },
    { path: '/creator', component: CreatorAccount, meta: { auth: true } },
    { path: '/creator/albums', component: CreatorAlbums, meta: { auth: true } },
    { path: '/creator/album/new', component: Form_NewAlbum, meta: { auth: true } },
    { path: '/creator/album/update/:id', component: Form_UpdateAlbum, meta: { auth: true } },
    { path: '/creator/album/:id', component: SingleCreatorAlbum, meta: { auth: true } },
    { path: '/albums', component: Albums, meta: { auth: true } },
    { path: '/albums/:id', component: SingleAlbum, meta: { auth: true } },
    { path: '/creator/register', component: Form_RegisterCreator, meta: { auth: true } },
    { path: '/playlist/new', component: Form_NewPlaylist, meta: { auth: true } },
    { path: '/rate/:id', component: RateSong, meta: { auth: true } },
    { path: '/playlist/:id', component: SinglePlaylist, meta: { auth: true } },
    { path: '/playlist/update/:id', component: Form_UpdatePlaylist, meta: { auth: true } },
    { path: '/playlist/add/:id', component: Form_AddToPlaylist, meta: { auth: true } },
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