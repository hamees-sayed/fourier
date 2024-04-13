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
import CreatorSongs from './pages/CreatorSongs.vue';
import Form_NewSong from './pages/Form_NewSong.vue';
import Form_UpdateSong from './pages/Form_UpdateSong.vue';
import AdminAlbums from './pages/AdminAlbums.vue';
import AdminCreators from './pages/AdminCreators.vue';
import AdminDashboard from './pages/AdminDashboard.vue';
import AdminUsers from './pages/AdminUsers.vue';
import AdminLogin from './pages/AdminLogin.vue';
import Unauthorized from './pages/Unauthorized.vue';


const routes = [
    { path: '/', component: Home, meta: { auth: false } },
    { path: '/login', component: Login, meta: { auth: false } },
    { path: '/register', component: Register, meta: { auth: false } },
    { path: '/account', component: Account, meta: { auth: true } },
    { path: '/creator', component: CreatorAccount, meta: { auth: true } },
    { path: '/creator/albums', component: CreatorAlbums, meta: { auth: true } },
    { path: '/creator/songs', component: CreatorSongs, meta: { auth: true } },
    { path: '/creator/album/new', component: Form_NewAlbum, meta: { auth: true } },
    { path: '/creator/album/update/:id', component: Form_UpdateAlbum, meta: { auth: true } },
    { path: '/creator/album/:id', component: SingleCreatorAlbum, meta: { auth: true } },
    { path: '/creator/song/new', component: Form_NewSong, meta: { auth: true } },
    { path: '/creator/song/update/:id', component: Form_UpdateSong, meta: { auth: true } },
    { path: '/albums', component: Albums, meta: { auth: true } },
    { path: '/albums/:id', component: SingleAlbum, meta: { auth: true } },
    { path: '/creator/register', component: Form_RegisterCreator, meta: { auth: true } },
    { path: '/playlist/new', component: Form_NewPlaylist, meta: { auth: true } },
    { path: '/rate/:id', component: RateSong, meta: { auth: true } },
    { path: '/playlist/:id', component: SinglePlaylist, meta: { auth: true } },
    { path: '/playlist/update/:id', component: Form_UpdatePlaylist, meta: { auth: true } },
    { path: '/playlist/add/:id', component: Form_AddToPlaylist, meta: { auth: true } },
    { path: '/admin/login', component: AdminLogin, meta: { auth: false } },
    { path: '/admin/albums', component: AdminAlbums, meta: { auth: true, requiresAdmin: true } },
    { path: '/admin/creators', component: AdminCreators, meta: { auth: true, requiresAdmin: true } },
    { path: '/admin/dashboard', component: AdminDashboard, meta: { auth: true, requiresAdmin: true } },
    { path: '/admin/users', component: AdminUsers, meta: { auth: true, requiresAdmin: true } },
    { path: '/unauthorized', component: Unauthorized, meta: { auth: false } },
    { path: '/:pathMatch(.*)', component: PageNotFound, meta: { auth: false } },
]
  
const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token');
  const isAdmin = localStorage.getItem('is_admin');
  const isCreator = localStorage.getItem('is_creator');

  if (to.meta.auth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.requiresAdmin && isAdmin !== 'true') {
    next('/unauthorized');
  } else {
    next();
  }
});

export default router;