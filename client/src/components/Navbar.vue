<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary py-0 px-4">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">
        <img src="../assets/logo.png" width="110" height="70" />
      </RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        </ul>
        <span class="navbar-text">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
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
import { IS_AUTHENTICATED } from '../store/storeconstants';

export default {
  computed: {
    ...mapGetters('auth', {
      isAuthenticated: IS_AUTHENTICATED,
    })
  },
  methods: {
    logOut() {
      localStorage.clear();
      this.$router.push('/');
      location.reload();
    }
  }
};

</script>
