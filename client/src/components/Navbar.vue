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
            <li class="nav-item" v-if="loggedIn">
              <a class="nav-link btn btn-link" @click="logout">Logout</a>
            </li>
            <div class="d-flex flex-row" v-else>
              <li class="nav-item">
                <RouterLink class="nav-link active" to="/login">Login</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/register">Register</RouterLink>
              </li>
          </div>
          </ul>
        </span>
      </div>
    </div>
  </nav>
</template>

<script>
import { RouterLink } from 'vue-router';

export default {
  components: {
    RouterLink
  },
  data() {
    return {
      loggedIn: false
    };
  },
  created() {
    this.checkLoggedIn();
  },
  methods: {
    checkLoggedIn() {
      const token = localStorage.getItem('token');
      this.loggedIn = !!token;
    },
    logout(){
      localStorage.removeItem('token');
      this.loggedIn = false;
      this.$router.push('/login');
    }
  },
  watch: {
    loggedIn(newValue) {
      if (newValue) {
        localStorage.setItem('token', localStorage.getItem('token'));
      } else {
        localStorage.removeItem('token');
      }
    }
  }
};

</script>
