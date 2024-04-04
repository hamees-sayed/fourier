<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary py-0 px-4">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">
        <img src="../assets/logo.png" width="110" height="70" />
      </RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="d-flex" v-if="isAuthenticated">
        <div class="header__option">
          <a class="btn btn-primary active" href="/" role="button">Songs 🎶</a>
        </div>
        <div class="header__option">
          <a class="btn btn-primary active" href="/albums" role="button">Albums 💿</a>
        </div>
      </div>
      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        </ul>
        <span class="navbar-text">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item" v-if="isAuthenticated && !isCreator">
              <a class="nav-link btn btn-link" href="/creator/register">Become Creator</a>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <a class="nav-link btn btn-link" href="/account">Account</a>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <a class="nav-link btn btn-link" @click.prevent="logOut">Logout</a>
            </li>
            <li class="nav-item" v-if="!isAuthenticated">
              <RouterLink class="nav-link active" to="/login">Login</RouterLink>
            </li>
            <li class="nav-item" v-if="!isAuthenticated">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
          </ul>
        </span>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex';
import { IS_AUTHENTICATED, IS_CREATOR, IS_ADMIN } from '../store/storeconstants';

export default {
  computed: {
    ...mapGetters('auth', {
      isAuthenticated: IS_AUTHENTICATED,
      isCreator: IS_CREATOR,
      isAdmin: IS_ADMIN,
    })
  },
  methods: {
    logOut() {
      localStorage.clear();
      this.$router.push('/');
      location.reload();
    }
  },
  mounted(){
    console.log(`creator: ${this.isCreator}, admin: ${this.isAdmin}, auth: ${this.isAuthenticated}`)
  }
};
</script>
